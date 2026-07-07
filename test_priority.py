import joblib

model = joblib.load(
    "models/priority_model.pkl"
)

bug = "Browser crashes when opening multiple tabs"

prediction = model.predict([bug])[0]

print("Predicted Priority:", prediction)