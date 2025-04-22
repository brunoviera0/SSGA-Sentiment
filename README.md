# SSGA-Sentiment

ran schema.py once to create typesense

To create local typesense server:

sudo docker pull typesense/typesense:0.25.1

sudo docker run -p 8108:8108 -v /tmp/typesense-data:/data \typesense/typesense:0.25.1 --data-dir /data --api-key=SSGAtester --enable-cors


Local server used for testing, need to switch to paid cloud server.

cc_FINAL.py

to run:  export APININJAS_API_KEY="key"

usage of file is python3 cc_FINAL.py Year Quarter

example: python3 cc_FINAL.py 2024 2

uses process_transcript function from scoring.py created by last year's team

Datastore tables:

-CompanyInfo (contains info such as tickers and sector)

-ssga_detail (creates entities summarizing sentiment for keyword paragraphs)

-ssga_sentiment (average sentiment scores)

-ssga_transcripts (contains full transcripts pulled from API_NINJAS)

-ssga_keywords (ssga keywords with category and sector)

cc_wordcloud.py generates a word cloud based on the transcripts stored in ssga_transcripts, saves them as a .png file, and stores them in a bucket.
