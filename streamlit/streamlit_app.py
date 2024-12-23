import streamlit as st
import pandas as pd
import joblib

# Load model and preprocessor
preprocessor = joblib.load('preprocessor_model.joblib')
model = joblib.load('best_xgb_model.joblib')

def predict_attrition(input_data):
    """
    Function to predict attrition and return results.
    """
    try:
        processed_data = preprocessor.transform(input_data)
        prediction = model.predict(processed_data)
        prediction_prob = model.predict_proba(processed_data)
        return prediction, prediction_prob
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None, None

# Streamlit App
st.title("Employee Attrition Prediction")
st.write("Predict the likelihood of employee attrition based on key features.")

# Input Form
with st.form(key="input_form"):
    st.header("Input Employee Details")

    # Numeric Inputs
    age = st.number_input("Age", min_value=16, max_value=65, value=30)
    daily_rate = st.number_input("Daily Rate", min_value=1, max_value=1500, value=500)
    distance_from_home = st.number_input("Distance from Home (km)", min_value=0, max_value=50, value=10)
    hourly_rate = st.number_input("Hourly Rate", min_value=1, max_value=100, value=50)
    monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=20000, value=5000)
    monthly_rate = st.number_input("Monthly Rate", min_value=1000, max_value=50000, value=20000)
    num_companies_worked = st.number_input("Number of Companies Worked", min_value=0, max_value=20, value=3)
    percent_salary_hike = st.number_input("Percent Salary Hike", min_value=0, max_value=100, value=10)
    total_working_years = st.number_input("Total Working Years", min_value=0, max_value=50, value=10)
    training_times_last_year = st.number_input("Training Times Last Year", min_value=0, max_value=10, value=2)
    years_at_company = st.number_input("Years at Company", min_value=0, max_value=50, value=5)
    years_in_current_role = st.number_input("Years in Current Role", min_value=0, max_value=20, value=2)
    years_since_last_promotion = st.number_input("Years Since Last Promotion", min_value=0, max_value=20, value=1)
    years_with_curr_manager = st.number_input("Years with Current Manager", min_value=0, max_value=20, value=3)

    # Categorical Inputs
    gender = st.selectbox("Gender", options=["Male", "Female"])
    over_18 = st.selectbox("Over 18", options=["Yes", "No"])
    over_time = st.selectbox("Over Time", options=["Yes", "No"])
    business_travel = st.selectbox("Business Travel", options=["Non-Travel", "Travel_Rarely", "Travel_Frequently"])
    department = st.selectbox("Department", options=["Sales", "Research & Development", "Human Resources"])
    education = st.selectbox("Education Level", options=[1, 2, 3, 4, 5], format_func=lambda x: ["Below College", "College", "Bachelor", "Master", "Doctor"][x-1])
    education_field = st.selectbox("Education Field", options=["Life Sciences", "Medical", "Marketing", "Technical Degree", "Human Resources", "Other"])
    environment_satisfaction = st.selectbox("Environment Satisfaction", options=[1, 2, 3, 4], format_func=lambda x: ["Low", "Medium", "High", "Very High"][x-1])
    job_involvement = st.selectbox("Job Involvement", options=[1, 2, 3, 4], format_func=lambda x: ["Low", "Medium", "High", "Very High"][x-1])
    job_level = st.selectbox("Job Level", options=[1, 2, 3, 4, 5])
    job_role = st.selectbox("Job Role", options=["Sales Executive", "Research Scientist", "Laboratory Technician", 
                                                 "Manager", "Sales Representative", "Research Director",
                                                 "Human Resources", "Healthcare Representative", "Manufacturing Director"])
    job_satisfaction = st.selectbox("Job Satisfaction", options=[1, 2, 3, 4], format_func=lambda x: ["Low", "Medium", "High", "Very High"][x-1])
    marital_status = st.selectbox("Marital Status", options=["Single", "Married", "Divorced"])
    relationship_satisfaction = st.selectbox("Relationship Satisfaction", options=[1, 2, 3, 4], format_func=lambda x: ["Low", "Medium", "High", "Very High"][x-1])
    stock_option_level = st.selectbox("Stock Option Level", options=[0, 1, 2, 3])
    work_life_balance = st.selectbox("Work Life Balance", options=[1, 2, 3, 4], format_func=lambda x: ["Low", "Good", "Excellent", "Outstanding"][x-1])
    performance_rating = st.selectbox("Performance Rating", options=[3, 4], format_func=lambda x: ["Excellent", "Outstanding"][x-3])  # Adjusted since min is 3

    # Submit button
    submit_button = st.form_submit_button(label="Predict")

# Prediction Logic
if submit_button:
    input_data = pd.DataFrame({
        "Age": [age],
        "DailyRate": [daily_rate],
        "DistanceFromHome": [distance_from_home],
        "Education": [education],
        "EnvironmentSatisfaction": [environment_satisfaction],
        "Gender": [gender],
        "HourlyRate": [hourly_rate],
        "JobInvolvement": [job_involvement],
        "JobLevel": [job_level],
        "JobSatisfaction": [job_satisfaction],
        "MonthlyIncome": [monthly_income],
        "MonthlyRate": [monthly_rate],
        "NumCompaniesWorked": [num_companies_worked],
        "Over18": [over_18],
        "PercentSalaryHike": [percent_salary_hike],
        "StockOptionLevel": [stock_option_level],
        "TotalWorkingYears": [total_working_years],
        "TrainingTimesLastYear": [training_times_last_year],
        "YearsAtCompany": [years_at_company],
        "YearsInCurrentRole": [years_in_current_role],
        "YearsSinceLastPromotion": [years_since_last_promotion],
        "YearsWithCurrManager": [years_with_curr_manager],
        "BusinessTravel": [business_travel],
        "Department": [department],
        "EducationField": [education_field],
        "JobRole": [job_role],
        "MaritalStatus": [marital_status],
        "OverTime": [over_time],
        "RelationshipSatisfaction": [relationship_satisfaction],
        "WorkLifeBalance": [work_life_balance],
        "PerformanceRating": [performance_rating]
    })

    prediction, prediction_prob = predict_attrition(input_data)
    if prediction is not None:
        result = "Attrition" if prediction[0] == 1 else "No Attrition"
        probability = prediction_prob[0][1] if prediction[0] == 1 else prediction_prob[0][0]

        # Display Results
        st.subheader("Prediction Result")
        st.write(f"The predicted attrition status is: **{result}**")
        st.write(f"Probability: **{probability * 100:.2f}%**")