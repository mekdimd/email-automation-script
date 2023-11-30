import os
import random
import smtplib
import ssl
from time import sleep
from datetime import datetime, timedelta, time
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


# # Print confirmation that email was sent
# def print_email_info(recipient_email, email_count, current_time, next_time):
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
        print(f"> OFFLINE HOURS: {time(offline_start, 0, 0).strftime('%I:%M:%S %p')} - {time(offline_end, 0, 0).strftime('%I:%M:%S %p')}")
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
        print(f"> {next_time.strftime('%I:%M:%S %p')} is OFFLINE!")
        print(f"> Add {format_time(sec_till_offline_end)} to get to {time(offline_end, 0, 0).strftime('%I:%M %p')}, total = {format_time(break_time.total_seconds())}")
        print(f"> Add initial break {format_time((next_time - current_time).total_seconds())} = {format_time((next_time + break_time - current_time).total_seconds())}")
        next_time += break_time

    return next_time


# Send emails with a delay in the range [min_delay, max_delay] (minutes)
def spaced_interval_algo(min_delay, max_delay, offline_start, offline_end):
    global TO_EMAIL

    email_count = 0    
    try:
        while True:            
            # Determine sleep time for next email
            rand_break = random.randint(min_delay * 60, max_delay * 60)
            current_time = datetime.now()
            next_time = calculate_next_time(current_time, rand_break, offline_start, offline_end)

            if not is_within_offline_hours(current_time + timedelta(seconds=rand_break), offline_start, offline_end):
                # Send email
                email_subject, email_body = fetch_email_data()
                send_email(TO_EMAIL, email_subject, email_body)
                email_count += 1
                print(f"Sent #{email_count} to {TO_EMAIL} at {current_time.strftime('%I:%M:%S %p')}")

            # Sleep until next email
            sleep_sec = (next_time - current_time).total_seconds()
            print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} (in {format_time(sleep_sec)})\n")
            sleep(sleep_sec)

    except KeyboardInterrupt:
        print("Email script terminated.")


# Send emails in short bursts (1-5 min apart) and take a longer break in range [break_min, break_max]
def burst_email_algo(num_burst_min, num_burst_max, long_break_min, long_break_max):
    MIN_BURST_FREQ, MAX_BURST_FREQ = [59, 123]
    OFFLINE_START, OFFLINE_END = [0, 6]
    # OFFLINE_START, OFFLINE_END = [10, 3]
    email_count = 0

    if OFFLINE_START == OFFLINE_END:
        raise Exception(f"Offline start hour can not have same start and end hour [{OFFLINE_START},{OFFLINE_END}]")

    try:
        while True:
            num_burst_emails = random.randint(num_burst_min, num_burst_max)
            print(f"BURST ALGORITHM\n\nSending {num_burst_emails} emails in burst...\n")

            for i in range(num_burst_emails):
                # Calculate break time
                burst_break_sec = random.randint(MIN_BURST_FREQ, MAX_BURST_FREQ)
                current_time = datetime.now()
                next_time = current_time + timedelta(seconds=burst_break_sec)

                # Sending burst during offline hours, sleep until hours are finished
                if is_within_offline_hours(next_time, OFFLINE_START, OFFLINE_END):
                    burst_resume_time = calculate_next_time(current_time, burst_break_sec, OFFLINE_START, OFFLINE_END)
                    pause_time = (burst_resume_time - current_time).total_seconds()
                    print(f"Scheduled to continue at {burst_resume_time.strftime('%I:%M:%S %p')} (in {format_time(pause_time)})\n")
                    print(f"\tsleeping for {format_time(pause_time)}")
                    sleep(pause_time)

                # Send burst email
                email_subject, email_body = fetch_email_data()
                send_email(TO_EMAIL, email_subject, email_body)
                email_count += 1
                
                # Update times
                current_time = datetime.now()
                next_time = current_time + timedelta(seconds=burst_break_sec)                

                # Print info
                print(f"Sent #{email_count} to {TO_EMAIL} at {current_time.strftime('%I:%M:%S %p')}")
                print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} (in {format_time(burst_break_sec)})")
                print(f"{i+1}/{num_burst_emails} burst emails sent\n")
                # print(f"\tsleeping for {format_time(burst_break_sec)}")
                sleep(burst_break_sec)

            # Take a longer break
            rand_break = random.randint(long_break_min * 60, long_break_max * 60)
            current_time = datetime.now()
            next_time = calculate_next_time(current_time, rand_break, OFFLINE_START, OFFLINE_END)
            long_break_sec = (next_time - current_time).total_seconds()

            # Print details for next email
            print(f"Long break. Next burst at {next_time.strftime('%I:%M:%S %p')} (in {format_time(long_break_sec)})\n")
            # print(f"\tsleeping for {format_time(long_break_sec)}")
            sleep(long_break_sec)
    except KeyboardInterrupt:
        print("Email script terminated.")


offline_start, offline_end = [0, 6]
min_burst, max_burst = [19, 26]
break_min, break_max = [180, 360]

# spaced_interval_algo(17, 127, offline_start, offline_end)
burst_email_algo(min_burst, max_burst, break_min, break_max)
