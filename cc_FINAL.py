import os
import json
import sys
import requests
from typing import List
import pandas as pd
from google.cloud import storage
from google.cloud import datastore
from scoring import process_transcript

#Google Cloud Configuration
PROJECT_ID = "sentiment-analysis-379200"
storage_client = storage.Client(project=PROJECT_ID)
datastore_client = datastore.Client(project=PROJECT_ID)

#API Ninjas authentication
def get_authenticated(url):
    headers = {'X-Api-Key': os.getenv('APININJAS_API_KEY')}
    return requests.get(url, headers=headers)

#API Ninjas (ticker, year, and quarter)
def earnings_calls(tickers: List[str], year: int, quarter: int):
    transcripts = {}

    for ticker in tickers:
        source = get_authenticated(
            f"https://api.api-ninjas.com/v1/earningstranscript?ticker={ticker}&year={year}&quarter={quarter}"
        )
        if source.status_code != 200:
            print(f"Error for {ticker}: {source.status_code} - {source.text}")
            continue

        try:
            resObj = json.loads(source.text)
            paragraphs = resObj['transcript'].split('\n')
            transcripts[ticker] = paragraphs
        except:
            print(f"Failed to decode JSON response for {ticker}, {year}Q{quarter}")

    return transcripts

#pull all tickers from CompanyInfo
def get_all_tickers():
    query = datastore_client.query(kind="CompanyInfo")
    return [entity["Ticker"] for entity in query.fetch() if "Ticker" in entity]

#pull all keywords and categories from ssga_keywords
def get_all_keywords():
    query = datastore_client.query(kind="ssga_keywords")
    return [(entity["Keyword"], entity["Category"]) for entity in query.fetch() if "Keyword" in entity and "Category" in entity]

#process and store sentiment data and keyword matches
def store_to_datastore(ticker, year, quarter, paragraphs):
    call_date = f"{year} Q{quarter}"
    period = f"Q{quarter}{year}"

    transcript_entity = datastore.Entity(
    key=datastore_client.key("ssga_transcripts"),
    exclude_from_indexes=["Transcript"] #exclude from indexing (otherwise transcripts are too large)
    )
    transcript_entity.update({
        "Ticker": ticker,
        "Period": period,
        "Transcript": paragraphs
    })
    datastore_client.put(transcript_entity)

    #keyword and category mappings
    keyword_tuples = get_all_keywords()
    keywords_list = [k for k, _ in keyword_tuples]
    category_map = {k: c for k, c in keyword_tuples}

    #format as DataFrames for process_transcript
    transcript_df = pd.DataFrame(paragraphs, columns=["Transcript"])
    keywords_df = pd.DataFrame({
        "Keyword": keywords_list,
        "Category": [category_map[k] for k in keywords_list]
    })

    #scoring and keyword matching
    processed_df = process_transcript(transcript_df, keywords_df)

    #ssga_detail entity
    if processed_df.empty:
        print(f"No keyword-matching paragraphs found for {ticker}. Skipping ssga_detail.")
    else:
        for index, row in processed_df.iterrows():
            detail_entity = datastore.Entity(datastore_client.key("ssga_detail"))
            detail_entity.update({
                "Period": period,
                "Category": row["Category"],
                "DocumentType": "Conference Call",
                "Keyword": row["Keyword"],
                "Paragraph": row["Paragraph"],
                "Score": row["Sentiment Score"],
                "Magnitude_Score": row["Sentiment Magnitude"],
                "Ticker": ticker
            })
            datastore_client.put(detail_entity)

    #average sentiment for call ssga_sentiment
    count = len(processed_df)
    avg_score = processed_df["Sentiment Score"].mean() if count > 0 else 0.0
    avg_magnitude = processed_df["Sentiment Magnitude"].mean() if count > 0 else 0.0

    sentiment_key = datastore_client.key("ssga_sentiment", f"{ticker}_{period}")
    sentiment_entity = datastore.Entity(sentiment_key)
    sentiment_entity.update({
        "Category": "AI",
        "Count": count,
        "Average_Sentiment_Score": avg_score,
        "Average_Magnitude_Score": avg_magnitude,
        "Period": period
    })
    datastore_client.put(sentiment_entity)

    print(f"Stored {ticker} data in Datastore.")

#process transcripts for all companies
def run():
    tickers = get_all_tickers()
    if len(sys.argv) < 3:
        print("Usage: python3 cc_FINAL.py <year> <quarter>")
        sys.exit(1)

    year = int(sys.argv[1])
    quarter = int(sys.argv[2])


    transcripts = earnings_calls(tickers, year, quarter)

    if not transcripts:
        print("No earnings call data available")
        return

    for ticker, paragraphs in transcripts.items():
        if paragraphs:
            store_to_datastore(ticker, year, quarter, paragraphs)
        else:
            print(f"No transcript available for {ticker}")


if __name__ == "__main__":
    run()
