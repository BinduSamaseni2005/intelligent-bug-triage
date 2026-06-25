# Intelligent Bug Triage System

An AI-powered bug management platform that automates bug triaging using Machine Learning. The system predicts the most suitable developer, estimates bug priority, detects duplicate issues, performs similar bug searches, and provides analytics dashboards to improve issue resolution efficiency.

## Features

* Automated Developer Assignment Prediction using Machine Learning
* Bug Priority Prediction (Low, Medium, High, Critical)
* Duplicate Bug Detection using Text Similarity Analysis
* Similar Bug Search for faster issue resolution
* Bug Trend Analytics Dashboard
* PDF Report Generation and Export
* REST API Support
* Real-time Project Insights and Monitoring

## Technologies Used

### Backend

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy

### Visualization & Reporting

* Matplotlib
* ReportLab

### Frontend

* HTML
* CSS
* Jinja2 Templates

## Machine Learning Components

* TF-IDF Vectorization
* Random Forest Classification
* Text Similarity Matching
* Priority Classification
* Developer Recommendation Engine

## Screenshots

### Home Page

![Home Page](screenshots/home-page.png)

### Similar Bug Search

![Similar Bug Search](screenshots/similar-bug-search.png)

### Analytics Dashboard

![Analytics Dashboard](screenshots/dashboard.png)

### Bug Trend Analytics

![Bug Trend Analytics](screenshots/dashboard-1.png)

## Project Structure

```text
intelligent-bug-triage/
│
├── app.py
├── requirements.txt
├── README.md
├── screenshots/
│   ├── home-page.png
│   ├── similar-bug-search.png
│   ├── dashboard.png
│   └── dashboard-1.png
│
├── templates/
├── static/
├── models/
└── data/
```

## Installation

Clone the repository:

```bash
git clone https://github.com/BinduSamaseni2005/intelligent-bug-triage.git
cd intelligent-bug-triage
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application:

```text
http://127.0.0.1:5000
```

## REST API Endpoints

| Endpoint        | Method   | Description                      |
| --------------- | -------- | -------------------------------- |
| /               | GET      | Home Page                        |
| /predict        | POST     | Predict Developer and Priority   |
| /search_similar | GET/POST | Similar Bug Search               |
| /dashboard      | GET      | Analytics Dashboard              |
| /download_pdf   | GET      | Generate and Download PDF Report |

## Key Highlights

* Automated bug triaging using Machine Learning
* Reduced manual effort in developer assignment
* Improved issue prioritization and tracking
* Analytics-driven bug monitoring
* Exportable PDF reports for project stakeholders

## Future Enhancements

* Jira Integration
* GitHub Issues Integration
* Email Notifications for Critical Bugs
* Deep Learning-based Classification
* Team Performance Analytics
* Multi-Project Support

## Author

**Bindu Reddy**
