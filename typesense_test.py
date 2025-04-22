import typesense

#connect to Typesense instance
typesense_client = typesense.Client({
    'nodes': [{
        'host': 'localhost',
        'port': '8108',
        'protocol': 'http'
    }],
    'api_key': 'SSGAtester',
    'connection_timeout_seconds': 2
})

#initialize
page = 1
all_hits = []

#fetch pages until there are no more results
while True:
    results = typesense_client.collections['ssga_detail'].documents.search({ ### select tables and then filter
        'q': 'AI agent', #word = AI Agent
        'query_by': 'Keyword',
        'filter_by': 'Keyword:=\"AI agent\"', #look for AI Agent entries in the keyword column
        'per_page': 100,
        'page': page
    })

    hits = results.get('hits', [])
    if not hits:
        break

    all_hits.extend(hits)
    page += 1

#display all of the matches
for hit in all_hits:
    doc = hit['document']
    print(f"{doc['Ticker']} | {doc['Period']} | {doc['Keyword']}")
    print(f"→ {doc['Paragraph']}\n")
