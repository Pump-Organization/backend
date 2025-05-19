import csv
from services.analytics_service import AnalyticsService


def append_dau(date):
    """get DAU from database then append to a CSV file"""
    analytics_service = AnalyticsService()

    # Get the daily active users count for the given date
    dau_count = analytics_service.get_daily_active_users(date)

    # Append the DAU count to a CSV file
    with open("analytics/dau.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, dau_count])

    print(f"Appended DAU for {date}: {dau_count}")


if __name__ == "__main__":
    from datetime import datetime, timedelta

    # Define start and end dates
    start_date = datetime(2025, 4, 28)
    end_date = datetime(2025, 5, 3)

    # Generate all dates in the range
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        append_dau(date_str)
        current_date += timedelta(days=1)
