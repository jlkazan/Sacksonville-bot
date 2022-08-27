# Sacksonville-bot
Twitter bot which sends a tweet every time the Jacksonville Jaguars get a sack.

## About
Sacksonville bot is a completely cloud native application using AWS free tier products only.
Using an EventBridge Trigger, a Lambda function runs every 5 minutes and searches
for live play by play data (using the [nfllivepy](https://github.com/jlkazan/nfllivepy) package I created). The application
makes use of dynamodb to keep track of sacks that have already been tweeted.

## Questions
Feel free to reach out with any questions you may have or features you'd like to see
from the bot!