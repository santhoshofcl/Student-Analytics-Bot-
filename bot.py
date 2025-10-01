import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import analytics
import visualize

TOKEN = "8024593561:AAH43e2xP7fnitX1EryjWtMR6EhYuoox-WQ"

logging.basicConfig(level=logging.INFO)

OUTPUT_DIR = "output"

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Student Analytics Bot!\n\n"
        "Available commands:\n"
        "/myreport <student_id>\n"
        "/classreport\n"
        "/rank\n"
        "/subject <subject_name>\n"
        "/prediction <student_id>\n"
        "/exit"
    )

# ---------------- STUDENT REPORT ----------------
async def myreport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ Please provide a Student ID.\nExample: `/myreport 101`")
        return

    try:
        student_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid Student ID. Must be a number.")
        return

    report = analytics.student_report(student_id)
    if not report or report["name"] == "Unknown":
        await update.message.reply_text(f"⚠️ No data found for Student ID: {student_id}")
        return

    # Generate charts
    png_path = visualize.plot_student_progress(student_id)
    html_path = visualize.plotly_student_progress(student_id)

    # Format text
    text = f"📊 Report for {report['name']}\nAverage: {report['average']}\n"
    for subject, score in report["details"].items():
        text += f"{subject}: {score}\n"

    # Send text + charts
    await update.message.reply_text(text)
    with open(png_path, "rb") as f:
        await update.message.reply_photo(photo=f)
    with open(html_path, "rb") as f:
        await update.message.reply_document(document=f)

# ---------------- CLASS REPORT ----------------
async def classreport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = analytics.class_report()
    png_path = visualize.plot_class_average()
    html_path = visualize.plotly_class_average()

    text = "🏫 Class Report (Average per Subject):\n"
    for sub, avg in data.items():
        text += f"{sub}: {round(avg, 2)}\n"

    await update.message.reply_text(text)
    with open(png_path, "rb") as f:
        await update.message.reply_photo(photo=f)
    with open(html_path, "rb") as f:
        await update.message.reply_document(document=f)

# ---------------- RANK LIST ----------------
async def rank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ranks = analytics.rank_list()
    text = "🏆 Rank List:\n"
    for _, row in ranks.iterrows():
        text += f"{int(row['Rank'])}. {row['Name']} - {round(row['Marks'], 2)}\n"
    await update.message.reply_text(text)

# ---------------- SUBJECT REPORT ----------------
async def subject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /subject <subject_name>")
        return

    subject_name = " ".join(context.args)
    rep = analytics.subject_report(subject_name)
    text = (
        f"📘 Subject Report - {subject_name}\n"
        f"Average: {round(rep['average'],2)}\n"
        f"Topper: {rep['topper']}\n"
        f"Lowest: {rep['lowest']}"
    )
    await update.message.reply_text(text)

# ---------------- PREDICTION ----------------
async def prediction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Predicts the next semester average marks for a student.
    Usage: /prediction <student_id>
    """
    if not context.args:
        await update.message.reply_text("Usage: /prediction <student_id>\nExample: /prediction 101")
        return

    try:
        student_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid Student ID. Must be a number.")
        return

    # Call semester-based prediction function
    pred = analytics.predict_next_semester_total(student_id)

    await update.message.reply_text(
        f"📈 Predicted next semester average marks for student {student_id}: {pred}"
    )

# Message to show on exit
EXIT_MSG = "👋 Thank you for using Student Analytics Bot! See you soon."

async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(EXIT_MSG)

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myreport", myreport))
    app.add_handler(CommandHandler("classreport", classreport))
    app.add_handler(CommandHandler("rank", rank))
    app.add_handler(CommandHandler("subject", subject))
    app.add_handler(CommandHandler("prediction", prediction))
    app.add_handler(CommandHandler("exit", exit_command))
    app.run_polling()

if __name__ == "__main__":
    main()
