# crosspostreddit
Reddit Cross-Posting Bot

This Python script is a simple Reddit cross-posting bot built using the PRAW (Python Reddit API Wrapper) library. The bot monitors new posts made by a specified Reddit user in a designated subreddit and automatically cross-posts those submissions to a list of destination subreddits.

Features:

Real-Time Monitoring: The script continuously checks for new posts by a specified Reddit user.

Subreddit Filter: Cross-posts are initiated only if the new post is in a specific source subreddit.

Cross-Posting: The script cross-posts the identified submissions to a predefined list of destination subreddits.

Delay between Cross-Posts: A 5-minute delay is introduced between each cross-post to adhere to Reddit API usage policies.

Instructions:

Configure API Credentials: Provide your Reddit API credentials, including client ID, client secret, username, and password.

Define User and Subreddit Parameters: Specify the target Reddit user, the subreddit to monitor for new posts, and the list of destination subreddits.

Run the Script: Execute the script, and it will continuously monitor and cross-post new submissions as per the defined criteria.
