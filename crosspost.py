import praw
import time
import random
import logging
import os
import configparser

# Load configuration from the file
config = configparser.ConfigParser()
config.read('config.ini')

# Reddit API credentials
client_id = config.get('Reddit', 'client_id')
client_secret = config.get('Reddit', 'client_secret')
username = config.get('Reddit', 'username')
password = config.get('Reddit', 'password')
user_agent = config.get('Reddit', 'user_agent')

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# Set up logging
logging.basicConfig(filename='crosspost_log.txt', level=logging.INFO)

# File to store the set of cross-posted submission IDs
id_storage_file = 'crossposted_ids.txt'

# Function to load the set of cross-posted submission IDs from a file
def load_crossposted_submission_ids():
    if os.path.exists(id_storage_file):
        with open(id_storage_file, 'r') as file:
            return set(file.read().splitlines())
    return set()

# Function to save the set of cross-posted submission IDs to a file
def save_crossposted_submission_ids(ids_set):
    with open(id_storage_file, 'w') as file:
        file.write('\n'.join(ids_set))

# Set to store the IDs of cross-posted submissions
crossposted_submission_ids = load_crossposted_submission_ids()

# User whose posts you want to cross-post
source_user = config.get('Crosspost', 'source_user')

# List of destination subreddits
destination_subreddits = config.get('Crosspost', 'destination_subreddits').split(',')

# Subreddit to check for crossposting
source_subreddit_to_crosspost = config.get('Crosspost', 'source_subreddit')

# Function to cross-post new posts from the source user
def crosspost_new_posts():
    global crossposted_submission_ids  # Make sure to use the global set

    # Monitor new posts by the source user
    for submission in reddit.redditor(source_user).stream.submissions():
        # Check if the post is in the specified subreddit and has not been cross-posted before
        if (
            submission.subreddit.display_name == source_subreddit_to_crosspost
            and submission.id not in crossposted_submission_ids
        ):
            # Cross-post the new submission to all destination subreddits
            for dest_subreddit in destination_subreddits:
                try:
                    destination_post = submission.crosspost(subreddit=dest_subreddit, send_replies=False)
                    print(f"Cross-posted successfully to {dest_subreddit}! New post URL: {destination_post.url}")

                    # Add the ID of the cross-posted submission to the set
                    crossposted_submission_ids.add(submission.id)

                    # Save the set of cross-posted submission IDs to a file
                    save_crossposted_submission_ids(crossposted_submission_ids)

                    # Print remaining requests and reset time
                    remaining_requests = int(reddit.auth.limits['remaining'])
                    reset_time = int(reddit.auth.limits['reset_timestamp'])
                    print(f"Remaining requests: {remaining_requests}, Reset time: {reset_time}")

                    # Add a random delay between 1 and 4 minutes after each cross-post
                    delay_seconds = random.randint(60, 240)  # 60-240 seconds = 1-4 minutes
                    time.sleep(delay_seconds)

                except praw.exceptions.APIException as api_exception:
                    # Handle other API exceptions
                    print(f"API Exception: {api_exception}")

                    # Log the exception for further analysis
                    with open('error_log.txt', 'a') as log_file:
                        log_file.write(f"API Exception: {api_exception}\n")
                    break

# Run the function at regular intervals
while True:
    try:
        crosspost_new_posts()
    except Exception as e:
        print(f"An error occurred: {e}")
        logging.error(f"An error occurred: {e}")

    # Add a delay (e.g., 15 minutes) before checking for new posts again
    time.sleep(60)  # 60 seconds = 1 minute