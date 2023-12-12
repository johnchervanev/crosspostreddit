# Reddit Cross-Posting Script

## Overview

This Python script utilizes the PRAW (Python Reddit API Wrapper) library to cross-post submissions from a source subreddit to multiple destination subreddits. The script is designed to work with multiple Reddit users, each specified in the `config.ini` file.

## Setup Instructions

### Step 1: Set Up Environment

1. **Python Installation:**
   - Ensure you have Python 3.x installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Virtual Environment (Optional but recommended):**
   - Create a virtual environment to isolate dependencies:
     ```bash
     python3 -m venv venv
     source venv/bin/activate   # On Windows, use "venv\Scripts\activate"
     ```

### Step 2: Install Dependencies

3. **Install Required Packages:**
   - Install the necessary Python packages using pip:
     ```bash
     pip install praw requests
     ```

### Step 3: Reddit Developer Account and API Credentials

4. **Create Reddit Developer Account:**
   - Go to [Reddit's App Preferences](https://www.reddit.com/prefs/apps).
   - Scroll down to the "Developed Applications" section and click on the "Create App" button.

5. **Fill Out the Form:**
   - Choose the script type as "script."
   - Set the name and description as per your preference.
   - Set the "about url" and "permissions" to your preference.
   - Enter "http://localhost:8080" as the "redirect uri."

6. **Retrieve API Credentials:**
   - After creating the app, you will find your `client_id` and `client_secret` on the app details page. Note these down; you will need them for configuration.

### Step 4: Configure Git and Clone Repository

7. **Install Git (if not installed):**
   - Download and install Git from [git-scm.com](https://git-scm.com/downloads).

8. **Configure Git:**
   - Set up your Git username and email:
     ```bash
     git config --global user.name "Your Name"
     git config --global user.email "your.email@example.com"
     ```

9. **Clone the Repository:**
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/yourusername/repo.git
     cd repo
     ```

### Step 5: Configuration

10. **Edit Config File:**
    - Open the `config.ini` file and fill in the required information:
      - Set `client_id`, `client_secret`, `username`, `password`, `user_agent` for each Reddit user.
      - Specify the source and destination subreddits, proxy settings, and delays.

### Step 6: Run the Script

11. **Run the Script:**
    - Execute the Python script:
      ```bash
      python script_name.py
      ```
      Replace `script_name.py` with the actual name of your Python script.

12. **Observe Output:**
    - The script will log information to the console and create log files (`crosspost_log.txt`, `error_log.txt`) for reference.

## Default Precautions

- **Rate Limiting:**
  - Be aware of Reddit API rate limits. The script includes basic rate limit checking, but avoid excessive requests to prevent temporary restrictions.

- **Proxy Usage:**
  - If using proxies, ensure they are reliable and properly configured. Check the console and `error_log.txt` for proxy-related issues.

- **Script Adjustments:**
  - Adjust script settings cautiously, considering Reddit's policies and the communities involved.

## Usage Clauses

- **Respect Reddit's Policies:**
  - Ensure compliance with [Reddit's API Terms](https://www.redditinc.com/policies/data-api-terms).

- **Community Guidelines:**
  - Follow the guidelines of the subreddits involved in cross-posting.

- **Account Safety:**
  - Keep API credentials secure. Do not share sensitive information.

- **Logging and Monitoring:**
  - Monitor script outputs and logs regularly for any unusual activity or errors.

- **Legal Compliance:**
  - Ensure your activities comply with applicable laws and regulations.

Congratulations! You've successfully set up and run the Reddit cross-posting script. Adjust configurations as needed for your specific use case.
