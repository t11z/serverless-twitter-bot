import os
import random
import openai
import tweepy
from azure.functions import TimerRequest

# Azure Function
def main(mytimer: TimerRequest) -> None:
  probability = random.random()
  if probability < float(os.getenv('PROBABILITY')) or 0.2:
    tweet_gpt_response()

def tweet_gpt_response():
  # OpenAI API setup
  openai.api_key = os.getenv('OPENAI_API_KEY')
  openai_system_prompt = os.getenv('OPENAI_SYSTEM_ROLE_MESSAGE')
  openai_user_prompt = os.getenv('OPENAI_USER_ROLE_MESSAGE')
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
      {"role": "system", "content": openai_system_prompt },
      {"role": "user", "content": openai_user_prompt }
  ],
  temperature = float(os.getenv('OPENAI_TEMPERATURE')) or 1,
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
