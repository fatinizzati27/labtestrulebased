import streamlit as st
import json
from PyPDF2 import PdfReader

# Load rules from JSON file
with open("json_q2.txt", "r") as f:
    rules = json.load(f)

# Sort rules by priority (highest first)
rules = sorted(rules, key=lambda x: x["priority"], reverse=True)

st.title("Rule-Based Smart Home Air Conditioner Controller")

# Input fields
temperature = st.number_input("Temperature (°C)", value=22)
humidity = st.number_input("Humidity (%)", value=46)
occupancy = st.selectbox("Occupancy", ["OCCUPIED", "EMPTY"])
time_of_day = st.selectbox("Time of Day", ["MORNING", "AFTERNOON", "EVENING", "NIGHT"])
windows_open = st.checkbox("Windows Open")

facts = {
    "temperature": temperature,
    "humidity": humidity,
    "occupancy": occupancy,
    "time_of_day": time_of_day,
    "windows_open": windows_open
}

# Function to evaluate conditions
def check_condition(condition, facts):
    var, op, value = condition
    fact_value = facts[var]

    if op == "==":
        return fact_value == value
    elif op == ">=":
        return fact_value >= value
    elif op == "<=":
        return fact_value <= value
    elif op == "<":
        return fact_value < value
    else:
        return False

# Rule engine
def run_rule_engine(facts, rules):
    for rule in rules:
        if all(check_condition(cond, facts) for cond in rule["conditions"]):
            return rule
    return None

if st.button("Decide AC Settings"):
    matched_rule = run_rule_engine(facts, rules)

    if matched_rule:
        st.success(f"Applied Rule: {matched_rule['name']}")
        st.write("### Final AC Settings")
        st.write("AC Mode:", matched_rule["action"]["ac_mode"])
        st.write("Fan Speed:", matched_rule["action"]["fan_speed"])
        st.write("Setpoint:", matched_rule["action"]["setpoint"])
        st.write("Reason:", matched_rule["action"]["reason"])
    else:
        st.warning("No matching rule found.")
