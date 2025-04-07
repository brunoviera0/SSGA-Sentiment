from wordcloud import WordCloud
import matplotlib.pyplot as plt
from google.cloud import datastore, storage

#config
PROJECT_ID = "sentiment-analysis-379200"
BUCKET_NAME = "news_40999"

datastore_client = datastore.Client(project=PROJECT_ID)
storage_client = storage.Client(project=PROJECT_ID)

#query ssga_transcripts
query = datastore_client.query(kind="ssga_transcripts")
for entity in query.fetch():
    ticker = entity["Ticker"]
    period = entity["Period"]
    paragraphs = entity["Transcript"]

    #combine all paragraphs into one string
    text = " ".join(paragraphs)

    #generate word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    #save .png file
    filename = f"{ticker}_{period}.png"
    wordcloud.to_file(filename)

    #upload to Google Cloud Storage
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_filename(filename)

    print(f"Word cloud for {ticker} ({period}) saved.")
