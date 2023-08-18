import streamlit as st
import modal
import json
import os


# Sample clinical trial data
sample_data = [
    {
        "NCTId": "NCT001",
        "BriefTitle": "Sample Trial 1",
        "OverallStatus": "Recruiting",
        "StartDate": "2023-05-01",
        "PrimaryCompletionDate": "2023-12-31",
        "CompletionDate": "2024-01-15",
        "LeadSponsorName": "Sample Sponsor A",
        "Outcome": "Positive",
        "Hypothesis": "Teleconsultation improves patient outcomes"
    },
    {
        "NCTId": "NCT002",
        "BriefTitle": "Sample Trial 2",
        "OverallStatus": "Completed",
        "StartDate": "2022-10-01",
        "PrimaryCompletionDate": "2023-03-31",
        "CompletionDate": "2023-04-15",
        "LeadSponsorName": "Sample Sponsor B",
        "Outcome": "Negative",
        "Hypothesis": "Teleconsultation has no effect on patient outcomes"
    }
]

# Main Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Clinical Trials Viewer",
        page_icon="💊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar inputs
    disease_menu = [
        "Cancer", "Diabetes", "Heart Disease", "COVID-19", "Asthma", 
        "Depression", "Obesity", "Alzheimer's", "Hypertension", "Arthritis",
        "Stroke", "Migraine", "Parkinson's", "HIV/AIDS", "Influenza", 
        "Epilepsy", "Allergies", "Osteoporosis", "Thyroid", "Anemia"
    ]

    # Sidebar for user input
    st.sidebar.title("Search Clinical Trials")
    selected_disease = st.sidebar.selectbox("Select a Disease or Enter One", [""] + disease_menu)
    additional_term = st.sidebar.text_input("Additional Term", "")
    search_button = st.sidebar.button("Search")

    # Display search results
    st.title("Clinical Trials Viewer")
    st.subheader("Deciphering clinical trials can be challenging, but with this site, you can easily view them.")

    
    study_index = st.session_state.get("study_index", 0)
    if st.button("Next Study"):
        study_index = (study_index + 1) % len(sample_data)
        st.session_state.study_index = study_index

    # Display the current study
    study = sample_data[study_index]
    st.subheader(f"{study['BriefTitle']}")
    col1, col2 = st.columns([1, 2])  # Create two columns
    # Left column
    with col1:
        st.write(f"**NCT ID:** {study['NCTId']}", unsafe_allow_html=True)
        st.write(f"**Title:** {study['BriefTitle']}", unsafe_allow_html=True)
        st.write(f"**Status:** {study['OverallStatus']}", unsafe_allow_html=True)
        st.write(f"**Start Date:** {study['StartDate']}", unsafe_allow_html=True)
        st.write(f"**Primary Completion Date:** {study['PrimaryCompletionDate']}", unsafe_allow_html=True)
        st.write(f"**Completion Date:** {study['CompletionDate']}", unsafe_allow_html=True)
        st.write(f"**Lead Sponsor:** {study['LeadSponsorName']}", unsafe_allow_html=True)

    # Right column
    with col2:
        st.write(f"**Outcome:** {study['Outcome']}", unsafe_allow_html=True)
        st.write(f"**Hypothesis:** {study['Hypothesis']}", unsafe_allow_html=True)
        if study['Outcome'] == "Positive" and "improves" in study['Hypothesis']:
            st.write("🟢 Hypothesis Supported", unsafe_allow_html=True)
        elif study['Outcome'] == "Negative" and "improves" in study['Hypothesis']:
            st.write("🔴 Hypothesis Not Supported", unsafe_allow_html=True)
        else:
            st.write("❓ Outcome and Hypothesis Mismatch", unsafe_allow_html=True) 
    

if __name__ == "__main__":
    main()
