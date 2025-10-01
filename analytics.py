import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# ---------------- Load Dataset ----------------
df = pd.read_csv("data/marks.csv")

# ---------------- Student Report ----------------
def student_report(student_id):
    """
    Returns student details, average marks, and subject-wise averages.
    """
    student = df[df["StudentID"] == student_id]
    if student.empty:
        return {"name": "Unknown", "average": 0, "details": {}}
    
    avg = student["Marks"].mean()
    subject_avg = student.groupby("Subject")["Marks"].mean().to_dict()
    
    return {
        "name": student["Name"].iloc[0],
        "average": round(avg, 2),
        "details": subject_avg
    }

# ---------------- Class Report ----------------
def class_report():
    """
    Returns class average marks per subject.
    """
    return df.groupby("Subject")["Marks"].mean().round(2).to_dict()

# ---------------- Rank List ----------------
def rank_list():
    """
    Returns a DataFrame with student average marks and ranks.
    """
    avg_scores = df.groupby(["StudentID", "Name"])["Marks"].mean().reset_index()
    avg_scores["Rank"] = avg_scores["Marks"].rank(ascending=False, method="dense").astype(int)
    return avg_scores.sort_values("Rank").reset_index(drop=True)

# ---------------- Subject Report ----------------
def subject_report(subject):
    """
    Returns subject-specific analytics: average, topper, lowest scorer.
    """
    sub_df = df[df["Subject"].str.lower() == subject.lower()]
    if sub_df.empty:
        return {"average": 0, "topper": "N/A", "lowest": "N/A"}
    
    return {
        "average": round(sub_df["Marks"].mean(), 2),
        "topper": sub_df.loc[sub_df["Marks"].idxmax()]["Name"],
        "lowest": sub_df.loc[sub_df["Marks"].idxmin()]["Name"]
    }

# ---------------- Marks Prediction ----------------
def predict_next_semester_total(student_id):
    """
    Predicts the next semester average marks for a student across all subjects.
    Returns predicted marks (0-100) or a message if not enough data.
    """
    # Filter student data
    student = df[df["StudentID"] == student_id]

    if student.empty:
        return "No data available for this student."

    if "ExamType" not in student.columns:
        return "Exam/Semester column missing in dataset."

    # Compute average marks per semester
    semester_avg = student.groupby("ExamType")["Marks"].mean().sort_index()
    
    if len(semester_avg) < 2:
        return "Not enough data to predict next semester marks (need at least 2 semesters)."

    # Linear regression
    X = np.arange(len(semester_avg)).reshape(-1, 1)  # 0,1,2,... semester sequence
    y = semester_avg.values

    model = LinearRegression()
    model.fit(X, y)

    next_sem_index = len(semester_avg)
    predicted_marks = model.predict([[next_sem_index]])[0]

    # Clip marks to 0-100
    predicted_marks = max(0, min(100, predicted_marks))

    return round(predicted_marks, 2)