from os import getenv

import boto3
from dotenv import load_dotenv
import pandas as pd
import tweepy
from nfllivepy.requester.pbp_requester import PBPRequester

load_dotenv()
dynamo = boto3.client("dynamodb", region_name="us-east-1")
TABLE_NAME = "nfl_data"


def run_bot(event, context):
    """
    Lambda handler for running the bot
    :param event: The event passed in from AWS lambda
    :param context: The context passed in from AWS lambda
    :return: Nothing
    """
    requester = PBPRequester()
    pbp = requester.get_live_pbp_for_team("JAX")

    # Exit if there is no pbp data or no sacks
    if pbp is None or len(pbp.index) == 0:
        return {"result": "No new plays"}

    # Filter sacks by the Jaguars (not when they have possession)
    sacks = pbp[(pbp['play_type'] == "Sack") & (pbp['posteam'] != "JAX")]
    if len(sacks) == 0:
        return {"result": "No new sacks"}

    for _, sack in sacks.iterrows():
        if not play_exists_in_db(sack['play_id']):
            add_play_to_db(sack)
            tweet_play(sack)

    return {"result": "New sacks added!"}

def add_play_to_db(play: pd.Series):
    """
    Add the play to the data base
    :param play: The play as a 1 row series
    :return:
    """
    print(f"Adding play {play['play_id']} to data base")
    dynamo.put_item(TableName=TABLE_NAME, Item={column: {"S": str(play[column])} for column in play.keys()})


def play_exists_in_db(play_id: int) -> bool:
    """
    Checks whether a play with the given play_id already exists in the database
    :param play_id: The play id number
    :return: Whether or not the play is in the database
    """
    play = dynamo.get_item(TableName=TABLE_NAME, Key={"play_id": {"S": play_id}})

    return 'Item' in play


def tweet_play(play: pd.Series):
    """
    Tweet out the play
    :param play: The play as a 1 row series
    :return: Nothing
    """
    # Authenticate to Twitter
    client = tweepy.Client(
        consumer_key=getenv("API_KEY"),
        consumer_secret=getenv("API_KEY_SECRET"),
        access_token=getenv("ACCESS_TOKEN"),
        access_token_secret=getenv("ACCESS_TOKEN_SECRET")
    )

    # Create a tweet
    client.create_tweet(text=f"Sacksonville is back! {play['play_description_short']}.")
