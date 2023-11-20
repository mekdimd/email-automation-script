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

1. Create a `.env` file in the project root.
2. Add the necessary environment variables. See the example below:

   ```sh
   # Login info
   DISPLAY_NAME='Bob Smith'
   EMAIL='bobsmith123@gmail.com'
   EMAIL_PASSWORD='abcdefghijklmnop'    # App Password

   TO_EMAIL='alicesmith@gmail.com'

   # Email Body
   FULL_NAME='Bob Smith'
   MAILING_ADDR='123 Main St, Vancouver, BC, V1V 1V1'
   TELEPHONE_NUM='604-123-4567'
   DIGITS='123456'
   EMAIL_BODY='bobsmith123@gmail.com'
   ```
