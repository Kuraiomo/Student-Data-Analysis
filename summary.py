import json

def generate_leave_summary(data):
    anomalies = data["anomalies"]
    statistics = data["basic_statistics"]
    events = data["significant_events"]
    patterns = data["temporal_patterns"]

    summary = []

    # Weekend Extension Analysis
    if patterns["daily_distribution"]["Friday"] > 70 and patterns["daily_distribution"]["Saturday"] > 75:
        summary.append("Students frequently take leave on Fridays and Saturdays, likely to extend their weekends for travel or relaxation.")

    # Monthly Leave Trends
    high_leave_months = {month: count for month, count in patterns["monthly_trend"].items() if count > 100}
    if high_leave_months:
        months = ", ".join(high_leave_months.keys())
        summary.append(f"Significant leave trends were observed in {months}, possibly due to holidays, academic breaks, or personal travel.")

    # Anomaly Detection & Patterns
    if max(anomalies["values"]) > anomalies["threshold"]:
        anomaly_start = anomalies["anomalous_dates"][0]
        anomaly_end = anomalies["anomalous_dates"][-1]
        summary.append(f"An unusual spike in leaves was recorded from {anomaly_start} to {anomaly_end}, suggesting events like exams, festivals, or urgent travel needs.")

    # Exam or Festival Leave Hypothesis
    if statistics["max_consecutive_days"] > 30:
        summary.append("Extended leave patterns suggest that students may have taken breaks for semester exams or long vacations.")

    # Event-Based Leave Patterns
    summary.append(f"The highest number of leaves occurred on {events['most_severe_day']}, possibly due to an important academic or cultural event.")
    
    # Recent Activity Indicator
    summary.append(f"The last notable leave occurrence was on {events['recent_occurrence']}, indicating a possible emerging pattern.")

    return {"Summary": "\n".join(summary)}


def generate_late_checkin_summary(data):
    """Generates a textual summary for late check-ins."""
    if "error" in data:
        return data["error"]

    anomalies = data["anomalies"]
    statistics = data["basic_statistics"]
    events = data["significant_events"]
    patterns = data["temporal_patterns"]

    summary = []

    # Check if late check-ins are minimal or isolated
    if statistics["total_late_checkins"] == 0:
        return {"summary": "There were no late check-ins recorded."}

    # Identify peak late check-in day
    summary.append(f"The highest number of late check-ins occurred on {events['most_severe_day']}, indicating a possible curfew violation.")

    # Anomalies in late check-ins
    if anomalies["values"] and max(anomalies["values"]) > anomalies["threshold"]:
        anomaly_date = anomalies["anomalous_dates"][0]
        summary.append(f"An unusual late check-in was recorded on {anomaly_date}, suggesting an exception or special event.")

    # Day-wise trends
    late_days = {day: count for day, count in patterns["daily_distribution"].items() if count > 0}
    if late_days:
        days_list = ", ".join(late_days.keys())
        summary.append(f"Late check-ins mostly occurred on {days_list}, possibly due to weekend outings or external activities.")

    # Monthly trends
    high_late_months = {month: count for month, count in patterns["monthly_trend"].items() if count > 0}
    if high_late_months:
        months = ", ".join(high_late_months.keys())
        summary.append(f"Late check-ins were observed in {months}, suggesting a pattern during these months.")

    # Recent Activity Indicator
    summary.append(f"The last recorded late check-in was on {events['recent_occurrence']}.")

    return {"Summary": "\n".join(summary)}


def generate_non_checked_in_summary(data):
    """Generates a summary of students who did not check out of the hostel."""
    if "error" in data:
        return data["error"]

    anomalies = data["anomalies"]
    statistics = data["basic_statistics"]
    events = data["significant_events"]
    patterns = data["temporal_patterns"]

    summary = []

    # Overall Non Check-in Stats
    summary.append(f"A total of {statistics['total_non_checked_in']} instances of students not checking out were recorded.")

    # Most Severe Day
    summary.append(f"The highest number of non-checked-in students was recorded on {events['most_severe_day']}.")

    # Anomaly Detection
    if max(anomalies["values"]) > anomalies["threshold"]:
        anomaly_dates = ", ".join(anomalies["anomalous_dates"])
        summary.append(f"Unusual non-check-in patterns were observed on {anomaly_dates}, indicating possible exams, events, or restrictions.")

    # Day-wise Trends
    high_days = {day: count for day, count in patterns["daily_distribution"].items() if count > 1}
    if high_days:
        days_list = ", ".join(high_days.keys())
        summary.append(f"Students frequently stayed in on {days_list}, which could indicate weekly tests, bad weather, or social trends.")

    # Monthly Trends
    high_months = {month: count for month, count in patterns["monthly_trend"].items() if count > 2}
    if high_months:
        months = ", ".join(high_months.keys())
        summary.append(f"High instances of non-check-in occurred in {months}, suggesting a seasonal pattern or academic deadlines.")

    # Recent Activity Indicator
    summary.append(f"The most recent occurrence of students not checking out was on {events['recent_occurrence']}.")

    return {"Summary": "\n".join(summary)}

def generate_leave_trend_summary(data):
    """Generates a summary of planned and urgent leave trends."""
    if "error" in data:
        return data["error"]

    anomalies = data["anomalies"]
    statistics = data["basic_stats"]
    events = data["significant_events"]
    patterns = data["temporal_patterns"]

    summary = []

    # Overall Leave Statistics
    summary.append(f"A total of {statistics['total_leaves']} leaves were recorded, with an average of {statistics['avg_daily_leaves']} leaves per day.")

    # Planned vs Urgent Leaves
    summary.append(f"Planned leaves accounted for {statistics['planned_leaves']['total']} ({data['percentage_distribution']['planned_percentage']['mean']}% on average), while urgent leaves were {statistics['urgent_leaves']['total']} ({data['percentage_distribution']['urgent_percentage']['mean']}% on average).")

    # Most Leaves on a Single Day
    summary.append(f"The highest number of leaves in a single day was {statistics['max_leaves_day']['count']} on {statistics['max_leaves_day']['date']}.")

    # Anomalies
    planned_anomalies = ", ".join(anomalies["planned_anomalies"]["dates"])
    urgent_anomalies = ", ".join(anomalies["urgent_anomalies"]["dates"])
    summary.append(f"Planned leave anomalies occurred on {planned_anomalies}, while urgent leave spikes happened on {urgent_anomalies}.")

    # Day-wise Trends
    high_days = {day: count for day, count in patterns["daily_patterns"]["by_weekday"]["planned_count"].items() if count > 25}
    if high_days:
        days_list = ", ".join(high_days.keys())
        summary.append(f"Planned leaves were most frequent on {days_list}, suggesting patterns around weekends or academic schedules.")

    # Monthly Trends
    high_months = {month: counts for month, counts in patterns["daily_patterns"]["by_month"].items() if counts["planned_count"] > 30}
    if high_months:
        months = ", ".join(high_months.keys())
        summary.append(f"High planned leave trends were observed in {months}, possibly indicating exam or holiday seasons.")

    # Most Unexpected Urgent Leaves
    unexpected_urgent_dates = [event["date"] for event in events["most_unexpected_urgent"] if event["urgent_percentage"] == 100.0]
    if unexpected_urgent_dates:
        unexpected_str = ", ".join(unexpected_urgent_dates)
        summary.append(f"Unexpected urgent leave spikes with 100% urgency were noted on {unexpected_str}, possibly due to emergencies.")

    return {"Summary": "\n".join(summary)}

