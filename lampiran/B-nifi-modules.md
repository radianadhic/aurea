# Lampiran B — Daftar Modul NiFi (NAR / Processor Kustom)

Modul-modul ini dapat dibungkus dalam satu NAR (`cif-matching-nar`) untuk menjaga konsistensi pipeline matching.

| Modul | Fungsi | Input | Output |
|---|---|---|---|
| `CifStandardize` | Standarisasi nama (lowercase, trim, hapus gelar "Dr/Hj/Mr"), normalisasi alamat (libpostal), normalisasi tanggal (DD-MM-YYYY → ISO) | FlowFile (JSON) | FlowFile terstandar + field `*_normalized` |
| `CifNikHash` | Hitung SHA-256(salt + NIK) | field `nik` | `nik_hash` |
| `CifExactLookup` | Multi-key lookup ke Valkey | `nik_hash`, `npwp_hash`, `email_norm`, `phone_e164` | `cif_id` (jika ketemu) + `match_layer=EXACT` |
| `CifFuzzySearch` | Query Elasticsearch (BM25 + fuzziness) | nama, alamat, tgl lahir | top-20 candidate + `match_layer=FUZZY` |
| `CifGraphSearch` | Query Neo4j via Bolt | cif_id, nama, alamat | candidate relasi (household/UBO) |
| `CifScoreAggregator` | Gabungkan skor + tentukan AUTO/POSSIBLE/NEW | hasil exact+fuzzy+graph | `decision`, `score_total`, `reason_code` |
| `CifSurvivorship` | Terapkan aturan source-of-record per field | incoming vs existing | merged record + `field_change_log` |
| `CifMasterUpsert` | Upsert idempotent ke `party_master` | merged record | outcome + `lineage_rows` |
| `CifCacheRefresh` | Update key `cif:{cif_id}` di Valkey | cif_id + record | cache entry baru + invalidate key lama |
| `CifException` | Tulis ke `cif_match_exception` (jika POSSIBLE_MATCH) | event + candidates | exception_id |
| `CifAuditLog` | Tulis ke `match_audit_log` | decision + skor + user | 1 row per keputusan |
| `CifBroadcast` | Publish ke Kafka `cif.broadcast` | event akhir | Kafka record |

### Pengemasan NAR
```
cif-matching-nar/
├── nifi-cif-nar-1.0.0.nar
├── config/
│   ├── salt.properties        # salt untuk hashing NIK
│   ├── survivor-rules.yaml   # aturan survivorship per field
│   └── scoring-weights.yaml  # bobot skor (cosine, jaccard, dll)
└── docs/
    └── README.md
```

### Controller Service terkait
- `SaltService` — membaca salt dari Vault, rotasi setiap 90 hari.
- `SurvivorRulesService` — load YAML aturan, *hot-reload*.
- `MatchScoringService` — implementasi rumus skor di Java.
EOF
