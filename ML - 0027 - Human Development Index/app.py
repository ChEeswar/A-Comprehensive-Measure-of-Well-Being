from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# 1. Load the saved model file
with open("HDI.pkl", "rb") as file:
    model = pickle.load(file)

# 2. Main home page route
@app.route("/")
def home():
    return render_template("home.html")

# 3. Route to display the input form webpage
@app.route("/Prediction")
def prediction():
    return render_template("indexnew.html")

# 4. FIXED: Route to calculate the prediction (Matches your HTML form lowercase action!)
@app.route("/predict", methods=["POST"])
def predict():
    # Grab user inputs from the HTML form fields
    country = float(request.form["Country"])
    life = float(request.form["Life_Expectancy"])
    school = float(request.form["Mean_Years_of_Schooling"])
    gni = float(request.form["GNI_Per_Capita"])

    # Package them into an array for the model
    features = np.array([[country, life, school, gni]])

    # Run the prediction
    prediction = model.predict(features)
    output = round(prediction[0], 3)

    # Determine the HDI category tier
    if output < 0.55:
        category = "Low HDI"
    elif output < 0.70:
        category = "Medium HDI"
    elif output < 0.80:
        category = "High HDI"
    else:
        category = "Very High HDI"

    # Send the result to your results webpage
    return render_template(
        "resultnew.html",
        prediction_text=f"{category}: {output}"
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)