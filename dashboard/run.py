import streamlit as st
import plotly.express as px
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
from database.extract_db import get_kill_events, killer_victim_ratio,kills_by_weapon,deaths_by_weapon,kills_by_distance,deaths_by_distance,avg_death_distance_per_weapon, avg_kill_distance_per_weapon
import plotly.graph_objects as go

# ==== To run this file : python -m streamlit run dashboard/run.py (from parent dir)


warnings.filterwarnings("ignore")
NICK = "@batata doce"


# ==== set the Dashboard ====
st.set_page_config(page_title="CS 1.6 Analysis", page_icon=":bar_chart:", layout="wide",
    initial_sidebar_state="expanded")
st.title(" :bar_chart: CS 1.6 Analysis")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Load data
data = get_kill_events()

# date range filter
col1, col2 = st.columns((2))
data["ts"] = pd.to_datetime(data["ts"])

# Getting the min and max date
start_date = pd.to_datetime(data["ts"]).min()
end_date = pd.to_datetime(data["ts"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", end_date))

data = data[(data["ts"] >= date1) & (data["ts"] <= date2)].copy()

# ==== Filters ====
#st.sidebar.image("image.png")
st.sidebar.header("Filter By: ")

killer = st.sidebar.multiselect("Pick Killer", data["killer_name"].unique())
if not killer:
    filtered_data = data.copy()
else:
    filtered_data = data[data["killer_name"].isin(killer)]

victim = st.sidebar.multiselect("Pick Victim", filtered_data["victim_name"].unique())
if not victim:
    filtered_data2 = filtered_data.copy()
else:
    filtered_data2 = filtered_data[filtered_data["victim_name"].isin(victim)]


weapon = st.sidebar.multiselect("Pick Weapon", filtered_data2["weapon"].unique())
if not weapon:
    filtered_data3 = filtered_data2.copy()
else:
    filtered_data3 = filtered_data2[filtered_data2["weapon"].isin(weapon)]


# Display the whole table 'kill_events'
st.header('Events')
st.dataframe(filtered_data3)



col1, col2 = st.columns(2)
# 1 Left Column - kills/deaths ratio
with col1:
    result = killer_victim_ratio()
    kills = result[0][0]
    deaths = result[0][1]
    ratio = kills / deaths if kills != 0 else 0

    # Convert to DataFrame
    df = pd.DataFrame(result, columns=['kills', 'deaths'])

    # Melt the DataFrame to have 'type' and 'number' columns
    df_melted = df.melt(var_name='type', value_name='number')
    df_melted['type'] = df_melted['type'].replace({'kills': 'Kills', 'deaths': 'Deaths'})


    color_map = {"Kills": "#FF2B4B", "Deaths": "#7F1B4B"}
    st.subheader("Kills - Deaths Ratio")
    fig = px.pie(df_melted, values="number", names="type", hole=0.5, color_discrete_sequence=[color_map[type] for type in df_melted['type'].unique()])
    fig.add_annotation(
        text=f"1  :  {ratio:.2f}",
        showarrow=False,
        font=dict(size=14),
        x=0.5, y=0.5,
        xref="paper", yref="paper"
    )
    # Update layout to position the legend on the left
    fig.update_layout(
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=-0.1
        )
    )

    fig.update_traces(text=[""], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Kills vs Deaths (Absolute Numbers)")
    fig_bar = px.bar(df_melted, x='type', y='number', color='type',
                     color_discrete_map={"Kill": "#FF2B4B", "Death": "#7F1B4B"},
                     labels={'number': 'Count', 'type': 'Type'}, text='number')
    fig_bar.update_layout(showlegend=False,
                          yaxis=dict(title='Count'),
                          xaxis=dict(title=''),
                          height=400,  # Set the same height as the pie chart
                          margin=dict(l=10, r=10, t=50, b=10))
    fig_bar.update_traces(texttemplate='%{text}', textposition='inside')
    st.plotly_chart(fig_bar, use_container_width=True)

# ==== Kills by Weapon ====
st.write("---")
st.subheader("Kills by Weapon")
# Get the data
df_weapons = kills_by_weapon()

# Plot the data
fig_weapons = px.bar(df_weapons, x='Weapon', y='Kills', color='Kills', color_continuous_scale=['#FFCCCC', '#FF6666', '#FF2B4B', '#990000'])
fig_weapons.update_layout(showlegend=False)

# Display the chart
st.plotly_chart(fig_weapons, use_container_width=True)


# ==== Deaths by Weapon ====

st.subheader("Deaths by Weapon")
# Get the data
df_weapons2 = deaths_by_weapon()

# Plot the data
fig_weapons2 = px.bar(df_weapons2, x='Weapon', y='Deaths', color='Deaths', color_continuous_scale=['#FFCCCC', '#FF6666', '#FF2B4B', '#990000'])
fig_weapons2.update_layout(showlegend=False)

# Display the chart
st.plotly_chart(fig_weapons2, use_container_width=True)

# ==== Kills/Deaths by distance ====
st.write("---")
col1, col2 = st.columns(2)


# Left Column - Kills per Distance
with col1:
    df_kills_distance = kills_by_distance()
    df_kills_distance = df_kills_distance.dropna()  # Remove NaN values
    st.subheader("Kills per Distance")
    fig_kills_distance = px.line(
        df_kills_distance,
        x='distance',
        y='kills',
        markers=True,
        line_shape="spline"
    )
    fig_kills_distance.update_traces(line_color='#FF2B4B', marker=dict(color='#FF2B4B'))
    fig_kills_distance.update_yaxes(range=[0, df_kills_distance['kills'].max() * 1.1])
    st.plotly_chart(fig_kills_distance, use_container_width=True)

# Right Column - Deaths per Distance
with col2:
    df_deaths_distance = deaths_by_distance()
    df_deaths_distance = df_deaths_distance.dropna()  # Remove NaN values
    st.subheader("Deaths per Distance")
    fig_deaths_distance = px.line(
        df_deaths_distance,
        x='distance',
        y='deaths',
        markers=True,
        line_shape="spline"
    )
    fig_deaths_distance.update_traces(line_color='#FF6347', marker=dict(color='#FF6347'))
    fig_deaths_distance.update_yaxes(range=[0, df_deaths_distance['deaths'].max() * 1.1])
    st.plotly_chart(fig_deaths_distance, use_container_width=True)


# ==== Kills/Deaths avg distance per weapon
st.write("---")
st.subheader("Average Kill/Death Distance per Weapon")
# Custom reddish color scale
kills_df = avg_kill_distance_per_weapon()
deaths_df = avg_death_distance_per_weapon()

# Merge the DataFrames on 'Weapon'
df_combined = pd.merge(kills_df, deaths_df, on='Weapon', how='outer').fillna(0)

# Create an overlayed horizontal bar plot
fig = go.Figure()

# Add kills bars
fig.add_trace(go.Bar(
    y=df_combined['Weapon'],
    x=df_combined['Avg_Kill_Distance'],
    name='Average Kill Distance',
    orientation='h',
    marker_color='#FF2B4B',
    opacity=0.7
))

# Add deaths bars
fig.add_trace(go.Bar(
    y=df_combined['Weapon'],
    x=df_combined['Avg_Death_Distance'],
    name='Average Death Distance',
    orientation='h',
    marker_color='#FF9999',
    opacity=0.7
))

# Update layout for better readability
fig.update_layout(
    barmode='group',  # Side-by-side bars for kills and deaths
    height=600,
    margin=dict(l=150, r=50, t=50, b=50),
    xaxis_title="Distance",
    yaxis_title="Weapon",
    font=dict(size=12),
    legend=dict(x=0, y=1.1, orientation='h')  # Position the legend above the chart
)

# Display the chart
st.plotly_chart(fig, use_container_width=True)


