import numpy as np
import pandas as pd
from scipy import stats


def late_checkins(data):
    """Analyzes late check-ins with multiple dimensions."""
    try:
        dates = pd.to_datetime(data["data"]["labels"])
        late_checkins = np.array(data["data"]["late_checked_in"])
        

        df = pd.DataFrame({
            "date": dates,
            "late_checkins": late_checkins,
            
        }).set_index("date")

        stats = {
            "total_late_checkins": int(df["late_checkins"].sum()),
            "days_with_late_checkins": int((df["late_checkins"] > 0).sum()),
            "max_consecutive_days": max_consecutive_days(df["late_checkins"]),
            "checkin_frequency": {
                "daily_avg": round(df["late_checkins"].mean(), 2),
                "weekly_avg": round(df["late_checkins"].resample("W").sum().mean(), 2)
            }
        }

        # 🛠️ FIX: Convert PeriodIndex to string using strftime
        monthly_trend = df.resample("ME")["late_checkins"].sum()
        monthly_trend = {key.strftime("%Y-%m") : int(value) for key, value in monthly_trend.items()} 

        temporal = {
            "daily_distribution": df.groupby(df.index.day_name())["late_checkins"].sum().to_dict(),
            "monthly_trend": monthly_trend
        }

        anomalies = find_anomalies(df["late_checkins"])

        events = {
            "most_severe_day": df["late_checkins"].idxmax().strftime("%Y-%m-%d"),
            "recent_occurrence": df[df["late_checkins"] > 0].index[-1].strftime("%Y-%m-%d") if stats["days_with_late_checkins"] > 0 else None
        }

        return {
            "basic_statistics": stats,
            "temporal_patterns": temporal,
            "anomalies": anomalies,
            "significant_events": events
        }

    except Exception as e:
        return {"error": str(e)}


def on_leave(data):
    """Analyzes student leave trends with multiple dimensions."""
    try:
        dates = pd.to_datetime(data["data"]["labels"])
        on_leave = np.array(data["data"]["on_leave"])

        df = pd.DataFrame({
            "date": dates,
            "on_leave": on_leave
        }).set_index("date")

        stats = {
            "total_on_leave": int(df["on_leave"].sum()),
            "days_with_leaves": int((df["on_leave"] > 0).sum()),
            "max_consecutive_days": max_consecutive_days(df["on_leave"]),
            "leave_frequency": {
                "daily_avg": round(df["on_leave"].mean(), 2),
                "weekly_avg": round(df["on_leave"].resample("W").sum().mean(), 2)
            }
        }

        # 🛠️ Fix: Convert PeriodIndex to string using strftime
        monthly_trend = df.resample("ME")["on_leave"].sum()
        monthly_trend = {key.strftime("%Y-%m"): int(value) for key, value in monthly_trend.items()}

        temporal = {
            "daily_distribution": df.groupby(df.index.day_name())["on_leave"].sum().to_dict(),
            "monthly_trend": monthly_trend
        }

        anomalies = find_anomalies(df["on_leave"])

        events = {
            "most_severe_day": df["on_leave"].idxmax().strftime("%Y-%m-%d"),
            "recent_occurrence": df[df["on_leave"] > 0].index[-1].strftime("%Y-%m-%d") if stats["days_with_leaves"] > 0 else None
        }

        return {
            "basic_statistics": stats,
            "temporal_patterns": temporal,
            "anomalies": anomalies,
            "significant_events": events
        }

    except Exception as e:
        return {"error": str(e)}
    

def non_checked_in(data):
    """Analyzes student leave trends with multiple dimensions."""
    try:
        dates = pd.to_datetime(data["data"]["labels"])
        non_checked_in = np.array(data["data"]["non_checked_in"])

        df = pd.DataFrame({
            "date": dates,
            "non_checked_in": non_checked_in
        }).set_index("date")

        stats = {
            "total_non_checked_in": int(df["non_checked_in"].sum()),
            "days_with_non_checked_in": int((df["non_checked_in"] > 0).sum()),
            "max_consecutive_days": max_consecutive_days(df["non_checked_in"]),
            "leave_frequency": {
                "daily_avg": round(df["non_checked_in"].mean(), 2),
                "weekly_avg": round(df["non_checked_in"].resample("W").sum().mean(), 2)
            }
        }

        # 🛠️ Fix: Convert PeriodIndex to string using strftime
        monthly_trend = df.resample("ME")["non_checked_in"].sum()
        monthly_trend = {key.strftime("%Y-%m"): int(value) for key, value in monthly_trend.items()}

        temporal = {
            "daily_distribution": df.groupby(df.index.day_name())["non_checked_in"].sum().to_dict(),
            "monthly_trend": monthly_trend
        }

        anomalies = find_anomalies(df["non_checked_in"])

        events = {
            "most_severe_day": df["non_checked_in"].idxmax().strftime("%Y-%m-%d"),
            "recent_occurrence": df[df["non_checked_in"] > 0].index[-1].strftime("%Y-%m-%d") if stats["days_with_non_checked_in"] > 0 else None
        }

        return {
            "basic_statistics": stats,
            "temporal_patterns": temporal,
            "anomalies": anomalies,
            "significant_events": events
        }

    except Exception as e:
        return {"error": str(e)}
    
    


