# This is a sample Python script.
import zipfile
import data_intake as intake
import streamlit as st
import pandas as pd
import os
import database
import plotly.express as px


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
    st.title(uploaded_file.name)
    st.text(uploaded_file.type)
    if "zip" in uploaded_file.type:
        extraction_path = ""
        if "samsung" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/samsung"
        elif "renpho" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/renpho"
        elif "fitbit" in uploaded_file.name:
            extraction_path = "datasets/downloaded_data/fitbit"
        with zipfile.ZipFile(uploaded_file, "r") as z:
            z.extractall(path=extraction_path)
        intake.get_data(extraction_path)
    uploaded_file.flush()
    uploaded_file.close()




placeholder = st.empty()
try:
    with placeholder.container():
        weight_table = pd.read_sql_table(table_name='weight', con=database.get_connection())
        food_info_table = pd.read_sql_table(table_name='food_info', con=database.get_connection())
        food_intake_table = pd.read_sql_table(table_name='food_intake', con=database.get_connection())
        general_food_table = food_info_table.merge(right=food_intake_table, on=['name'], how='right')

        general_food_table = general_food_table.drop(
            columns=['metric_serving_unit', 'serving_description', 'name', 'description'],
            axis=1,
        )
        print(general_food_table.info())
        print(general_food_table.describe())
        general_food_table['start_time'] = pd.to_datetime(general_food_table['start_time'])
        general_food_table = general_food_table.resample('D', on='start_time').sum().reset_index()

        weight_table.sort_values(by=['start_time'], ascending=False, inplace=True)

        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        kpi_col1.metric(
            label='Age',
            value=33
        )
        kpi_col2.metric(
            label='Weight',
            value=round(weight_table.iloc[0]['weight'], 2),
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['weight']-weight_table.iloc[1]['weight'])/weight_table.iloc[1]['weight'],
                    2)
            )+" %"
        )
        kpi_col3.metric(
            label='Height',
            value=round(weight_table.iloc[0]['height'], 2),
        )
        kpi_col4.metric(
            label='Basal Metabolic Rate',
            value=weight_table.iloc[0]['basal_metabolic_rate'],
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['basal_metabolic_rate']-weight_table.iloc[1]['basal_metabolic_rate'])/weight_table.iloc[1]['basal_metabolic_rate'],
                    2
                )
            )+" %"
        )
        kpi_col1.metric(
            label='Skeletal Muscle Mass',
            value=round(weight_table.iloc[0]['skeletal_muscle_mass'], 2),
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['skeletal_muscle_mass']-weight_table.iloc[1]['skeletal_muscle_mass'])/weight_table.iloc[1]['skeletal_muscle_mass'],
                    2
                )
            )+" %"
        )
        kpi_col2.metric(
            label='Fat Free',
            value=round(weight_table.iloc[0]['fat_free'], 2),
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['fat_free']-weight_table.iloc[1]['fat_free'])/weight_table.iloc[1]['fat_free'],
                    2
                )
            )+" %"
        )
        kpi_col3.metric(
            label='Body Fat',
            value=round(weight_table.iloc[0]['body_fat'], 2),
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['body_fat']-weight_table.iloc[1]['body_fat'])/weight_table.iloc[1]['body_fat'],
                    2
                )
            )+" %"
        )
        kpi_col4.metric(
            label='Total Body Water',
            value=round(weight_table.iloc[0]['total_body_water'], 2),
            delta=str(
                round(
                    100 * (weight_table.iloc[0]['total_body_water']-weight_table.iloc[1]['total_body_water'])/weight_table.iloc[1]['total_body_water'],
                    2
                )
            )+" %"
        )
        graph_col1, graph_col2 = st.columns(2)

        with graph_col1:
            st.markdown("### Weight Chart")
            weight_chart = px.line(
                data_frame=weight_table, x='start_time', y='weight'
            )
            st.plotly_chart(weight_chart, use_container_width=True)

        with graph_col2:
            st.markdown("### Body Fat Chart")
            body_fat_chart = px.line(
                data_frame=weight_table, x='start_time', y='body_fat'
            )
            st.plotly_chart(body_fat_chart, use_container_width=True)
        st.markdown("### Carbs Chart")
        carbs_chart = px.line(
                data_frame=general_food_table, x='start_time', y='carbohydrate'
        )
        carbs_chart.add_hline(y=25)
        st.plotly_chart(carbs_chart, use_container_width=True)

        st.write(general_food_table)
except:
    st.markdown("# NO DATA YET PLEASE UPLOAD USING THE SIDEBAR BROWSE FILES BUTTON! ")
