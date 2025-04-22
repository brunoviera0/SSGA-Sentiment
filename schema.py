###creates typesense collection for ssga_detail

schema = {
  "name": "ssga_detail",
  "fields": [
    { "name": "Period", "type": "string" },
    { "name": "Category", "type": "string", "facet": True },
    { "name": "DocumentType", "type": "string" },
    { "name": "Keyword", "type": "string", "facet": True },
    { "name": "Paragraph", "type": "string" },
    { "name": "Score", "type": "float" },
    { "name": "Magnitude_Score", "type": "float" },
    { "name": "Ticker", "type": "string", "facet": True }
  ],
  "default_sorting_field": "Score"
}

typesense_client.collections.create(schema)
