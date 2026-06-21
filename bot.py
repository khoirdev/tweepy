import os
import tweepy
from google import genai
import random

# === CONFIG ===
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
X_API_KEY = os.environ["X_API_KEY"]
X_API_SECRET = os.environ["X_API_SECRET"]
X_ACCESS_TOKEN = os.environ["X_ACCESS_TOKEN"]
X_ACCESS_SECRET = os.environ["X_ACCESS_SECRET"]

# === GEMINI SETUP ===
client_ai = genai.Client(api_key=GEMINI_API_KEY)

# === PROMPT THEMES ===
themes = [
    "kehidupan anak kos yang chaos tapi tetap optimis",
    "drama kerja remote yang absurd",
    "overthinking tengah malam soal hal sepele",
    "hubungan manusia dengan algoritma media sosial",
    "pengalaman naik transportasi umum Indonesia",
    "budaya rebahan dan produktivitas palsu",
    "dilema antara hemat dan jajan",
    "toxic positivity yang tidak disadari",
    "drama grup chat keluarga",
    "ekspektasi vs realita kerja setelah lulus kuliah",
]

SYSTEM_PROMPT = """Kamu adalah akun Twitter/X humor Indonesia yang absurd dan sarkastik.
Gaya kamu: singkat, nyelekit, relatable, kadang existential, tidak menggurui.
Tulis 1 tweet humor dalam Bahasa Indonesia.
Aturan:
- Maksimal 250 karakter
- Tidak pakai hashtag
- Tidak pakai emoji berlebihan (max 1)
- Tidak menjelaskan lelucon
- Tone: absurd, sarkastik, atau deadpan
- Hanya tulis tweet-nya saja, tanpa keterangan tambahan"""

def generate_tweet():
    theme = random.choice(themes)
    prompt = f"{SYSTEM_PROMPT}\n\nTema hari ini: {theme}"
    response = client_ai.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
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
    print(f"✅ Tweet posted! ID: {response.data['id']}")
    print(f"📝 Content: {text}")
    return response

def main():
    print("🤖 Generating tweet...")
    tweet = generate_tweet()
    print(f"📝 Generated: {tweet}")
    post_tweet(tweet)

if __name__ == "__main__":
    main()
- Tidak pakai emoji berlebihan (max 1)
- Tidak menjelaskan lelucon
- Tone: absurd, sarkastik, atau deadpan
- Hanya tulis tweet-nya saja, tanpa keterangan tambahan"""

def generate_tweet():
    theme = random.choice(themes)
    prompt = f"{SYSTEM_PROMPT}\n\nTema hari ini: {theme}"
    response = model.generate_content(prompt)
    tweet = response.text.strip()
    # Pastikan tidak melebihi 280 karakter
    if len(tweet) > 280:
        tweet = tweet[:277] + "..."
    return tweet

def post_tweet(text):
    client = tweepy.Client(
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_SECRET,
    )
    response = client.create_tweet(text=text)
    print(f"✅ Tweet posted! ID: {response.data['id']}")
    print(f"📝 Content: {text}")
    return response

def main():
    print("🤖 Generating tweet...")
    tweet = generate_tweet()
    print(f"📝 Generated: {tweet}")
    post_tweet(tweet)

if __name__ == "__main__":
    main()
  
