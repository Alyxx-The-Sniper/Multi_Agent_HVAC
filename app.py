import streamlit as st
import agents
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Rosegold HVAC Design Engineering Department",
    page_icon="❄️",
    layout="wide"
)


# --- Background Image ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1721549369164-2fd07f795ce4?q=80&w=717&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --- Page Title ---
st.title("Rosegold HVAC Design Workflow ❄️")
st.caption(f"📍 Location: Antipolo City, Philippines | 📅 Date: {datetime.now().strftime('%B %d, %Y')}")

# --- Input Form ---
st.header("1. Enter Project Data")
st.info("Describe the area's conditions. The more detail you provide, the more accurate the AI's calculation will be.")

with st.form(key="hvac_form"):
    col1, col2 = st.columns(2)

    with col1:
        project_name = st.text_input("Project Name", "Commercial Office Space")
        length = st.number_input("Room Length (meters)", min_value=1.0, value=15.0)
        width = st.number_input("Room Width (meters)", min_value=1.0, value=10.0)
        height = st.number_input("Room Height (meters)", min_value=2.0, value=3.0)
        occupants = st.number_input("Max Number of Occupants", min_value=1, value=12)

    with col2:
        # Replace specific inputs with a single text area
        area_conditions = st.text_area(
            "Area Conditions & Remarks",
            "e.g., The roof is made of galvanized iron insulated in foam. The walls are made of concrete cement. The west-facing wall is all glass (single-pane). The other walls are concrete. Standard office lighting and 12 workstations with computers. No special heat-generating equipment.",
            height=220
        )

    submit_button = st.form_submit_button(label=" 🛰️ Generate HVAC Design")

# --- Agent Processing and Output ---
if submit_button:
    st.header("2. Agent Analysis & Reports")
    # Format the input data string with the new remarks field
    report_data = f"""
- **Project Name:** {project_name}
- **Room Dimensions (L x W x H):** {length}m x {width}m x {height}m
- **Total Floor Area:** {length * width:.2f} sq. m.
- **Occupancy:** {occupants} persons
- **Area Conditions & Remarks:** {area_conditions}
"""
    # The rest of the agent calling logic remains the same
    with st.spinner('Agent 1 (OpenAI) and Agent 2 (Kimi) are drafting proposals...'):
        report_1 = agents.get_openai_report(report_data)
        report_2 = agents.get_kimi_report(report_data)

    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📄 **Agent 1: OpenAI's Proposal**", expanded=True):
            st.markdown(report_1)

    with col2:
        with st.expander("📄 **Agent 2: Kimi's Proposal**", expanded=True):
            st.markdown(report_2)

    st.header("3. Final Approved Report")
    with st.spinner('Agent 3 (Head Engineer Gemini) is reviewing and finalizing the report...'):
        final_report = agents.get_gemini_final_report(
            report_data=report_data,
            report_1=report_1,
            report_2=report_2
        )
        st.markdown(final_report)
        st.success("✅ Final report generated and ready for quotation!")