import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
timetable = {
    "Monday": {
        "OOAD": 1,
        "QM": 1,
        "AI": 1,
        "APTI": 1,
        "TOC": 1,
        "DCN": 1,
        "MN": 1
    },
    "Tuesday": {
        "NW LAB": 4,
        "TECH": 1,
        "LIB": 1,
        "QM": 1
    },
    "Wednesday": {
        "MN": 1,
        "OOAD": 1,
        "QM": 1,
        "APTI": 1,
        "TOC": 1,
        "DCN": 1,
        "AI": 1
    },
    "Thursday": {
        "TOC": 1,
        "DCN": 1,
        "MN": 1,
        "AI": 1,
        "CT LAB": 3
    },
    "Friday": {
        "AI": 1,
        "APTI": 1,
        "OOAD": 1,
        "TOC": 1,
        "TECH": 2,
        "SWAYAM": 1
    }
}

def calculate_attendance(absent_days):
    total_weeks = 15
    attendance_data = []
    subjects = {}

    for day, subjects_in_day in timetable.items():
        for subject, periods_per_day in subjects_in_day.items():
            if subject not in subjects:
                subjects[subject] = 0
            subjects[subject] += periods_per_day

    for subject, total_periods in subjects.items():
        total_hours = total_periods * total_weeks
        days_absent = sum(absent_days.get(day, 0) * timetable[day].get(subject, 0) for day in absent_days)
        hours_attended = total_hours - days_absent
        attendance_percentage = (hours_attended / total_hours) * 100
        required_percentage = 75
        status = "Met Requirement" if attendance_percentage >= required_percentage else "Below Requirement"
        attendance_data.append([subject, total_periods, total_hours, days_absent,
                                f"{attendance_percentage:.2f}%", status])

    df = pd.DataFrame(attendance_data, columns=["Subject", "Periods/Week", "Total Hours",
                                                "Days Absent", "Attendance Percentage", "Status"])

    return df

def highlight_attendance(val):
    percentage = float(val[:-1])  
    
    if 90 <= percentage <= 100:
        return 'background-color: darkgreen'
    elif 80 <= percentage < 90:
        return 'background-color: mediumseagreen'
    elif 70 <= percentage < 80:
        return 'background-color: yellowgreen'
    elif 50 <= percentage < 70:
        return 'background-color: lightcoral'
    else:  
        return 'background-color: darkred'

def attendance_app():
    st.title("Attendance Tracker")

    absent_days = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}

    with st.sidebar:
        st.header("Mark Absences for Each Day")
        for day in absent_days.keys():
            absent_days[day] = st.number_input(f"{day}", min_value=0, step=1, key=f"input_{day}")
    
    st.write(f"Updated Leave Hours: {absent_days}")

    if st.button("Calculate Attendance Report"):
        df = calculate_attendance(absent_days)
        
        plot_attendance(df)
        
        styled_df = df.style.applymap(highlight_attendance, subset=["Attendance Percentage"])
        
        st.write("Attendance Report:")
        st.dataframe(styled_df)

        csv = convert_df(df)
        st.download_button("Download Attendance Report", csv, "attendance_report.csv", "text/csv", key="download_button")

def plot_attendance(df):
    subjects = df['Subject'].tolist()
    percentages = df['Attendance Percentage'].apply(lambda x: float(x.strip('%'))).tolist()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(subjects, percentages, label="Attendance Percentage", color='skyblue', marker='o')
    ax.plot(subjects, [75] * len(subjects), label="75% Requirement", color='orange', linestyle='--', marker='x')

    ax.set_xlabel('Subjects')
    ax.set_ylabel('Attendance Percentage')
    ax.set_title('Attendance vs 75% Requirement')
    ax.legend()

    st.pyplot(fig)

def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

if __name__ == "__main__":
    attendance_app()
