# Intelligent Bug Triage System

An AI-powered bug management system that automatically predicts the most suitable developer, estimates bug priority, detects duplicate issues, performs similar bug searches, and provides analytics dashboards for project monitoring.

## Features

* Developer Assignment Prediction
* Priority Prediction
* Duplicate Bug Detection
* Similar Bug Search
* Analytics Dashboard
* PDF Report Export
* REST APIs
* Historical Bug Analysis

## Technologies Used

* Python
* Flask
* Scikit-learn
* Pandas
* NumPy
* Matplotlib
* ReportLab
* HTML/CSS
* Jinja2 Templates

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
Intelligent-Bug-Triage-System/
│
├── app.py
├── requirements.txt
├── README.md
├── home-page.png
├── similar-bug-search.png
├── dashboard.png
├── dashboard-1.png
├── templates/
├── static/
├── models/
└── data/
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd Intelligent-Bug-Triage-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

## API Endpoints

| Endpoint        | Method   | Description                  |
| --------------- | -------- | ---------------------------- |
| /               | GET      | Home Page                    |
| /predict        | POST     | Predict Developer & Priority |
| /search_similar | GET/POST | Similar Bug Search           |
| /dashboard      | GET      | Analytics Dashboard          |
| /download_pdf   | GET      | Download PDF Report          |

## Future Enhancements

* Integration with Jira and GitHub Issues
* Deep Learning-based Bug Classification
* Real-time Notifications
* Team Performance Analytics
* Multi-project Support

## Author

Bindu Reddy
