# This is a sample Python script.

import streamlit as st
import pandas as pd
import database
import plotly.express as px
import traceback
import sys


st.set_page_config(
    page_title="Personal Health Dashboard",
    page_icon="✅",
    layout="wide",
)

st.sidebar.subheader("Dashboard Controls")
st.title('Health Control Panel')

tabs = st.tabs(["metrics", "plots", "reports"])
try:

    with tabs[0]:
        weight_table = pd.read_sql_table(table_name='weight', con=database.get_connection())
        weight_table = weight_table[(weight_table['date'] > '2023-01-01')]
        general_food_table = pd.read_sql_table(table_name='general_food_table', con=database.get_connection())
        general_food_table = general_food_table[(general_food_table['start_time'] > '2023-01-01')]
        general_food_table.sort_values(by=['start_time'], ascending=False, inplace=True)
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
            label='Last Average Weekly Carb',
            value=round(general_food_table.iloc[0]['carbohydrate'], 2),
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

        st.markdown("Daily Report Table")
        st.write(pd.read_sql_table(table_name='daily_report', con=database.get_connection()))
except:
    traceback.print_exception(*sys.exc_info())
    st.markdown("# NO DATA YET PLEASE UPLOAD USING THE SIDEBAR BROWSE FILES BUTTON! ")
