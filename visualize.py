import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load dataset
df = pd.read_csv("data/marks.csv")

# Output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# ---------------- Matplotlib: Student Progress (Single Line) ----------------
def plot_student_progress(student_id):
    student = df[df["StudentID"] == student_id].sort_values("ExamType")
    
    # Overall marks average across subjects per exam
    pivot = student.groupby("ExamType")["Marks"].mean()
    
    plt.figure(figsize=(8,5))
    plt.plot(pivot.index, pivot.values, marker='o', color='blue', label='Average Marks')
    plt.title(f"{student['Name'].iloc[0]} Progress")
    plt.xlabel("Exam")
    plt.ylabel("Marks")
    plt.ylim(0, 100)
    plt.grid(True)
    plt.legend()
    
    file_path = os.path.join(output_dir, "student_progress.png")
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()
    return file_path

# ---------------- Plotly: Student Progress (Single Line) ----------------
def plotly_student_progress(student_id):
    student = df[df["StudentID"] == student_id].sort_values("ExamType")
    
    # Average marks per exam
    avg_marks = student.groupby("ExamType")["Marks"].mean().reset_index()
    
    fig = px.line(
        avg_marks,
        x="ExamType",
        y="Marks",
        markers=True,
        title=f"{student['Name'].iloc[0]} Progress (Interactive)",
        labels={"Marks":"Marks", "ExamType":"Exam"}
    )
    fig.update_yaxes(range=[0, 100])
    
    file_path = os.path.join(output_dir, "student_progress.html")
    fig.write_html(file_path)
    return file_path

# ---------------- Matplotlib: Class Average ----------------
def plot_class_average():
    avg = df.groupby("ExamType")["Marks"].mean()
    
    plt.figure(figsize=(8,5))
    plt.plot(avg.index, avg.values, marker='o', color='green')
    plt.title("Class Average Progress")
    plt.xlabel("Exam")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.grid(True)
    
    file_path = os.path.join(output_dir, "class_avg.png")
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()
    return file_path

# ---------------- Plotly: Class Average ----------------
def plotly_class_average():
    avg = df.groupby("ExamType")["Marks"].mean().reset_index()
    
    fig = px.line(
        avg,
        x="ExamType",
        y="Marks",
        markers=True,
        title="Class Average Progress (Interactive)"
    )
    fig.update_yaxes(range=[0, 100])
    
    file_path = os.path.join(output_dir, "class_avg.html")
    fig.write_html(file_path)
    return file_path
