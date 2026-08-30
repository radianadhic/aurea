# Lampiran C — Konfigurasi Elasticsearch & Cypher

## C.1 Elasticsearch — Index Template (lengkap)

```bash
# Buat custom analyzer untuk bahasa Indonesia
PUT /_index_template/cif_party_template
{
  "index_patterns": ["cif_party*"],
  "template": {
    "settings": {
      "number_of_shards": 5,
      "number_of_replicas": 2,
      "analysis": {
        "filter": {
          "indonesian_stop": {
            "type": "stop",
            "stopwords": "_indonesian_"
          },
          "indonesian_stemmer": {
            "type": "stemmer",
            "language": "indonesian"
          },
          "indonesian_normalization": {
            "type": "icu_normalizer",
            "name": "nfc"
          }
        },
        "analyzer": {
          "cif_name_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "asciifolding",
              "indonesian_normalization",
              "indonesian_stop",
              "indonesian_stemmer",
              "ngram_3_5"
            ]
          },
          "cif_address_analyzer": {
            "type": "custom",
            "tokenizer": "standard",
            "filter": [
              "lowercase",
              "asciifolding",
              "indonesian_normalization"
            ]
          }
        }
      }
    },
    "mappings": {
      "properties": {
        "cif_id":            { "type": "keyword" },
        "nik_hash":          { "type": "keyword" },
        "npwp_hash":         { "type": "keyword" },
        "nama_lengkap": {
          "type": "text",
          "analyzer": "cif_name_analyzer",
          "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } }
        },
        "nama_normalized":   { "type": "keyword" },
        "tanggal_lahir":     { "type": "date", "format": "yyyy-MM-dd||strict_date_optional_time" },
        "tempat_lahir":      { "type": "text", "analyzer": "standard",
                               "fields": { "keyword": { "type": "keyword" } } },
        "alamat":            { "type": "text", "analyzer": "cif_address_analyzer" },
        "alamat_normalized": { "type": "keyword" },
        "kota":              { "type": "keyword" },
        "provinsi":          { "type": "keyword" },
        "kode_pos":          { "type": "keyword" },
        "phone_e164":        { "type": "keyword" },
        "email_norm":        { "type": "keyword" },
        "jenis_kelamin":     { "type": "keyword" },
        "jenis_pihak":       { "type": "keyword" },
        "nib":               { "type": "keyword" },
        "kyc_status":        { "type": "keyword" },
        "status":            { "type": "keyword" },
        "created_at":        { "type": "date" },
        "updated_at":        { "type": "date" }
      }
    }
  }
}
```

## C.2 Query Multi-Match dengan Boost

```json
POST /cif_party/_search
{
  "size": 20,
  "_source": ["cif_id", "nama_lengkap", "tanggal_lahir",
              "tempat_lahir", "alamat", "kota"],
  "query": {
    "function_score": {
      "query": {
        "bool": {
          "must": [
            { "multi_match": {
                "query": "{{nama_input}}",
                "fields": ["nama_lengkap^3", "nama_lengkap.keyword^4"],
                "fuzziness": "AUTO:4,7",
                "prefix_length": 1
            }}
          ],
          "should": [
            { "term":  { "tanggal_lahir": { "value": "{{tgl_lahir}}", "boost": 4 } } },
            { "match": { "tempat_lahir":  { "query": "{{tempat_lahir}}", "boost": 2 } } },
            { "match": { "alamat":        { "query": "{{alamat_input}}", "boost": 1.5 } } },
            { "term":  { "kota":          { "value": "{{kota}}", "boost": 1.2 } } },
            { "term":  { "phone_e164":    { "value": "{{phone_e164}}", "boost": 3 } } },
            { "term":  { "email_norm":    { "value": "{{email_norm}}", "boost": 3 } } }
          ],
          "filter": [
            { "term": { "status": "active" } }
          ]
        }
      },
      "field_value_factor": {
        "field": "updated_at",
        "factor": 0.00000001,
        "modifier": "ln1p",
        "missing": 0
      },
      "boost_mode": "sum"
    }
  }
}
```

## C.3 Cypher Queries untuk Graph Matching

### C.3.1 Cari household candidate
```cypher
// Parameter: $cif_id, $alamat_norm, $nama_part
MATCH (p:Person {cif_id: $cif_id})-[:LIVES_AT]->(a:Address)
MATCH (other:Person)-[:LIVES_AT]->(a)
WHERE other.cif_id <> $cif_id
WITH other, a,
     apoc.text.jaroWinklerDistance(toLower(other.nama), toLower($nama_input)) AS jw
WHERE jw > 0.85
RETURN other.cif_id, other.nama, jw AS score
ORDER BY score DESC LIMIT 5;
```

### C.3.2 Deteksi beneficial owner ganda
```cypher
MATCH (p:Person)-[r:BENEFICIAL_OWNER_OF]->(o:Organization)
WHERE o.nib = $nib
WITH o, collect({cif_id: p.cif_id, nama: p.nama,
                 percent: r.percent, since: r.since}) AS ubos
WHERE size(ubos) > 1
RETURN o.cif_id AS org_cif, o.nama, ubos;
```

### C.3.3 Auto-suggest household link
```cypher
// Jalankan periodik setiap malam
MATCH (p1:Person)-[:LIVES_AT]->(a1:Address)
MATCH (p2:Person)-[:LIVES_AT]->(a2:Address)
WHERE a1.alamat_norm = a2.alamat_norm
  AND p1.cif_id < p2.cif_id
  AND NOT (p1)-[:MEMBER_OF]->(:Household)<-[:MEMBER_OF]-(p2)
WITH p1, p2, a1 LIMIT 1000
MERGE (h:Household {addr_id: a1.addr_id})
  ON CREATE SET h.created_at = datetime()
MERGE (p1)-[:MEMBER_OF {since: datetime()}]->(h)
MERGE (p2)-[:MEMBER_OF {since: datetime()}]->(h)
RETURN count(*) AS households_created;
```

### C.3.4 Reconciliation Postgres ↔ Neo4j
```cypher
// Tandai cif yang sudah tidak ada di Postgres
MATCH (p:Person)
WHERE NOT EXISTS {
  MATCH (pgRow:PostgresMirror {cif_id: p.cif_id})
  WHERE pgRow.deleted_at IS NULL
}
SET p.status = 'orphan', p.flagged_at = datetime()
RETURN p.cif_id;
```
EOF
