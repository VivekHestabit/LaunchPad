
import streamlit as st  

import requests

st.set_page_config(
    page_title="Titanic Survival Prediction Page ",
    layout = "centered"
)

st.title("Tital Survival Prediction Page")
st.write("Enter the passenger details to know the survival prediction ")


st.divider()

age = st.number_input(
    "Age",
    min_value=0.0,
    value=25.0
)

sex = st.selectbox(
    "Sex", 
    ["male", "Female"]
)

pclass = st.selectbox(
    "Passenger Class",
    [1, 2, 3]
)

fare = st.number_input(
    "Fare",
    min_value=0.0,
    value=10.0
)

sibsp = st.number_input(
    "Number of Siblings / Spouses (SibSp)",
    min_value=0,
    step=1
)

parch = st.number_input(
    "Number of Parents / Children (Parch)",
    min_value=0,
    step=1
)

embarked = st.selectbox(
    "Embarked Port",
    ["C", "Q", "S"]
)

if st.button ("Predict Survival "):
    payload = {
        "Age" : age,
        "Sex" : sex,
        "Pclass" : pclass,
        "Fare" : fare,
        "SibSp" : sibsp,
        "Parch" : parch,
        "Embarked" : embarked
    }
    
    try:
        
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload
        )
        
        if response.status_code == 200:
            result = response.json()
            
            st.success("Prediction Successfull")
            st.json(result)
            
        else:
            st.error("API returned an error : ")
            st.write(response.text)
            
            
    except Exception as e : 
        st.error("Cannot be Able to Connect to the API")
        st.write(str(e))