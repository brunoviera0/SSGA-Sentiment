# SSGA-Sentiment

run schema.py only once to create typesense

To create local typesense server:

sudo docker pull typesense/typesense:0.25.1

sudo docker run -p 8108:8108 -v /tmp/typesense-data:/data \typesense/typesense:0.25.1 --data-dir /data --api-key=SSGAtester --enable-cors

example of how to index using typesense can be found "typesense_test.py"

Local server used for testing, need to switch to paid cloud server.


cc_wordcloud.py: generates a wordcloud based off of a stored earnings call transcript, then stores the file in a bucket within google storage



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


dailypricesjob.py

to run: python3 dailypricesjob.py

Pulls today's stock price and volume data for the tickers found in the CompanyInfo table

Creates an entity for each ticker in the Dailyprices Datastore table with: ticker, price, volume, timestamp

If no data is found for a ticker, the script will print a message and continue.

To set up automatic daily price updates using cron:

The script is scheduled to run Monday through Friday at 4:00 PM Eastern Time.

Crontab entry:

00 20 * * 1-5 /usr/bin/python3 /home/sentapp/dailyprices/dailypricesjob.py >> /home/sentapp/dailyprices/cron_log.txt 2>&1

Runs dailypricesjob.py every weekday at 4 PM Eastern Time.

Output and errors are logged to cron_log.txt inside the same folder.

To edit or view the current crontab-

crontab -e
