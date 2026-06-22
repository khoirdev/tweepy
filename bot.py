import os
import sys
import tweepy
import requests
import random

# Read environment variables safely
X_API_KEY = os.environ.get("X_API_KEY")
X_API_SECRET = os.environ.get("X_API_SECRET")
X_ACCESS_TOKEN = os.environ.get("X_ACCESS_TOKEN")
X_ACCESS_SECRET = os.environ.get("X_ACCESS_SECRET")
AI_API_KEY = os.environ.get("AI_API_KEY")

AI_BASE_URL = "https://chat.khoirulaziz757.workers.dev/v1"

themes = [
    "kehidupan anak kos yang chaos tapi tetap optimis",
    "drama kerja remote yang absurd",
    "overthinking tengah malam soal hal sepele",
    "budaya rebahan dan produktivitas palsu",
    "dilema antara hemat dan jajan",
    "drama grup chat keluarga",
]

PROMPT = "Kamu adalah akun Twitter humor Indonesia absurd dan sarkastik. Tulis 1 tweet dalam Bahasa Indonesia. Maksimal 250 karakter, tanpa hashtag, max 1 emoji, tone deadpan. Hanya tulis tweetnya..."


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


def check_required_env():
    required = ["X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET", "AI_API_KEY"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        print("Missing required environment variables: " + ", ".join(missing))
        sys.exit(1)


def validate_twitter_credentials():
    # Try a lightweight API call to confirm auth works before posting
    try:
        client_x = tweepy.Client(
            consumer_key=X_API_KEY,
            consumer_secret=X_API_SECRET,
            access_token=X_ACCESS_TOKEN,
            access_token_secret=X_ACCESS_SECRET,
        )
        # get_me() should return the authenticated user on success
        me = client_x.get_me()
        if me is None or getattr(me, "data", None) is None:
            print("Twitter credential check failed: client.get_me() returned no user data.")
            sys.exit(1)
        # Success
        return client_x
    except tweepy.errors.Unauthorized:
        print("Authentication failed: Unauthorized. Check your X_API_KEY/X_API_SECRET/X_ACCESS_TOKEN/X_ACCESS_SECRET repository secrets and token permissions.")
        sys.exit(1)
    except Exception as e:
        print("Unexpected error during Twitter credential check:", str(e))
        sys.exit(1)


def post_tweet(text, client_x):
    try:
        response = client_x.create_tweet(text=text)
        # response.data may be a dict-like object
        tweet_id = None
        if response is not None and getattr(response, "data", None) is not None:
            tweet_id = response.data.get("id") if isinstance(response.data, dict) else getattr(response.data, "id", None)
        print("Tweet posted! ID:", tweet_id)
        print("Content:", text)
        return response
    except tweepy.errors.Unauthorized:
        print("Post failed: unauthorized. Verify your API keys and tokens in repository secrets and that the app has write/post permissions.")
        sys.exit(1)
    except Exception as e:
        print("Post failed:", str(e))
        sys.exit(1)


def main():
    check_required_env()
    print("Generating tweet...")
    tweet = generate_tweet()
    print("Generated: " + tweet)

    # Validate credentials and get a client
    client = validate_twitter_credentials()
    post_tweet(tweet, client)


if __name__ == "__main__":
    main()
