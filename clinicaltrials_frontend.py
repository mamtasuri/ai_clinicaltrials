import streamlit as st
import modal
import json
import os


# Main Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Clinical Trials Summarizer",
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
    st.title("Clinical Trials Summarizer")
    st.subheader("Deciphering clinical trials can be challenging, but with this site, you can easily view them.")
    st.subheader("             ")
    st.subheader("             ")
    
    disease_json = None
    #with open('./heartdisease_data.json') as f:
    #    disease_json = json.load(f)    

    if search_button:
        # Call the function to get the study info for the selected disease
        output_json = process_getstudy_info(selected_disease, additional_term)
        print(json.dumps(output_json, indent=4))
        
        disease_json = output_json
    else:
        with open('./heartdisease_data.json') as f:
            disease_json = json.load(f)   

    study_index = st.session_state.get("study_index", 0)
    if st.button("Next Study"):
        study_index = (study_index + 1) % len(disease_json)
        st.session_state.study_index = study_index

    # Display the current study
    study = disease_json[study_index]
    st.subheader(f":blue[Study: {study['brief_title']}]")
    col1, col2 = st.columns([1, 2])  # Create two columns
    # Left column
    with col1:
        st.write(f"**NCT ID:** {study['nct_id']}", unsafe_allow_html=True)
        st.write(f"**Title:** {study['brief_title']}", unsafe_allow_html=True)
        st.write(f"**Status:** {study['overall_status']}", unsafe_allow_html=True)
        st.write(f"**Start Date:** {study['start_date']}", unsafe_allow_html=True)
        st.write(f"**Completion Date:** {study['completion_date']}", unsafe_allow_html=True)
        st.write(f"**Lead Sponsor:** {study['lead_sponsor']}", unsafe_allow_html=True)

    # Right column
    with col2:
        st.write("**Summary of the Study**")
        st.write(f" {study['summary']}")
 
 
def process_getstudy_info(selected_disease, additional_term):
    f = modal.Function.lookup("clinicaltrials-project", "get_study_info")
    output = f.call(selected_disease, additional_term)
    return output   

if __name__ == "__main__":
    main()
