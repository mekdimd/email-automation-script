# email_config.py
import os
import json
import random

from dotenv import load_dotenv
from email.message import EmailMessage
import smtplib
import ssl


class EmailConfig:
    def __init__(self, json_path):
        # Load environment variables from .env file
        load_dotenv()
        self.DISPLAY_NAME = os.environ.get("DISPLAY_NAME")  # Optional Display name
        self.FROM_EMAIL = os.environ.get("EMAIL")  # Your email
        self.PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Your (app) password

        with open(json_path, 'r') as file:
            data = json.load(file)
            self.to_email = data["to_email"]

            # Email subject
            self.email_subject_list = data["email_subject"]["list"]

            # Email body
            self.email_body_list = data["email_body"]["list"]
            self.email_body_shuffle = data["email_body"]["shuffle"]
            self.email_body_shuffle_first = data["email_body"]["shuffle_first_item"]

            # Time related
            self.offline_hr_start = data["offline_hours"][0]
            self.offline_hr_end = data["offline_hours"][1]
            self.email_break_minutes_min = data["email_break_minutes"][0]
            self.email_break_minutes_max = data["email_break_minutes"][1]

            # Burst Algorithm
            self.using_burst_algo = data["burst"]["using_burst_algo"]
            self.burst_min_freq_sec = data["burst"]["burst_frequency_sec"][0]
            self.burst_max_freq_sec = data["burst"]["burst_frequency_sec"][1]
            self.burst_num_emails_min = data["burst"]["num_emails"][0]
            self.burst_num_emails_max = data["burst"]["num_emails"][1]
            self.burst_long_break_minutes_min = data["burst"]["long_break_minutes"][0]
            self.burst_long_break_minutes_max = data["burst"]["long_break_minutes"][1]

    def is_using_burst_algo(self):
        return self.using_burst_algo

    # Return Random email subject subject
    def get_subject(self):
        return random.choice(self.email_subject_list)

    # Return body list
    def get_body_str(self):
        result_list = self.email_body_list.copy()

        # Shuffle array
        if self.email_body_shuffle:
            # Shuffle everything but the first item
            if not self.email_body_shuffle_first:
                temp = result_list[1:]
                random.shuffle(temp)
                result_list[1:] = temp

            # Shuffle everything
            else:
                random.shuffle(result_list)

        return '\n'.join([str(item) for item in result_list])

    def send_email(self):
        em = EmailMessage()
        em['From'] = f'{self.DISPLAY_NAME} <{self.FROM_EMAIL}>'
        em['To'] = self.to_email
        em['Subject'] = self.get_subject()
        em.set_content(self.get_body_str())

        # Extra security
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.FROM_EMAIL, self.PASSWORD)
            smtp.sendmail(self.FROM_EMAIL, self.to_email, em.as_string())
            smtp.quit()

    # TODO JSON FILE CHECKS
    def validate_data(self):
        pass

    def __str__(self):
        return (
            f"To Email: {self.to_email}\n"
            f"Email Subject List: {self.email_subject_list}\n"
            f"Email Body List: {self.email_body_list}\n"
            f"Email Body Shuffle: {self.email_body_shuffle}\n"
            f"Email Body Shuffle First: {self.email_body_shuffle_first}\n"
            f"Offline Hours: {self.offline_hr_start} - {self.offline_hr_end}\n"
            f"Email Break Minutes Min: {self.email_break_minutes_min}\n"
            f"Email Break Minutes Max: {self.email_break_minutes_max}\n"
            f"Using Burst Algorithm: {self.using_burst_algo}\n"
            f"Burst Min Frequency (sec): {self.burst_min_freq_sec}\n"
            f"Burst Max Frequency (sec): {self.burst_max_freq_sec}\n"
            f"Burst Num Emails Min: {self.burst_num_emails_min}\n"
            f"Burst Num Emails Max: {self.burst_num_emails_max}\n"
            f"Burst Long Break Minutes Min: {self.burst_long_break_minutes_min}\n"
            f"Burst Long Break Minutes Max: {self.burst_long_break_minutes_max}\n"
        )


config = "config.json"
obj = EmailConfig(config)
print(obj)
