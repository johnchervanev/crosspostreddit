# crosspostreddit

# Reddit Cross-Posting Bot

## Overview

Automated Reddit cross-posting bot written in Python using PRAW, designed to monitor a specified user's new posts in a source subreddit and cross-post them to a list of destination subreddits with a 5-minute delay between each cross-post.

## Setup Instructions

### 1. Set Up Python Environment

#### 1.1 Install Python

If you don't have Python installed, download and install it from the [official Python website](https://www.python.org/downloads/). Make sure to add Python to your system's PATH during installation.

#### 1.2 Install PIP

PIP is the package installer for Python. You likely have it installed with Python, but you can check by running:

```bash
pip --version
```

1.3 Install PRAW
PRAW is the Python Reddit API Wrapper. Install it using:

```bash
pip install praw
```
2. Create Reddit App
2.1 Create a Reddit Account
If you don't have a Reddit account, create one here.

2.2 Create a Reddit Developer App
Go to Reddit Preferences > Apps.
Scroll down to the "Developed Applications" section.
Click on "Create App" or "Create Another App."
Choose "script" as the app type.
Enter a name, description, and about-url (can be any valid URL).
Set the permissions to "read" (required for reading posts).
Enter a random string as the redirect URI (e.g., http://localhost:8080).
Click "Create app."
2.3 Retrieve API Credentials
After creating the app, note down the client ID (under the app name) and the client secret (in the app's details).

3. Configure the Script
3.1 Download the Script
Copy the cross-posting script provided.

3.2 Edit the Script
Open the script in a text editor and replace placeholders with your values:

'example_user' with the Reddit username to monitor.

'source_subreddit' with the subreddit to monitor.

['destination_subreddit1', 'destination_subreddit2', '...'] with the list of destination subreddits.

'your_client_id', 'your_client_secret', 'your_username', and 'your_password' with values from the Reddit app.

4. Run the Script
4.1 Run the Script
Open a terminal/command prompt, navigate to the script's directory, and run:

```bash
python script_name.py
```
Replace script_name.py with your script's filename.

4.2 Observe Output
The script should start monitoring for new posts and print messages when it cross-posts. Check for errors or exceptions in the terminal.

