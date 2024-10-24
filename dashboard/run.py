import streamlit as st
import plotly.express as px
import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
from database.extract_db import *
import plotly.graph_objects as go

warnings.filterwarnings("ignore")
NICK = "@batata doce"

# ==== Set the Dashboard ====
st.set_page_config(page_title="CS1.6 Analytics", page_icon=":bar_chart:", layout="wide",
                   initial_sidebar_state="expanded")
st.title(" :bar_chart: CS1.6 Analytics")
st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# Load data
data = get_kill_events()

# ==== Events Filters ====
# Dates
col1, col2 = st.columns(2)
data["ts"] = pd.to_datetime(data["ts"])
start_date = pd.to_datetime(data["ts"]).min()
end_date = pd.to_datetime(data["ts"]).max() + timedelta(days=1)

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", start_date))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", end_date))

data = data[(data["ts"] >= date1) & (data["ts"] <= date2)].copy()

# Sidebar filters
st.sidebar.header("Filter Events By: ")
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

# ==== Events and KDR ==== #
col1, col2, col3 = st.columns(3)
with col2:
    st.subheader("Kills - Deaths Ratio (KDR)")
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
    fig = px.pie(df_melted, values="number", names="type", hole=0.5,
                 color_discrete_sequence=[color_map[type] for type in df_melted['type'].unique()])
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
            x=-0.02
        )
    )

    fig.update_traces(text=[""], textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with col3:
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

with col1:
    st.subheader('Events')
    columns_to_keep = ['ts', 'killer_name', 'victim_name', 'weapon', 'distance', 'headshot']
    filtered_data3 = filtered_data3.sort_values(by='ts', ascending=False).reset_index(drop=True)
    st.dataframe(filtered_data3[columns_to_keep])

# ==== Kills/Deaths by Weapon ====
st.write("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Kills by Weapon")
    # Get the data
    df_weapons = kills_by_weapon()

    # Plot the data
    fig_weapons = px.bar(df_weapons, x='Weapon', y='Kills', color='Kills',
                         color_continuous_scale=['#FFCCCC', '#FF6666', '#FF2B4B', '#990000'])
    fig_weapons.update_layout(showlegend=False)

    # Display the chart
    st.plotly_chart(fig_weapons, use_container_width=True)

with col2:
    st.subheader("Deaths by Weapon")
    # Get the data
    df_weapons2 = deaths_by_weapon()

    # Plot the data
    fig_weapons2 = px.bar(df_weapons2, x='Weapon', y='Deaths', color='Deaths',
                          color_continuous_scale=['#FFCCCC', '#FF6666', '#FF2B4B', '#990000'])
    fig_weapons2.update_layout(showlegend=False)

    # Display the chart
    st.plotly_chart(fig_weapons2, use_container_width=True)

# ==== Kills/Deaths by Distance on the same plot ====
st.write("---")
col1, col2 = st.columns(2)

# Left Column - Combined Kills, Deaths, and Headshots per Distance
with col1:
    st.subheader("Kills(+Headshots)/Deaths by Distance")
    # Fetch data
    df_kills_distance = kills_by_distance()
    df_kills_distance = df_kills_distance.dropna()  # Remove NaN values
    df_deaths_distance = deaths_by_distance()
    df_deaths_distance = df_deaths_distance.dropna()  # Remove NaN values
    headshots_df = headshots_by_distance()

    # Merge kills and deaths DataFrames on distance
    df_combined = pd.merge(df_kills_distance, df_deaths_distance, on='distance', how='left')

    # Fill missing deaths with 0
    df_combined['deaths'] = df_combined['deaths'].fillna(0)

    # Merge headshot data into the combined dataframe
    df_combined = pd.merge(df_combined, headshots_df, left_on='distance', right_on='Distance', how='left')
    df_combined['Headshot_Count'] = df_combined['Headshot_Count'].fillna(0)  # Fill missing headshots with 0

    # Calculate performance score (kills - deaths)
    df_combined['performance'] = df_combined['kills'] - df_combined['deaths']

    # Find the best distance based on the highest performance score
    best_distance = df_combined.loc[df_combined['performance'].idxmax(), 'distance']
    best_kills = df_combined.loc[df_combined['performance'].idxmax(), 'kills']
    best_deaths = df_combined.loc[df_combined['performance'].idxmax(), 'deaths']

    # Create a combined figure with kills, deaths, and headshots
    fig_combined = px.line()

    # Add Kills per Distance trace
    fig_combined.add_scatter(
        x=df_combined['distance'],
        y=df_combined['kills'],
        mode='lines+markers',
        name='Kills',
        line_shape='spline',
        line=dict(color='#FF2B4B'),
        marker=dict(color='#FF2B4B', symbol='cross')
    )

    # Add Deaths per Distance trace
    fig_combined.add_scatter(
        x=df_combined['distance'],
        y=df_combined['deaths'],
        mode='lines+markers',
        name='Deaths',
        line_shape='spline',
        line=dict(color='#FF6347'),
        marker=dict(color='#FF6347')
    )

    # Add Headshots per Distance trace (scatter line)
    fig_combined.add_scatter(
        x=df_combined['distance'],
        y=df_combined['Headshot_Count'],
        mode='lines',
        name='Headshots',
        line_shape='spline',
        line=dict(color='#FB1B43', width=1, dash='5px,2px'),  # Thin and dashed line
        marker=dict(color='#FB1B43')
    )

    # Highlight the best distance with a marker
    fig_combined.add_scatter(
        x=[best_distance],
        y=[best_kills],
        mode='markers',
        marker=dict(color='#FF2B4B', size=12, symbol='cross'),
        name='Best Distance'
    )

    # Show the plot in the Streamlit app
    st.plotly_chart(fig_combined)



# ==== Kills/Deaths avg distance per weapon ====
with col2:
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
        height=500,
        margin=dict(l=150, r=50, t=50, b=50),
        xaxis_title="Distance",
        yaxis_title="Weapon",
        font=dict(size=12),
        legend=dict(x=0, y=1.1, orientation='h')  # Position the legend above the chart
    )

    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

