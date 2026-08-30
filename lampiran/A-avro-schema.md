# Lampiran A — Skema Avro untuk Event CIF

```json
{
  "type": "record",
  "name": "CifEvent",
  "namespace": "com.bank.cif.events",
  "version": "1.0",
  "fields": [
    { "name": "event_id",       "type": "string" },
    { "name": "event_type",     "type": { "type": "enum",
                                          "name": "EventType",
                                          "symbols": ["CREATE","UPDATE","DELETE","MATCH_DECISION"] } },
    { "name": "source_system",  "type": "string" },
    { "name": "source_record_id","type": "string" },
    { "name": "correlation_id", "type": "string" },
    { "name": "event_time",     "type": "long", "logicalType": "timestamp-millis" },
    { "name": "incoming_record", "type": {
        "type": "record",
        "name": "Party",
        "fields": [
          { "name": "nik",          "type": ["null","string"], "default": null },
          { "name": "npwp",         "type": ["null","string"], "default": null },
          { "name": "nama_lengkap", "type": "string" },
          { "name": "nama_ibu",     "type": ["null","string"], "default": null },
          { "name": "jenis_kelamin","type": ["null","string"], "default": null },
          { "name": "tanggal_lahir","type": ["null","string"], "default": null },
          { "name": "tempat_lahir", "type": ["null","string"], "default": null },
          { "name": "alamat",       "type": ["null","string"], "default": null },
          { "name": "kota",         "type": ["null","string"], "default": null },
          { "name": "provinsi",     "type": ["null","string"], "default": null },
          { "name": "kode_pos",     "type": ["null","string"], "default": null },
          { "name": "phone",        "type": ["null","string"], "default": null },
          { "name": "email",        "type": ["null","string"], "default": null },
          { "name": "jenis_pihak",  "type": { "type": "enum", "name": "PartyType",
                                                "symbols": ["INDIVIDUAL","ORGANIZATION"] } },
          { "name": "nib",          "type": ["null","string"], "default": null },
          { "name": "kyc_status",   "type": ["null","string"], "default": null }
        ]
    }},
    { "name": "decision",       "type": ["null", {
        "type": "record",
        "name": "MatchDecision",
        "fields": [
          { "name": "cif_id",     "type": "string" },
          { "name": "match_score","type": "double" },
          { "name": "match_reason","type": "string" },
          { "name": "candidates", "type": { "type": "array",
                                            "items": {
                                              "type": "record",
                                              "name": "Candidate",
                                              "fields": [
                                                { "name": "cif_id", "type": "string" },
                                                { "name": "score",  "type": "double" },
                                                { "name": "breakdown", "type": "string" }
                                              ]
                                            } } }
        ]
    }], "default": null }
  ]
}
```
