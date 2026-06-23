from flask import Flask, render_template, request
import joblib
import pandas as pd
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from duplicate_detector import find_duplicate
from similarity_search import search_similar_bugs
from reportlab.pdfgen import canvas
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

# Load Models
developer_model = joblib.load("models/developer_model.pkl")
priority_model = joblib.load("models/priority_model.pkl")

# History File
HISTORY_FILE = "data/predictions.csv"

# Create file if not exists
if not os.path.exists(HISTORY_FILE):

    pd.DataFrame(
        columns=[
            "bug_description",
            "developer",
            "priority",
            "confidence"
        ]
    ).to_csv(HISTORY_FILE, index=False)


@app.route("/")
def home():

    try:

        history_df = pd.read_csv(HISTORY_FILE)

        if history_df.empty:
            history = []
        else:
            history = history_df.tail(10).to_dict("records")

    except Exception as e:

        print("History Error:", e)
        history = []

    return render_template(
        "index.html",
        history=history
    )


@app.route("/predict", methods=["POST"])
def predict():

    bug = request.form["bug_description"]

    # Duplicate Detection
    duplicate, similar_bug = find_duplicate(bug)

    # Developer Prediction
    probabilities = developer_model.predict_proba([bug])[0]

    developers = developer_model.classes_

    developer_scores = list(
        zip(developers, probabilities)
    )

    developer_scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_developers = [
        (
            dev,
            round(score * 100, 2)
        )
        for dev, score in developer_scores[:3]
    ]

    developer = top_developers[0][0]

    # Priority Prediction
    priority = priority_model.predict([bug])[0]

    # Confidence Score
    confidence = top_developers[0][1]

    # Save Prediction
    new_row = pd.DataFrame([{
        "bug_description": bug,
        "developer": developer,
        "priority": priority,
        "confidence": confidence
    }])

    new_row.to_csv(
        HISTORY_FILE,
        mode="a",
        header=False,
        index=False
    )

    # Latest History
    history = pd.read_csv(
        HISTORY_FILE
    ).tail(10).to_dict("records")

    return render_template(
        "index.html",
        developer=developer,
        priority=priority,
        confidence=confidence,
        duplicate=duplicate,
        similar_bug=similar_bug,
        top_developers=top_developers,
        history=history
    )


@app.route("/dashboard")
def dashboard():

    df = pd.read_csv(HISTORY_FILE)

    total_bugs = len(df)

    high_priority = len(
        df[df["priority"] == "High"]
    )

    critical_priority = len(
        df[df["priority"] == "Critical"]
    )

    developer_counts = (
        df["developer"]
        .value_counts()
        .to_dict()
    )

    priority_counts = (
        df["priority"]
        .value_counts()
        .to_dict()
    )
    # Create date column if missing
    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

    trend_data = (
    df.groupby("date")
    .size()
    .to_dict()
)

    # Developer Workload Pie Chart

    plt.figure(figsize=(5, 5))

    plt.pie(
        developer_counts.values(),
        labels=developer_counts.keys(),
        autopct="%1.1f%%"
    )

    plt.title("Developer Workload")

    plt.savefig("static/developer_chart.png")

    plt.close()

    # Priority Distribution Chart

    plt.figure(figsize=(6, 4))

    plt.bar(
        priority_counts.keys(),
        priority_counts.values()
    )

    plt.title("Priority Distribution")

    plt.savefig("static/priority_chart.png")

    plt.close()

    return render_template(
    "dashboard.html",
    total_bugs=total_bugs,
    high_priority=high_priority,
    critical_priority=critical_priority,
    developer_counts=developer_counts,
    priority_counts=priority_counts,
    trend_data=trend_data
)

@app.route("/similar")
def similar_page():

    return render_template(
        "similar.html"
    )


@app.route("/search_similar", methods=["POST"])
def search_similar():

    query = request.form["bug"]

    results = search_similar_bugs(query)

    return render_template(
        "similar.html",
        query=query,
        results=results
    )
@app.route("/export_pdf")
def export_pdf():

    df = pd.read_csv(HISTORY_FILE)

    pdf_file = "bug_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(100, 800, "Bug Analytics Report")

    c.drawString(
        100,
        770,
        f"Total Bugs: {len(df)}"
    )

    y = 730

    for _, row in df.tail(15).iterrows():

        text = (
            f"{row['bug_description']} | "
            f"{row['developer']} | "
            f"{row['priority']}"
        )

        c.drawString(50, y, text[:100])

        y -= 20

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )
@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    bug = data["bug_description"]

    developer = developer_model.predict([bug])[0]

    priority = priority_model.predict([bug])[0]

    confidence = round(
        max(
            developer_model.predict_proba([bug])[0]
        ) * 100,
        2
    )

    return jsonify({
        "developer": developer,
        "priority": priority,
        "confidence": confidence
    })
@app.route("/api/dashboard")
def api_dashboard():

    df = pd.read_csv(HISTORY_FILE)

    return jsonify({
        "total_bugs": len(df),
        "high_priority":
            len(df[df["priority"] == "High"]),
        "critical_priority":
            len(df[df["priority"] == "Critical"])
    })

if __name__ == "__main__":
    app.run(debug=True)