import os
import tweepy
import requests
import random

X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]
AI_API_KEY = os.environ["AI_API_KEY"]

AI_BASE_URL = "https://chat.khoirulaziz757.workers.dev/v1"

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

    headers = {
        "Authorization": "Bearer " + AI_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "model": "@cf/meta/llama-3.3-70b-instruct-fp8-fast",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 100,
    }

    response = requests.post(AI_BASE_URL + "/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    tweet = data["choices"][0]["message"]["content"].strip()

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
    