# ==== Headshot total ratio ==== #
st.write("---")
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Headshot Ratio")
    headshot_count, non_headshot_count = total_headshot()
    data = {
        'Type': ['Headshots', 'Non-Headshots'],
        'Count': [headshot_count, non_headshot_count]
    }
    df = pd.DataFrame(data)

    # Create a pie chart
    fig = px.pie(
        df,
        names='Type',
        values='Count',
        color='Type',
        color_discrete_map={'Headshot': '#FF1B4B', 'Non-Headshot': '#FB2E4B'},
        labels={'Type': 'Headshot Type', 'Count': 'Count'}
    )
    # Update layout to position the legend on the left
    fig.update_layout(
        legend=dict(
            x=-0.2,  # Adjust x position for legend
            y=0.5,  # Center the legend vertically
            traceorder='normal',
            orientation='v'
        )
    )
    # Customize the text inside the pie chart
    fig.update_traces(
        textinfo='percent',  # Show both percentage and label
        insidetextfont=dict(size=26),  # Increase the font size of the text inside the pie
        textfont=dict(size=25, family='Courier New')  # Increase the font size of the percentage labels
    )
    st.plotly_chart(fig)

# ==== Headshot Rate for 3 major weapons - default last 10 days ====
with col2:
    st.subheader("Headshot Rate Over Time - By Weapon")
    weapons = ('m4a1', 'ak47', 'deagle')
    df = headshot_by_weapon(weapons)

    # Get the max and min dates from the data
    max_date = df['Date'].max()
    min_date = df['Date'].min()

    # Set default start and end dates to display the last 10 days
    default_start_date = max_date - pd.Timedelta(days=20)
    default_end_date = max_date

    col2_1, col2_2 = st.columns(2)

    # Allow the user to pick start and end dates, defaulting to the last 10 days
    start_date = col2_1.date_input("Start Date", default_start_date, min_value=min_date, max_value=max_date, key='start_date')
    end_date = col2_2.date_input("End Date", default_end_date, min_value=min_date, max_value=max_date, key='end_date')

    # Filter the data based on selected (or default) date range
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Create the plot
    fig = px.line(filtered_df, x='Date', y='Headshot_Ratio', color='Weapon',
                  color_discrete_map={'m4a1': '#FF2B4B', 'ak47': '#7F1B4B', 'deagle': '#FF9F7F'},
                  markers=True)

    # Customize the line style
    fig.update_traces(line=dict(dash='dash', width=2),  # Dashed line
                      marker=dict(size=8, symbol='x'))

    # Update layout for better readability
    fig.update_layout(
        xaxis_title='Date',
        xaxis=dict(
            title="Date",
            tickmode='linear',
            dtick="D",  # Interval set to one day
            tickformat="%Y-%m-%d"),
        yaxis_title='Headshot Ratio',
        yaxis=dict(range=[0, 1]),  # Ensure y-axis ranges from 0 to 1
        legend_title='Weapon'
    )

    # Display the plot
    st.plotly_chart(fig)



