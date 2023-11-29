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
    seconds = int(seconds)
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


# Prepare email contents (shuffling, randomizing, etc. happens here)
def fetch_email_data():
    global EMAIL_SUBJECT_LIST, EMAIL_BODY_LIST

    email_subject = random.choice(EMAIL_SUBJECT_LIST)

    # Shuffle array (idx 1-end), and join items
    temp = EMAIL_BODY_LIST[1:]
    random.shuffle(temp)
    EMAIL_BODY_LIST[1:] = temp
    email_body = '\n'.join([str(item) for item in EMAIL_BODY_LIST])

    return email_subject, email_body


# Print confirmation that email was sent
def print_email_info(recipient_email, email_count, current_time, next_time):
    time_diff = next_time - current_time
    print(f"Sent #{email_count} to {recipient_email} at {current_time.strftime('%I:%M:%S %p')}")
    print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} (in {format_time(time_diff.total_seconds())})")


# Returns whether a given datetime object is in range (int) [offline_start, offline_end]
def is_within_offline_hours(current_time, offline_start, offline_end):
    offline_start_sec = offline_start * 3600
    offline_end_sec = offline_end * 3600
    time_sec = current_time.hour * 3600 + current_time.minute * 60 + current_time.second

    return (
            (offline_start < offline_end and (offline_start_sec <= time_sec < offline_end_sec)) or
            (offline_start > offline_end and (time_sec >= offline_start_sec or time_sec <= offline_end_sec)) or
            (offline_start == offline_end)  # Offline hours span full day i.e. always offline
    )


# TODO HANDLE DECIMAL OFFLINE_START AND OFFLINE_END
# Returns the next email time to send for
def calculate_next_time(current_time, break_sec, offline_start, offline_end):
    next_time = current_time + timedelta(seconds=break_sec)
    break_time = next_time - current_time

    if is_within_offline_hours(next_time, offline_start, offline_end):
        print(f"> OFFLINE HOURS: {datetime(2023, 11, 24, offline_start, 0, 0).strftime('%I:%M:%S %p')} - {datetime(2023, 11, 24, offline_end, 0, 0).strftime('%I:%M:%S %p')}")
        print(f"> Current Time: {current_time.strftime('%I:%M:%S %p')}")
        print(f"> Next Time: {next_time.strftime('%I:%M:%S %p')}")
        print(f"> break_time = {format_time(break_time.total_seconds())}\n")

        offline_end_sec = offline_end * 3600
        next_time_sec = next_time.hour * 3600 + next_time.minute * 60 + next_time.second
       
        # Handle case when offline hours go past midnight goes into the next day
        # Add 24h if the difference is negative (overflow into the next day)
        sec_till_offline_end = offline_end_sec - next_time_sec
        if sec_till_offline_end < 0:
            sec_till_offline_end += 24 * 3600

        # Update break time (and as a result, next_time)
        break_time += timedelta(seconds=sec_till_offline_end)
        print(f"> {next_time.strftime('%I:%M:%S %p')} is OFFLINE! Add {format_time(sec_till_offline_end)} break, total {format_time(break_time.total_seconds())}")
        next_time += break_time

    return next_time


# Send emails with a delay in the range [min_delay, max_delay] (minutes)
def spaced_interval_algo(min_delay, max_delay, offline_start, offline_end):
    global TO_EMAIL

    email_count = 0    
    try:
        while True:
            email_subject, email_body = fetch_email_data()

            # Send email
            send_email(TO_EMAIL, email_subject, email_body)
            current_time = datetime.now()
            email_count += 1
            
            # Deternmine sleep time for next email
            rand_break = random.randint(min_delay * 60, max_delay * 60)
            next_time = calculate_next_time(current_time, rand_break, offline_start, offline_end)

            # Confirmation that email was sent
            print_email_info(TO_EMAIL, email_count, current_time, next_time)
            
            # Sleep until next email
            sleep_sec = (next_time - current_time).total_seconds()
            sleep(sleep_sec)

    except KeyboardInterrupt:
        print("Email script terminated.")


offline_start, offline_end = [13, 17]

spaced_interval_algo(17, 127, offline_start, offline_end)
