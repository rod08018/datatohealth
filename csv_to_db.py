# This is a sample Python script.
import zipfile
import data_intake as intake
import streamlit as st
import os


def create_dirs(path: str):
    try:
        os.mkdir(path)
    except FileExistsError:
        print(path + " path already exist")


st.set_page_config(
    page_title="Personal Health Dashboard",
    page_icon="✅",
    layout="wide",
)

st.sidebar.subheader("Dashboard Controls")
st.title('Health Control Panel')
if not os.path.exists('datasets') or not os.path.exists('datasets/downloaded_data'):
    create_dirs('datasets')
    create_dirs('datasets/downloaded_data')
    create_dirs('datasets/downloaded_data/renpho')
    create_dirs('datasets/downloaded_data/samsung')
    create_dirs('datasets/downloaded_data/fitbit')

uploaded_file = st.sidebar.file_uploader(
    label="Select your data",
    type=['zip'],
    accept_multiple_files=False,
    key="fileUploader"
)

if uploaded_file is not None:

    if "zip" in uploaded_file.type:
        extraction_path = ""
        if "samsung" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/samsung"
        elif "renpho" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/renpho"
        elif "fitbit" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/fitbit"
        with zipfile.ZipFile(uploaded_file, "r") as z:
            print(extraction_path)
            z.extractall(path=extraction_path)
        intake.get_data(extraction_path)
    uploaded_file.flush()
    uploaded_file.close()
