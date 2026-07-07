
from flask import Flask, render_template, request, send_file, jsonify
import joblib
import pandas as pd
import os
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from duplicate_detector import find_duplicate
from similarity_search import search_similar_bugs
from reportlab.pdfgen import canvas

app = Flask(__name__)

# ===================================
# Load Model
# ===================================

priority_model = joblib.load("models/priority_model.pkl")

# ===================================
# History File
# ===================================

HISTORY_FILE = "data/predictions.csv"

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(
        columns=[
            "bug_description",
            "priority",
            "confidence",
            "date"
        ]
    ).to_csv(HISTORY_FILE, index=False)

# ===================================
# HOME
# ===================================

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


# ===================================
# PREDICT
# ===================================

@app.route("/predict", methods=["POST"])
def predict():

    bug = request.form["bug_description"]

    # Duplicate Detection
    duplicate, similar_bug = find_duplicate(bug)

    # Priority Prediction
    priority = priority_model.predict([bug])[0]

    # Confidence
    try:
        confidence = round(
            max(priority_model.predict_proba([bug])[0]) * 100,
            2
        )
    except:
        confidence = 75.0

    # Save Prediction
    new_row = pd.DataFrame([{
        "bug_description": bug,
        "priority": priority,
        "confidence": confidence,
        "date": pd.Timestamp.now().strftime("%Y-%m-%d")
    }])

    new_row.to_csv(
        HISTORY_FILE,
        mode="a",
        header=False,
        index=False
    )

    history = pd.read_csv(HISTORY_FILE).tail(10).to_dict("records")

    return render_template(
        "index.html",
        priority=priority,
        confidence=confidence,
        duplicate=duplicate,
        similar_bug=similar_bug,
        history=history
    )


# ===================================
# DASHBOARD
# ===================================

@app.route("/dashboard")
def dashboard():

    df = pd.read_csv(HISTORY_FILE)

    total_bugs = len(df)

    priority_counts = (
        df["priority"]
        .value_counts()
        .to_dict()
    )

    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

    trend_data = (
        df.groupby("date")
        .size()
        .to_dict()
    )

    plt.figure(figsize=(8,5))
    plt.bar(
        priority_counts.keys(),
        priority_counts.values()
    )
    plt.title("Priority Distribution")
    plt.xlabel("Priority")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/priority_chart.png")
    plt.close()

    return render_template(
        "dashboard.html",
        total_bugs=total_bugs,
        priority_counts=priority_counts,
        trend_data=trend_data
    )

# ===================================
# SIMILAR BUG SEARCH
# ===================================

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


# ===================================
# PDF EXPORT
# ===================================

@app.route("/export_pdf")
def export_pdf():

    df = pd.read_csv(HISTORY_FILE)

    pdf_file = "bug_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(
        50,
        800,
        "Bug Prediction Report"
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        50,
        770,
        f"Total Predictions: {len(df)}"
    )

    y = 730

    for _, row in df.tail(15).iterrows():

        text = (
            f"{row['priority']} | "
            f"{row['confidence']}% | "
            f"{row['bug_description']}"
        )

        c.drawString(
            40,
            y,
            text[:120]
        )

        y -= 20

        if y < 50:
            c.showPage()
            y = 800

    c.save()

    return send_file(
        pdf_file,
        as_attachment=True
    )


# ===================================
# API - PREDICT
# ===================================

@app.route("/api/predict", methods=["POST"])
def api_predict():

    data = request.get_json()

    bug = data["bug_description"]

    priority = priority_model.predict([bug])[0]

    try:
        confidence = round(
            max(priority_model.predict_proba([bug])[0]) * 100,
            2
        )
    except:
        confidence = 75.0

    return jsonify({
        "priority": priority,
        "confidence": confidence
    })


# ===================================
# API - DASHBOARD
# ===================================

@app.route("/api/dashboard")
def api_dashboard():

    df = pd.read_csv(HISTORY_FILE)

    return jsonify({
        "total_bugs": len(df),
        "priority_distribution":
        df["priority"].value_counts().to_dict()
    })


# ===================================
# RUN
# ===================================

if __name__ == "__main__":
    app.run(debug=True)

