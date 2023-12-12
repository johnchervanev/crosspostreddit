import praw
import time
import random
import logging
import os
import configparser
import requests
from logging.handlers import RotatingFileHandler
import sys

# Create a logger instance
logger = logging.getLogger()

# Set up logging with a custom format
logging.basicConfig(
    filename='crosspost_log.txt',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
)

# Add a console handler to print log messages to the terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Add a rotating file handler to manage log files over time
log_file = 'crosspost_log.txt'
max_log_size_bytes = 15 * 1024 * 1024  # 15 MB
backup_count = 5  # Number of backup log files to keep

rotating_file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size_bytes, backupCount=backup_count)
rotating_file_handler.setLevel(logging.INFO)
rotating_file_handler.setFormatter(formatter)
logger.addHandler(rotating_file_handler)

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

# Load configuration from the file
config = configparser.ConfigParser()
try:
    config.read('config.ini')
except configparser.Error as e:
    print(f"Error reading config.ini: {e}")
    sys.exit(1)

# Initialize check_posts_delay_minutes before the loop
check_posts_delay_minutes = config.getint('Delays', 'check_posts_delay_minutes')

# Dictionary to store Reddit instances for each user
reddit_instances = {}

# Function to load Reddit API credentials for a specific user
def load_reddit_credentials(user_section):
    try:
        return (
            config.get(user_section, 'client_id'),
            config.get(user_section, 'client_secret'),
            config.get(user_section, 'username'),
            config.get(user_section, 'password'),
            config.get(user_section, 'user_agent'),
        )
    except configparser.Error as e:
        raise ValueError(f"Error loading credentials for {user_section} from config.ini: {e}")

# Function to check proxy connection
def check_proxy_connection(username, proxies):
    test_url = 'http://www.reddit.com'
    try:
        response = requests.get(test_url, proxies=proxies, timeout=10)
        if response.status_code == 200:
            print(f"Proxy connection is successful to reddit user {username}")
        else:
            print(f"Proxy connection failed for reddit user {username}. Status code: {response.status_code}")
            # Log the error instead of raising SystemExit
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"Proxy connection failed. Status code: {response.status_code}\n")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        # Log the error instead of raising SystemExit
        with open('error_log.txt', 'a') as log_file:
            log_file.write(f"An error occurred during the request: {e}\n")
        print(f"Proxy connection failed for reddit user {username}. An error occurred: {e}")

# Function to fetch new submissions from the source user
def fetch_new_submissions(reddit, user_section):
    global crossposted_submission_ids  # Make sure to use the global set

    # Retrieve source user from the current user section
    source_user = config.get(user_section, 'source_user')

    # Subreddit to check for new submissions
    source_subreddit_to_check = config.get(user_section, 'source_subreddit')

    logger.info(f"Fetching new submissions from source subreddit: {source_subreddit_to_check} by user: {source_user}")

    # Fetch new submissions from the source subreddit
    for submission in reddit.subreddit(source_subreddit_to_check).new(limit=10):  # Adjust the limit as needed
        # Check if the post has not been cross-posted before
        if submission.id not in crossposted_submission_ids and submission.author and submission.author.name == source_user:
            # Process the new submission
            process_submission(reddit, user_section, submission)

    # Add a delay before moving on to the next user
    time.sleep(5)  # Adjust the delay as needed

# Function to process a new submission and perform cross-posting
def process_submission(reddit, user_section, submission):
    global crossposted_submission_ids  # Make sure to use the global set

    # List of destination subreddits
    destination_subreddits = config.get(user_section, 'destination_subreddits').split(',')

    logger.info(f"Processing new submission: {submission.title}")

    # Check the rate limit status before making API requests
    remaining_requests = reddit.auth.limits['remaining']
    reset_timestamp = reddit.auth.limits['reset_timestamp']

    logger.info(f"Remaining requests: {remaining_requests}")
    logger.info(f"Reset timestamp: {reset_timestamp}")

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
            delay_seconds = random.randint(crosspost_delay_min * 60, crosspost_delay_max * 60)
            time.sleep(delay_seconds)

        except praw.exceptions.APIException as api_exception:
            # Handle other API exceptions
            print(f"API Exception: {api_exception}")

            # Log the exception for further analysis
            with open('error_log.txt', 'a') as log_file:
                log_file.write(f"API Exception: {api_exception}\n")

# Loop through each Reddit user and fetch new submissions
for user_section in config.sections():
    if user_section.startswith('RedditUser'):
        print(f"Processing user: {user_section}")

        # Load credentials for the current user
        client_id, client_secret, username, password, user_agent = load_reddit_credentials(user_section)

        # Proxy configuration for the current user
        proxy_url_user = config.get(user_section, 'proxy_url')
        proxies_user = {
            'http': proxy_url_user,
            'https': proxy_url_user,
        }

        print(f"Checking proxy connection for {username}")
        # Check proxy connection for the current user
        check_proxy_connection(username, proxies_user)

        # Load delay options from the configuration
        crosspost_delay_min = config.getint('Delays', 'crosspost_delay_min')
        crosspost_delay_max = config.getint('Delays', 'crosspost_delay_max')
        # Set 'proxies' to the current user's proxies
        proxies = proxies_user

        # Create a Reddit instance without the proxies argument if not already created
        if username not in reddit_instances:
            print(f"Creating Reddit instance for {username}")
            reddit_instances[username] = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                username=username,
                password=password,
                user_agent=user_agent,
                proxies=proxies,
            )

        print(f"Running fetch_new_submissions for {username}")
        # Call the function to fetch new submissions for the current Reddit user
        fetch_new_submissions(reddit_instances[username], user_section)

       

# Log information about finishing the script
logger.info("Script completed.")
