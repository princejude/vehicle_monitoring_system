from datetime import datetime, time

def is_peak_time(start_hour=7, end_hour=19):
    """
    Check if the current time falls within peak hours (default: 07:00 to 19:00).

    :param start_hour: Start hour of the peak time.
    :param end_hour: End hour of the peak time.
    :return: True if current time is within peak hours, otherwise False.
    """
    current_time = datetime.now().time()
    start_time = time(hour=start_hour)
    end_time = time(hour=end_hour)
    return start_time <= current_time <= end_time
