from datetime import datetime


def to_timestmp(time_str: str) -> datetime.timestamp:
    dates, times = time_str.split()[0], time_str.split()[1]


def make_time_range(start: str, end: str) -> list:
    start_month = start.split("-")[1]
    start_year = start.split("-")[0]
    end_month = end.split("-")[1]
    end_year = end.split("-")[0]

    count_months = (
        (int(end_year) - int(start_year)) * 12 + (int(end_month) - int(start_month)) + 1
    )
    if count_months <= 0:
        print("ERROR: end must be > start")
        return 0
    print(count_months)

    time_range = []
    month_now = int(start_month)
    year_now = int(start_year)

    for i in range(count_months):
        time_range.append(
            str(year_now) + "-" + "0" * (2 - len(str(month_now))) + str(month_now)
        )
        if month_now == 12:
            month_now = 1
            year_now += 1
        else:
            month_now += 1
    return time_range
