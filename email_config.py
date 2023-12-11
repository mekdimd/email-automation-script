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

            # Validate and set to_email
            self.to_email = data.get("to_email", "")
            if not self.to_email:
                raise ValueError("Invalid or missing 'to_email' in the configuration.")

            # Validate and set email_subject_list
            self.email_subject_list = data.get("email_subject", {}).get("list", [])
            if not self.email_subject_list or not all(isinstance(subj, str) for subj in self.email_subject_list):
                raise ValueError("Invalid or missing 'email_subject.list' in the configuration.")

            # Validate and set email_body_list, email_body_shuffle, and email_body_shuffle_first
            email_body = data.get("email_body", {})
            self.email_body_list = email_body.get("list", [])
            if not self.email_body_list or not all(isinstance(line, str) for line in self.email_body_list):
                raise ValueError("Invalid or missing 'email_body.list' in the configuration.")
            self.email_body_shuffle = bool(email_body.get("shuffle", False))
            self.email_body_shuffle_first = bool(email_body.get("shuffle_first_item", False))

            # Validate and set offline_hr_start and offline_hr_end
            offline_hours = data.get("offline_hours", [])
            if len(offline_hours) != 2 or not all(isinstance(hr, int) for hr in offline_hours):
                raise ValueError("Invalid or missing 'offline_hours' in the configuration.")
            self.offline_hr_start, self.offline_hr_end = offline_hours
            if not (0 <= self.offline_hr_start <= 23 and 0 <= self.offline_hr_end <= 23):
                raise ValueError("Invalid values for 'offline_hours'. Hours should be in the range [0, 23].")
            if self.offline_hr_start == self.offline_hr_end:
                raise ValueError("'offline_hours' should have different start and end times.")

            # Validate and set email_break_minutes_min and email_break_minutes_max
            email_break_minutes = data.get("email_break_minutes", [])
            if len(email_break_minutes) != 2 or not all(isinstance(minutes, int) for minutes in email_break_minutes):
                raise ValueError("Invalid or missing 'email_break_minutes' in the configuration.")
            self.email_break_minutes_min, self.email_break_minutes_max = email_break_minutes
            if not (0 <= self.email_break_minutes_min <= self.email_break_minutes_max):
                raise ValueError("Invalid values for 'email_break_minutes'. Minutes should be non-negative.")

            # Validate and set Burst Algorithm parameters
            burst_data = data.get("burst", {})
            self.using_burst_algo = bool(burst_data.get("using_burst_algo", False))

            # Validate and set burst_min_freq_sec and burst_max_freq_sec
            burst_frequency_sec = burst_data.get("burst_frequency_sec", [])
            if len(burst_frequency_sec) != 2 or not all(isinstance(sec, int) for sec in burst_frequency_sec):
                raise ValueError("Invalid or missing 'burst.burst_frequency_sec' in the configuration.")
            self.burst_min_freq_sec, self.burst_max_freq_sec = burst_frequency_sec
            if not (0 <= self.burst_min_freq_sec <= self.burst_max_freq_sec):
                raise ValueError("Invalid values for 'burst.burst_frequency_sec'. Seconds should be non-negative.")
            if self.burst_min_freq_sec > self.burst_max_freq_sec:
                raise ValueError("Invalid values for 'burst.burst_frequency_sec'. "
                                 "Minimum frequency should be less than or equal to maximum frequency.")

            # Validate and set burst_num_emails_min and burst_num_emails_max
            burst_num_emails = burst_data.get("num_emails", [])
            if len(burst_num_emails) != 2 or not all(isinstance(num, int) for num in burst_num_emails):
                raise ValueError("Invalid or missing 'burst.num_emails' in the configuration.")
            self.burst_num_emails_min, self.burst_num_emails_max = burst_num_emails
            if self.burst_num_emails_min > self.burst_num_emails_max:
                raise ValueError("Invalid values for 'burst.num_emails'. "
                                 "Minimum number of emails should be less than or equal to maximum number.")

            # Validate and set burst_long_break_minutes_min and burst_long_break_minutes_max
            burst_long_break_minutes = burst_data.get("long_break_minutes", [])
            if len(burst_long_break_minutes) != 2 or not all(
                    isinstance(minutes, int) for minutes in burst_long_break_minutes
            ):
                raise ValueError("Invalid or missing 'burst.long_break_minutes' in the configuration.")
            self.burst_long_break_minutes_min, self.burst_long_break_minutes_max = burst_long_break_minutes
            if not (0 <= self.burst_long_break_minutes_min <= self.burst_long_break_minutes_max):
                raise ValueError("Invalid values for 'burst.long_break_minutes'. Minutes should be non-negative.")
            if self.burst_long_break_minutes_min > self.burst_long_break_minutes_max:
                raise ValueError("Invalid values for 'burst.long_break_minutes'. "
                                 "Minimum long break minutes should be less than or equal to maximum.")

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
