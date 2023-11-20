import os
import random
import smtplib
import ssl
import time
from email.message import EmailMessage
from time import sleep, strftime, localtime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get email info
DISPLAY_NAME = os.environ.get('DISPLAY_NAME')  # Optional Display name
FROM_EMAIL = os.environ.get("EMAIL")  # Your email
PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Your (app) password
TO_EMAIL = os.environ.get("TO_EMAIL")  # Recipient email

# Modify email subjects
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


def run_send_emails():
    global EMAIL_BODY_LIST, EMAIL_SUBJECT_LIST
    try:
        email_count = 0

        while True:
            # Shuffle array (idx 1-end), and join items
            temp = EMAIL_BODY_LIST[1:]
            random.shuffle(temp)
            EMAIL_BODY_LIST[1:] = temp
            email_body = '\n'.join([str(item) for item in EMAIL_BODY_LIST])

            send_email(TO_EMAIL, random.choice(EMAIL_SUBJECT_LIST), email_body)

            # Confirmation that email was sent
            current_time = strftime("%I:%M:%S%p", localtime())
            email_count += 1
            print(f"Sent to {TO_EMAIL} at {current_time} ({email_count} total)")

            # Sleep for a random interval between a specified range
            lower_bound_min = 30
            upper_bound_min = 90
            sleep_time = random.uniform(lower_bound_min * 60, upper_bound_min * 60)

            print(f"Next email will be sent at {strftime('%I:%M:%S %p', localtime(time.time() + sleep_time))}\n")
            sleep(sleep_time)

    except KeyboardInterrupt:
        print("Email script terminated.")


run_send_emails()
