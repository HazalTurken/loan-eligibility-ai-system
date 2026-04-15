import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="Smart Loan Advisor AI", page_icon="💰", layout="centered")

# Add model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Add feature columns
with open("feature_columns.pkl", "rb") as f:
    feature_columns = pickle.load(f)

# Title
st.title("💰 Smart Loan Advisor AI")
st.write("Fill in the applicant information below and see the eligibility result.")

# User Inputs
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
applicant_income = st.number_input("Applicant Income", min_value=0, value=5000, step=100)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0.0, value=0.0, step=100.0)
loan_amount = st.number_input("Loan Amount", min_value=1.0, value=120.0, step=1.0)
loan_amount_term = st.number_input("Loan Amount Term", min_value=1.0, value=360.0, step=1.0)
credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Adapting the input to the model
def build_input_df():

    """
    Creates a DataFrame from user inputs in the correct format for the trained model.
    
    It applies manual encoding for categorical variables, fills missing columns,
    and ensures the feature order matches the training data.
    
    Returns:
        pd.DataFrame: Model-ready input data.
    """
    
    input_dict = {
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_amount_term,
        "Credit_History": credit_history,
        "Gender_Male": 1 if gender == "Male" else 0,
        "Married_Yes": 1 if married == "Yes" else 0,
        "Dependents_1": 1 if dependents == "1" else 0,
        "Dependents_2": 1 if dependents == "2" else 0,
        "Dependents_3+": 1 if dependents == "3+" else 0,
        "Education_Not Graduate": 1 if education == "Not Graduate" else 0,
        "Self_Employed_Yes": 1 if self_employed == "Yes" else 0,
        "Property_Area_Semiurban": 1 if property_area == "Semiurban" else 0,
        "Property_Area_Urban": 1 if property_area == "Urban" else 0,
    }

    # Turn into DataFrame
    input_df = pd.DataFrame([input_dict])

    for col in feature_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[feature_columns]
    return input_df

# Giving advice
def get_advice(probability):
    
    """
    Generates simple improvement suggestions based on user inputs and prediction results.
    
    It evaluates key factors such as income, credit history, loan amount, and coapplicant income
    to provide actionable advice for increasing loan approval chances.
    
    Returns:
        list: A list of recommendation strings.
    """
    
    advice = []

    if credit_history == 0.0:
        advice.append("Improve credit history.")
    if applicant_income < 4000:
        advice.append("Higher stable income may increase approval chances.")
    if loan_amount > 200:
        advice.append("Reducing the requested loan amount may help.")
    if coapplicant_income == 0:
        advice.append("A coapplicant income may strengthen the application.")

    if not advice:
        advice.append("Your current profile already looks strong.")

    return advice

# Button Trigger
if st.button("Check Eligibility"):
    input_df = build_input_df()
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    st.subheader("Result")

    if prediction == 1:
        st.success("✅ Eligible")
    else:
        st.error("❌ Not Eligible")

    st.write(f"**Approval Probability:** {probability:.2%}")

    # Gamified score
    score = int(probability * 100)
    st.metric("Loan Readiness Score", f"{score}/100")
    st.progress(score)

    # Risk band
    if probability >= 0.75:
        st.info("🏆 Risk Level: Low Risk")
    elif probability >= 0.50:
        st.warning("🎯 Risk Level: Medium Risk")
    else:
        st.error("⚠️ Risk Level: High Risk")

    # Advice
    st.markdown("### 💡 Improvement Advice")
    for item in get_advice(probability):
        st.write(f"- {item}")

    # Ballons on screen
    if score >= 80:
        st.balloons()