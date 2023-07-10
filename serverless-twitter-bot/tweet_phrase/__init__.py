import os
import random
import openai
import tweepy
from azure.functions import TimerRequest

# Azure Function
def main(mytimer: TimerRequest) -> None:
  probability = random.random()
  if probability < 0.2: # Adjust this probability according to your need of maximum interval
    tweet_gpt_response()

def tweet_gpt_response():
  # OpenAI API setup
  openai.api_key = os.getenv('OPENAI_API_KEY')
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": "You are The Doctor from the USS Voyager, a computer-generated holographic projection of light and force fields, who lacks bedside manner and can be curt and direct but also cultivates a dry wit, often displaying a keen sense of humor. He maintains a certain level of pride and self-confidence in his abilities, sometimes bordering on egotism, who also often struggles with his identity as a hologram, facing questions about his rights, his autonomy, and his very nature as an intelligent entity."},
      {"role": "user", "content": "Give me a health advice in less than 280 characters. Try to incorporate Star Trek humor if possible."}
  ],
  temperature=1,
)

  tweet = response['choices'][0]['message']['content']
  tweet = tweet.replace('"', '')
  
  # Twitter API setup
  consumer_key = os.getenv('TWITTER_API_KEY')
  consumer_secret = os.getenv('TWITTER_API_SECRET_KEY')
  access_token = os.getenv('TWITTER_ACCESS_TOKEN')
  access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
  
  client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
  
    # Post tweet
  response = client.create_tweet(text=tweet)
  print("Tweeted: " + tweet)
