import os
import random
import smtplib
import ssl
from time import sleep
from datetime import datetime, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISPLAY_NAME = os.environ.get("DISPLAY_NAME")   # Optional Display name
FROM_EMAIL = os.environ.get("EMAIL")            # Your email
PASSWORD = os.environ.get("EMAIL_PASSWORD")     # Your (app) password
TO_EMAIL = os.environ.get("TO_EMAIL")           # Recipient email

# List of email subjects
EMAIL_SUBJECT_LIST = [
    'Simplii Debit Mastercard Holiday Sweepstakes entry',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry',
    'Simplii Debit Mastercard Holiday Sweepstakes - entry',
    'Simplii Debit Mastercard Holiday Sweepstakes - Entry',
    'Entry for Simplii Debit Mastercard Holiday Sweepstakes',
    'Simplii Debit Mastercard Holiday Sweepstakes entry - Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes entry - Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes entry - Mekdim Dereje',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry - Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry - Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry - Mekdim Dereje',
    'Simplii Debit Mastercard Holiday Sweepstakes entry: Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes entry: Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes entry: Mekdim Dereje',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry: Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry: Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry: Mekdim Dereje',
    'Simplii Debit Mastercard Holiday Sweepstakes entry for Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes entry for Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes entry for Mekdim Dereje',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry for Mekdim',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry for Mekdim D.',
    'Simplii Debit Mastercard Holiday Sweepstakes Entry for Mekdim Dereje',
    'Mekdim - Simplii Debit Mastercard Holiday Sweepstakes entry',
    'Mekdim D. - Simplii Debit Mastercard Holiday Sweepstakes entry',
    'Mekdim Dereje - Simplii Debit Mastercard Holiday Sweepstakes entry',
    'Mekdim - Simplii Debit Mastercard Holiday Sweepstakes Entry',
    'Mekdim D. - Simplii Debit Mastercard Holiday Sweepstakes Entry',
    'Mekdim Dereje - Simplii Debit Mastercard Holiday Sweepstakes Entry',
]

EMAIL_BODY_LIST = [
    f'Full Name: {os.environ.get("FULL_NAME")}',
    f'Mailing Address: {os.environ.get("MAILING_ADDR")}',
    f'Telephone Number: {os.environ.get("TELEPHONE_NUM")}',
    f'First 6 digits of Simplii Debit Mastercard: {os.environ.get("DIGITS")}',
    f'Email address: {os.environ.get("EMAIL_BODY")}',
]


def send_email(to, subject, body):
    global DISPLAY_NAME, FROM_EMAIL, PASSWORD

    em = EmailMessage()
    em['From'] = f'{DISPLAY_NAME} <{FROM_EMAIL}>'
    em['To'] = to
    em['Subject'] = subject
    em.set_content(body)

    # Extra security
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(FROM_EMAIL, PASSWORD)
        smtp.sendmail(FROM_EMAIL, to, em.as_string())
        smtp.quit()


# Format time as a human-readable string
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        if minutes > 0 and seconds > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{hours}h {minutes}m"
        elif seconds > 0:
            return f"{hours}h {seconds}s"
        else:
            return f"{hours}h"
    elif minutes > 0:
        if seconds > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{minutes}m"
    else:
        return f"{seconds}s"


# Send emails with a delay in the range [min_delay, max_delay]
def spaced_interval_algo(min_delay, max_delay):
    global EMAIL_BODY_LIST, EMAIL_SUBJECT_LIST
    
    try:
        email_count = 0
        while True:
            # Shuffle array (idx 1-end), and join items
            temp = EMAIL_BODY_LIST[1:]
            random.shuffle(temp)
            EMAIL_BODY_LIST[1:] = temp
            email_body = '\n'.join([str(item) for item in EMAIL_BODY_LIST])

            # Send email
            send_email(TO_EMAIL, random.choice(EMAIL_SUBJECT_LIST), email_body)

            # Confirmation that email was sent
            current_time = datetime.now()
            email_count += 1
            print(f"Sent to {TO_EMAIL} at {current_time.strftime('%I:%M:%S %p')} ({email_count} total)")

            # Sleep for a random interval between a specified range
            sleep_time_sec = random.randint(min_delay * 60, max_delay * 60)
            next_time = current_time + timedelta(seconds=sleep_time_sec)

            # Calculate the time difference
            time_diff = next_time - current_time
            time_diff_str = format_time(time_diff.seconds)
            
            print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} (in {time_diff_str})\n")
            sleep(sleep_time_sec)

    except KeyboardInterrupt:
        print("Email script terminated.")


# Send emails in short bursts (1-5 min apart) and take a longer break in range [break_min, break_max]
def burst_email_algo(num_emails_in_burst, break_min, break_max):
    pass


spaced_interval_algo(17, 127) 
