#!/usr/bin/env bash
python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt #Use this to get cleaned tweets
python ./src/average_degree.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt #Use this to run the degree calculation file