def max_consecutive_days(series):
    count = max_count = 0
    for val in series:
        count = count + 1 if val > 0 else 0
        max_count = max(max_count, count)
    return max_count

def find_anomalies(series):
    # Using IQR for non-normal distribution
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    anomalies = series[series > (q3 + 1.5 * iqr)]
    return {
        "threshold": q3 + 1.5 * iqr,
        "anomalous_dates": anomalies.index.strftime("%Y-%m-%d").tolist(),
        "values": anomalies.values.tolist()
    }


import numpy as np
import pandas as pd
from scipy import stats

def leave_trends(data):
    """Analyzes planned and unplanned leave trends from JSON data."""
    
    # Convert JSON to DataFrame
    df = pd.DataFrame(data["data"]["plannedUnplannedLeavesTrends"])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()
    
    # Convert numeric columns to float
    numeric_cols = ['urgent_count', 'planned_count', 'total_leaves', 'urgent_percentage', 'planned_percentage']
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Avoid division errors
    df['urgent_ratio'] = df['urgent_count'] / (df['total_leaves'] + 1e-6)
    df['planning_efficiency'] = df['planned_count'] / (df['planned_count'] + df['urgent_count'] + 1e-6)

    # Perform analysis
    analysis = {
        "basic_stats": get_basic_stats(df),
        "temporal_patterns": temporal_analysis(df),
        "anomalies": detect_anomalies(df),
       
        "significant_events": identify_significant_events(df),
        "correlation_analysis": calculate_correlations(df),
        "percentage_distribution": analyze_percentages(df)
    }

    return analysis

def get_basic_stats(df):
    return {
        "total_leaves": int(df['total_leaves'].sum()),
        "avg_daily_leaves": round(df['total_leaves'].mean(), 2),
        "max_leaves_day": {
            "date": df['total_leaves'].idxmax().strftime("%Y-%m-%d"),
            "count": int(df['total_leaves'].max())
        },
        "urgent_leaves": {
            "total": int(df['urgent_count'].sum()),
            "daily_avg": round(df['urgent_count'].mean(), 2),
            "max_day": df['urgent_count'].idxmax().strftime("%Y-%m-%d")
        },
        "planned_leaves": {
            "total": int(df['planned_count'].sum()),
            "daily_avg": round(df['planned_count'].mean(), 2),
            "max_day": df['planned_count'].idxmax().strftime("%Y-%m-%d")
        }
    }

def temporal_analysis(df):
    return {
        "daily_patterns": {
            "by_weekday": df.groupby(df.index.day_name())[['urgent_count', 'planned_count']].sum().to_dict(),
            "by_month": {
                key.strftime("%Y-%m"): value.to_dict() 
                for key, value in df.resample('ME')[['urgent_count', 'planned_count']].sum().iterrows()
            }
        },
        
    }


def detect_anomalies(df):
    def find_iqr_anomalies(series):
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        return series[series > (q3 + 1.5 * iqr)]
    
    return {
        "urgent_anomalies": format_anomalies(find_iqr_anomalies(df['urgent_count'])),
        "planned_anomalies": format_anomalies(find_iqr_anomalies(df['planned_count']))
    }

def format_anomalies(series):
    return {
        "dates": series.index.strftime("%Y-%m-%d").tolist(),
        "values": series.values.tolist(),
    }




def identify_significant_events(df):
    return {
        "highest_urgent_percentage": get_max_percentage_event(df, 'urgent_percentage'),
        "highest_planned_percentage": get_max_percentage_event(df, 'planned_percentage'),
        "most_unexpected_urgent": get_unexpected_events(df)
    }

def get_max_percentage_event(df, col):
    max_row = df[col].idxmax()
    return {
        "date": max_row.strftime("%Y-%m-%d"),
        "percentage": round(float(df.loc[max_row, col]), 2),
        "total_leaves": int(df.loc[max_row, 'total_leaves'])
    }

def get_unexpected_events(df):
    """Find events where urgent leave percentage is unusually high."""
    unexpected = df[df['urgent_percentage'] > 70]  # Fixed Syntax Error
    return [{
        "date": idx.strftime("%Y-%m-%d"),
        "urgent_percentage": round(float(row['urgent_percentage']), 2),
        "total_leaves": int(row['total_leaves'])
    } for idx, row in unexpected.iterrows()]

def calculate_correlations(df):
    return {
        "urgent_vs_planned": round(df['urgent_count'].corr(df['planned_count']), 3),
        "urgent_vs_total": round(df['urgent_count'].corr(df['total_leaves']), 3),
        "planned_vs_total": round(df['planned_count'].corr(df['total_leaves']), 3)
    }

def analyze_percentages(df):
    return {
        "urgent_percentage": {
            "mean": round(df['urgent_percentage'].mean(), 2),
            "std_dev": round(df['urgent_percentage'].std(), 2)
        },
        "planned_percentage": {
            "mean": round(df['planned_percentage'].mean(), 2),
            "std_dev": round(df['planned_percentage'].std(), 2)
        }
    }


