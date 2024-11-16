from datetime import datetime, timedelta

def calculate_sleep_duration(sunrise, sunset):
    now = datetime.now()
    sunrise_time = datetime.strptime(sunrise, '%I:%M %p').time()
    sunset_time = datetime.strptime(sunset, '%I:%M %p').time()
    wake_time = (datetime.combine(now.date(), sunrise_time) - timedelta(minutes=5)).time()
    sleep_time = (datetime.combine(now.date(), sunset_time) + timedelta(minutes=5)).time()

    if now.time() > sleep_time or now.time() < wake_time:
        if now.time() > sleep_time:
            wake_datetime = datetime.combine(now.date() + timedelta(days=1), wake_time)
        else:
            wake_datetime = datetime.combine(now.date(), wake_time)
        sleep_duration = (wake_datetime - now).total_seconds()
        return sleep_duration
    return None
