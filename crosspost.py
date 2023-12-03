import praw
import time

# Reddit API credentials
client_id = 'your_client_id'
client_secret = 'your_client_secret'
username = 'your_username'
password = 'your_password'  # Replace 'your_password' with your actual Reddit password
user_agent = 'your_user_agent'

# Create a Reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

# User whose posts you want to cross-post
source_user = 'source_username'  # Replace 'example_user' with the actual Reddit username

# List of destination subreddits
destination_subreddits = ['destination_subreddit1', 'destination_subreddit2']

# Subreddit to check for crossposting
source_subreddit_to_crosspost = 'source_subreddit_to_crosspost'  # Replace with the subreddit name

# Function to cross-post new posts from the source user
def crosspost_new_posts():
    # Monitor new posts by the source user
    for submission in reddit.redditor(source_user).stream.submissions():
        # Check if the post is in the specified subreddit
        if submission.subreddit.display_name == source_subreddit_to_crosspost:
            # Cross-post the new submission to all destination subreddits
            for dest_subreddit in destination_subreddits:
                try:
                    destination_post = submission.crosspost(subreddit=dest_subreddit, send_replies=False)
                    print(f"Cross-posted successfully to {dest_subreddit}! New post URL: {destination_post.url}")

                    # Add a delay of 5 minutes before cross-posting the next submission
                    time.sleep(300)  # 300 seconds = 5 minutes

                except praw.exceptions.APIException as api_exception:
                    # Handle other API exceptions
                    print(f"API Exception: {api_exception}")
                    break

# Run the function at regular intervals
while True:
    try:
        crosspost_new_posts()
    except Exception as e:
        print(f"An error occurred: {e}")

    # Add a delay (e.g., 15 minutes) before checking for new posts again
    time.sleep(60)  # 60 seconds = 1 minute
