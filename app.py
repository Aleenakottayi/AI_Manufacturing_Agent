import joblib
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import datetime

app = Flask(__name__)
app.secret_key = "industrial_secret"
model = joblib.load("energy_model.pkl")

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin":
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    prediction = session.get("prediction")
    return render_template("dashboard.html", prediction=prediction)


# ---------------- AI PREDICTION ----------------
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("login"))

    temperature = float(request.form["temperature"])
    pressure = float(request.form["pressure"])
    machine_load = float(request.form["machine_load"])
    runtime = float(request.form["runtime"])

    input_data = np.array([[temperature, pressure, machine_load, runtime]])
    predicted_energy = round(float(model.predict(input_data)[0]), 2)

    # Carbon factor (kg CO2 per kWh)
    emission_factor = 0.45
    predicted_carbon = round(predicted_energy * emission_factor, 2)

    # Electricity cost (₹ per kWh industrial avg)
    cost_per_kwh = 8
    estimated_cost = round(predicted_energy * cost_per_kwh, 2)

    # Carbon tax (₹ 1500 per ton CO2)
    carbon_tax_per_ton = 1500
    carbon_tax = round((predicted_carbon / 1000) * carbon_tax_per_ton, 2)

    # ---------------- Risk Classification ----------------
    if predicted_energy < 1000:
        risk_color = "green"
        status = "Low"
        sustainability_score = "A"
        recommendation = "System operating efficiently. Maintain current parameters."
    elif predicted_energy < 1300:
        risk_color = "yellow"
        status = "Moderate"
        sustainability_score = "B"
        recommendation = "Minor optimization possible. Consider reducing runtime slightly."
    elif predicted_energy < 1600:
        risk_color = "orange"
        status = "High"
        sustainability_score = "C"
        recommendation = "Reduce machine load by 5–10% to improve efficiency."
    else:
        risk_color = "red"
        status = "Critical"
        sustainability_score = "D"
        recommendation = "Immediate optimization required. Reduce load and temperature."

    session["prediction"] = {
        "temperature": temperature,
        "pressure": pressure,
        "machine_load": machine_load,
        "runtime": runtime,
        "energy": predicted_energy,
        "carbon": predicted_carbon,
        "cost": estimated_cost,
        "carbon_tax": carbon_tax,
        "risk_color": risk_color,
        "status": status,
        "score": sustainability_score,
        "recommendation": recommendation
    }

    return redirect(url_for("dashboard"))

# ---------------- DOWNLOAD REPORT ----------------
@app.route("/download-report")
def download_report():
    if "user" not in session:
        return redirect(url_for("login"))

    prediction = session.get("prediction")

    if not prediction:
        return redirect(url_for("dashboard"))

    file_path = "report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("AI-Driven Manufacturing Energy Intelligence Report", styles["Heading1"]))
    elements.append(Spacer(1, 20))

    # Date
    today = datetime.datetime.now().strftime("%d %B %Y %H:%M")
    elements.append(Paragraph(f"Generated On: {today}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    # Table Data
    data = [
        ["Parameter", "Value"],
        ["Temperature (°C)", prediction["temperature"]],
        ["Pressure (bar)", prediction["pressure"]],
        ["Machine Load (%)", prediction["machine_load"]],
        ["Runtime (hours)", prediction["runtime"]],
        ["Predicted Energy (kWh)", prediction["energy"]],
        ["Predicted Carbon (kg CO2)", prediction["carbon"]],
    ]

    table = Table(data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    # Explanation Section
    elements.append(Paragraph("Analysis & Insights:", styles["Heading2"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "The AI model predicts energy consumption based on operational parameters. "
        "Higher temperature and extended runtime significantly increase energy usage. "
        "Carbon emissions are estimated using an industrial emission factor of 0.45 kg CO2 per kWh.",
        styles["Normal"]
    ))

    doc.build(elements)

    return send_file(file_path, as_attachment=True)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("prediction", None)
    return redirect(url_for("home"))



 if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))  # Get the port Render assigns
    app.run(host="0.0.0.0", port=port, debug=True)