import os
import tweepy
from google import genai
import random

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]

client_ai = genai.Client(api_key=GEMINI_API_KEY)

themes = [
    "kehidupan anak kos yang chaos tapi tetap optimis",
    "drama kerja remote yang absurd",
    "overthinking tengah malam soal hal sepele",
    "budaya rebahan dan produktivitas palsu",
    "dilema antara hemat dan jajan",
    "drama grup chat keluarga",
]

PROMPT = "Kamu adalah akun Twitter humor Indonesia absurd dan sarkastik. Tulis 1 tweet dalam Bahasa Indonesia. Maksimal 250 karakter, tanpa hashtag, max 1 emoji, tone deadpan. Hanya tulis tweetnya saja."

def generate_tweet():
    theme = random.choice(themes)
    full_prompt = PROMPT + " Tema: " + theme
    response = client_ai.models.generate_content(
        model="gemini-2.0-flash",
        contents=full_prompt,
    )
    tweet = response.text.strip()
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    return tweet

def post_tweet(text):
    client_x = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )
    response = client_x.create_tweet(text=text)
    print("Tweet posted! ID: " + str(response.data["id"]))
    print("Content: " + text)
    return response

def main():
    print("Generating tweet...")
    tweet = generate_tweet()
    print("Generated: " + tweet)
    post_tweet(tweet)

if __name__ == "__main__":
    main()
