# SSGA-Sentiment

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



cc_wordcloud.py generates a word cloud based on the transcripts stored in ssga_transcripts, saves them as a .png file, and stores them in a bucket.
