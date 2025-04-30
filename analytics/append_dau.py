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
    for i in range(22, 28):
        date = f"2025-04-{i}"
        append_dau(date)
