# Email Automation Script

## Description

The Email Automation Script is a Python script that sends emails at random intervals. It is designed for scenarios where
you want to simulate human-like email sending patterns. The current implementation is for a sweepstake contest.

This script utilizes the `smtplib` library for sending emails and incorporates the `python-dotenv` package to manage
environment variables.

## Getting Started

### Prerequisites

- Have a Gmail account with 2-Step Verification enabled. It is recommended to use a separate Gmail account that is not
  your primary account.
- Create an App Password for the script.
  See [Google's documentation](https://support.google.com/accounts/answer/185833?hl=en) for more information
  or [this video](https://youtu.be/g_j6ILT-X0k?t=24&si=ZmYLkSX2zi6fthfY).

### Installation

1. Install Python 3.9.6 from [python.org](https://www.python.org/downloads/) if not already installed.

2. Clone the repository:

   ```bash
   git clone https://github.com/mekdimd/email-automation-script
   ```

3. Navigate to the project root:

   ```bash
   cd email-automation-script
   ```

4. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

5. Activate the Virtual Environment

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

6. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

7. Run the script:

   ```bash
   python3 main.py
   ```

## Configuration

1. Create a `.env` file in the project root and add the necessary environment variables. See the example below:
   ```sh
   # Login info
   DISPLAY_NAME='Bob Smith'
   EMAIL='bobsmith123@gmail.com'
   EMAIL_PASSWORD='abcdefghijklmnop'    # App Password
   ```
2. Edit the config.json file to configure the script. See the example below:
   ```json
    {
      "to_email": "test@gmail.com",
      "email_subject": {
        "list": [
          "Subject 1",
          "Subject 2",
          "Subject 3"
        ]
      },
      "email_body": {
        "list": [
          "First Line",
          "Second Line",
          "Third Line"
        ],
        "shuffle": 1,
        "shuffle_first_line": 0
      },
      "offline_hours": [0, 6],
      "email_break_minutes": [60, 120],
      "burst": {
        "using_burst_algo": 1,
        "burst_frequency_sec": [59, 123],
        "num_emails": [19, 26],
        "long_break_minutes": [180, 480]
      }
    }
   ```
