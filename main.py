import random
from time import sleep
from datetime import datetime, timedelta, time

from email_config import EmailConfig


# Format time as a human-readable string
def format_time(seconds) -> str:
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


# Print confirmation that email was sent
def print_email_info(recipient_email: str, email_count: int, current_time: datetime, next_time: datetime) -> None:
    time_diff = next_time - current_time
    print(f"Sent #{email_count} to {recipient_email} at {current_time.strftime('%I:%M:%S %p')}")
    print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} "
          f"(in {format_time(time_diff.total_seconds())})")


# Returns whether a given datetime object is in range (int) [offline_start, offline_end]
def is_within_offline_hours(current_time: datetime, offline_start: int, offline_end: int):
    offline_start_sec = offline_start * 3600
    offline_end_sec = offline_end * 3600
    time_sec = current_time.hour * 3600 + current_time.minute * 60 + current_time.second

    return (
            (offline_start < offline_end and (offline_start_sec <= time_sec < offline_end_sec)) or
            (offline_start > offline_end and (time_sec >= offline_start_sec or time_sec <= offline_end_sec)) or
            (offline_start == offline_end)  # Offline hours span full day i.e. always offline
    )


# Returns the next email time to send for
def calculate_next_time(current_time: datetime, break_sec: int, offline_start: int, offline_end: int) -> datetime:
    next_time = current_time + timedelta(seconds=break_sec)
    break_time = next_time - current_time

    if is_within_offline_hours(next_time, offline_start, offline_end):
        print(f"> OFFLINE HOURS: "
              f"{time(offline_start, 0, 0).strftime('%I:%M:%S %p')} - "
              f"{time(offline_end, 0, 0).strftime('%I:%M:%S %p')}")
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
        print(f"> Add {format_time(sec_till_offline_end)} to get to {time(offline_end, 0, 0).strftime('%I:%M %p')}, "
              f"total = {format_time(break_time.total_seconds())}")
        print(f"> Add initial break {format_time((next_time - current_time).total_seconds())}"
              f" = {format_time((next_time + break_time - current_time).total_seconds())}")
        next_time += break_time

    return next_time


# Send emails with a delay in the range [min_delay, max_delay] (minutes)
def spaced_interval_algo(econfig: EmailConfig) -> None:
    email_count = 0
    try:
        while True:
            # Determine sleep time for next email
            rand_break: int = random.randint(econfig.email_break_minutes_min * 60, econfig.email_break_minutes_max * 60)
            current_time: datetime = datetime.now()
            next_time: datetime = calculate_next_time(current_time,
                                                      rand_break,
                                                      econfig.offline_hr_start,
                                                      econfig.offline_hr_end)

            if not is_within_offline_hours(current_time + timedelta(seconds=rand_break),
                                           econfig.offline_hr_start,
                                           econfig.offline_hr_end):
                # Send email
                econfig.send_email()
                email_count += 1
                print(f"Sent #{email_count} to {econfig.to_email} at {current_time.strftime('%I:%M:%S %p')}")

            # Sleep until next email
            sleep_sec = (next_time - current_time).total_seconds()
            print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} (in {format_time(sleep_sec)})\n")
            sleep(sleep_sec)

    except KeyboardInterrupt:
        print("Email script terminated.")


# Send emails in short bursts (1-5 min apart) and take a longer break in range [break_min, break_max]
def burst_email_algo(econfig: EmailConfig) -> None:
    email_count = 0

    try:
        while True:
            num_burst_emails = random.randint(econfig.burst_num_emails_min, econfig.burst_num_emails_max)
            print(f"BURST ALGORITHM\n\nSending {num_burst_emails} emails in burst...\n")

            for i in range(num_burst_emails):
                # Calculate break time
                burst_break_sec: int = random.randint(econfig.burst_min_freq_sec, econfig.burst_max_freq_sec)
                current_time: datetime = datetime.now()
                next_time: datetime = current_time + timedelta(seconds=burst_break_sec)

                # Sending burst during offline hours, sleep until hours are finished
                if is_within_offline_hours(next_time, econfig.offline_hr_start, econfig.offline_hr_end):
                    burst_resume_time = calculate_next_time(
                        current_time,
                        burst_break_sec,
                        econfig.offline_hr_start,
                        econfig.offline_hr_end)
                    pause_time = (burst_resume_time - current_time).total_seconds()
                    print(f"Scheduled to continue at {burst_resume_time.strftime('%I:%M:%S %p')} "
                          f"(in {format_time(pause_time)})\n")
                    print(f"\tsleeping for {format_time(pause_time)}")
                    sleep(pause_time)

                # Send burst email
                econfig.send_email()
                email_count += 1

                # Update times
                current_time = datetime.now()
                next_time = current_time + timedelta(seconds=burst_break_sec)

                # Print info
                print(f"Sent #{email_count} "
                      f"to {econfig.to_email} "
                      f"at {current_time.strftime('%I:%M:%S %p')}")
                print(f"Next email will be sent at {next_time.strftime('%I:%M:%S %p')} "
                      f"(in {format_time(burst_break_sec)})")
                print(f"{i + 1}/{num_burst_emails} burst emails sent\n")
                sleep(burst_break_sec)

            # Take a longer break
            rand_break = random.randint(econfig.burst_long_break_minutes_min * 60,
                                        econfig.burst_long_break_minutes_max * 60)
            current_time = datetime.now()
            next_time = calculate_next_time(current_time, rand_break, econfig.offline_hr_start, econfig.offline_hr_end)
            long_break_sec = (next_time - current_time).total_seconds()

            # Print details for next email
            print(f"Long break. Next burst at {next_time.strftime('%I:%M:%S %p')} (in {format_time(long_break_sec)})\n")
            sleep(long_break_sec)
    except KeyboardInterrupt:
        print("Email script terminated.")


def main():
    filepath = "config.json"
    email_config_info = EmailConfig(filepath)

    # spaced_interval_algo(email_config_info)
    burst_email_algo(email_config_info)


if __name__ == '__main__':
    main()
