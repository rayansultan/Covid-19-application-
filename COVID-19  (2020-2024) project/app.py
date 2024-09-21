import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import plotly.express as px
import pydeck as pdk 
df = pd.read_csv("COVID-19-global-data.csv", encoding='ISO-8859-1')
#df['Date_reported'] = pd.to_datetime(df['Date_reported'])  # Ensure correct datetime format
#df['year_report'] = df['Date_reported'].dt.year
st.title("COVID-19 Dashboard")
st.subheader("Cases and Deaths Across Regions from 2019 to 2024")
st.markdown("Source table can be found [here](https://www.kaggle.com/datasets/abdoomoh/daily-covid-19-data-2020-2024)")
with st.expander("See full data table"):
    st.dataframe(df)
with st.form("Covid-19-form"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Select WHO Region:")
        region = st.selectbox("WHO Region", df['WHO_region'].unique(), key="who_region")
        st.write("Select a Country :")
        country = st.selectbox("Countries", df[df['WHO_region'] == region]['Country'].unique(), key="countries")
        #end_year = st.slider("Year", min_value=1991, max_value=2023, value=2023, step=1, key="end_y")
        
    with col2:
     st.write("Choose a starting date")
     start_year = st.slider("Year", min_value=2019, max_value=2024, value=2019, step=1, key="start_y")
     st.write("Choose an end date")
     end_year = st.slider("Year", min_value=2019, max_value=2024, value=2024, step=1, key="end_y")

    submit_btn = st.form_submit_button("Analyze", type="primary")

start_date = f" {start_year}"
end_date = f" {end_year}"
def end_before_start(start_date, end_date):
    if start_date > end_date:
        return True
    else:
        return False

filtered_df = df[
    (df['WHO_region'] == region) &
    (df['Country'] == country) &
    (df['year_report'] >= start_year) &
    (df['year_report'] <= end_year)
]

# Display filtered results in the first tab
tab1, tab2, tab3,tab4 = st.tabs(["Cases and Death", " Line Charts", "Compare according to Bar Charts","Compare according to Pie Charts"])

with tab1:
    st.subheader(f"COVID-19 Data for {country} in {start_year}-{end_year}")
    cl1,cl2=st.columns(2)
    # Display new cases, cumulative cases, new deaths, and cumulative deaths
    if not filtered_df.empty:
        
        
               initial_new_cases = filtered_df.loc[filtered_df['year_report'].idxmin(), 'New_cases']
               final_new_cases = filtered_df.loc[filtered_df['year_report'].idxmax(), 'New_cases']
               initial_cumulative_cases = filtered_df.loc[filtered_df['year_report'].idxmin(), 'Cumulative_cases']
               final_cumulative_cases = filtered_df.loc[filtered_df['year_report'].idxmax(), 'Cumulative_cases']
        
        # Get initial and final values for new and cumulative deaths
               initial_new_deaths = filtered_df.loc[filtered_df['year_report'].idxmin(), 'New_deaths']
               final_new_deaths = filtered_df.loc[filtered_df['year_report'].idxmax(), 'New_deaths']
               initial_cumulative_deaths = filtered_df.loc[filtered_df['year_report'].idxmin(), 'Cumulative_deaths']
               final_cumulative_deaths = filtered_df.loc[filtered_df['year_report'].idxmax(), 'Cumulative_deaths']
        
        # Calculate percentage changes
               percent_change_new_cases = round((final_new_cases - initial_new_cases) / initial_new_cases * 100, 2) if initial_new_cases != 0 else 0
               percent_change_cumulative_cases = round((final_cumulative_cases - initial_cumulative_cases) / initial_cumulative_cases * 100, 2) if initial_cumulative_cases != 0 else 0
               percent_change_new_deaths = round((final_new_deaths - initial_new_deaths) / initial_new_deaths * 100, 2) if initial_new_deaths != 0 else 0
               percent_change_cumulative_deaths = round((final_cumulative_deaths - initial_cumulative_deaths) / initial_cumulative_deaths * 100, 2) if initial_cumulative_deaths != 0 else 0
        
        # Display the metrics with percentage change
               col1, col2 = st.columns(2)
        
               with col1:
                st.metric(label=f"New Cases in {country} ({start_year}-{end_year})", value=f"{final_new_cases:,}", delta=f"{percent_change_new_cases}%")
                st.metric(label=f"Cumulative Cases in {country} ({start_year}-{end_year})", value=f"{final_cumulative_cases:,}", delta=f"{percent_change_cumulative_cases}%")
        
               with col2:
                 st.metric(label=f"New Deaths in {country} ({start_year}-{end_year})", value=f"{final_new_deaths:,}", delta=f"{percent_change_new_deaths}%")
                 st.metric(label=f"Cumulative Deaths in {country} ({start_year}-{end_year})", value=f"{final_cumulative_deaths:,}", delta=f"{percent_change_cumulative_deaths}%")

with tab2:
    st.header("Line Charts")

    clmn1, clmn2 = st.columns(2)

    with clmn1:
        if len(filtered_df) > 1:
            fig1, ax1 = plt.subplots()
            ax1.plot(filtered_df['year_report'], filtered_df['Cumulative_cases'], label='Cumulative Cases', color='blue')
            ax1.set_xlabel('Year')
            ax1.set_ylabel('Cumulative Cases')
            ax1.set_title('Cumulative Cases Over Time')
            ax1.legend()
            ax1.set_xticks(filtered_df['year_report'].unique())
            ax1.tick_params(axis='x', rotation=45)
            st.pyplot(fig1)

            fig3, ax3 = plt.subplots()
            ax3.plot(filtered_df['year_report'], filtered_df['New_cases'], label='New Cases', color='green')
            ax3.set_xlabel('Year')
            ax3.set_ylabel('New Cases')
            ax3.set_title('New Cases Over Time')
            ax3.legend()
            ax3.set_xticks(filtered_df['year_report'].unique())
            ax3.tick_params(axis='x', rotation=45)
            st.pyplot(fig3)
        else:
            st.write("Not enough data points for plotting.")

    with clmn2:
        if len(filtered_df) > 1:
            fig2, ax2 = plt.subplots()
            ax2.plot(filtered_df['year_report'], filtered_df['Cumulative_deaths'], label='Cumulative Deaths', color='red')
            ax2.set_xlabel('Year')
            ax2.set_ylabel('Cumulative Deaths')
            ax2.set_title('Cumulative Deaths Over Time')
            ax2.legend()
            ax2.set_xticks(filtered_df['year_report'].unique())
            ax2.tick_params(axis='x', rotation=45)
            st.pyplot(fig2)

            fig4, ax4 = plt.subplots()
            ax4.plot(filtered_df['year_report'], filtered_df['New_deaths'], label='New Deaths', color='orange')
            ax4.set_xlabel('Year')
            ax4.set_ylabel('New Deaths')
            ax4.set_title('New Deaths Over Time')
            ax4.legend()
            ax4.set_xticks(filtered_df['year_report'].unique())
            ax4.tick_params(axis='x', rotation=45)
            st.pyplot(fig4)
        else:
            st.write("Not enough data points for plotting.")

# Bar charts in tab2
with tab3:
    st.header("Bar Charts by WHO Region")

    # Multiselect for countries
    selected_countries = st.multiselect("Choose cRegions you want :", options=df["WHO_region"].unique(), default=filtered_df["WHO_region"].unique())

    # Filter dataset by selected countries
    filtered_by_country = df[df['WHO_region'].isin(selected_countries)]

    # Group by region and sum cases and deaths
    region_cases = filtered_by_country.groupby('WHO_region')['Cumulative_cases'].sum().reset_index()
    region_deaths = filtered_by_country.groupby('WHO_region')['Cumulative_deaths'].sum().reset_index()

    # Plot bar chart for cases
    st.subheader("Cumulative Cases by Region")
    fig5, ax5 = plt.subplots()
    ax5.bar(region_cases['WHO_region'], region_cases['Cumulative_cases'], color='blue')
    ax5.set_xlabel('Region')
    ax5.set_ylabel('Cumulative Cases')
    ax5.set_title('Cumulative Cases by Region')
    plt.xticks(rotation=45)
    st.pyplot(fig5)

    # Plot bar chart for deaths
    st.subheader("Cumulative Deaths by Region")
    fig6, ax6 = plt.subplots()
    ax6.bar(region_deaths['WHO_region'], region_deaths['Cumulative_deaths'], color='red')
    ax6.set_xlabel('Region')
    ax6.set_ylabel('Cumulative Deaths')
    ax6.set_title('Cumulative Deaths by Region')
    plt.xticks(rotation=45)
    st.pyplot(fig6)

#
with tab4:
    st.header("COVID-19 Cases and Deaths Pie Charts")
    
    # Multiselect for countries
    selected_countries = st.multiselect("Choose countries", options=df["Country"].unique(), default=filtered_df["Country"].unique())

    # Check if any countries are selected
    if selected_countries:
        # Filter dataset by selected countries
        filtered_by_country = df[df['Country'].isin(selected_countries)]

        # Group by country and sum cases and deaths
        country_cases = filtered_by_country.groupby('Country')['Cumulative_cases'].sum().reset_index()
        country_deaths = filtered_by_country.groupby('Country')['Cumulative_deaths'].sum().reset_index()

        # Plot pie chart for cases
        st.subheader("Cumulative Cases by Country")
        if not country_cases.empty:
            fig_cases = plt.figure(figsize=(3, 3))
            
            plt.pie(country_cases['Cumulative_cases'], labels=country_cases['Country'], autopct='%1.1f%%', startangle=140,textprops={'fontsize': 5})
            plt.title('Cumulative Cases Distribution',fontsize=6)
            st.pyplot(fig_cases)
        else:
            st.write("No data available for selected countries.")

        # Plot pie chart for deaths
        st.subheader("Cumulative Deaths by Country")
        if not country_deaths.empty:
            fig_deaths = plt.figure(figsize=(3, 3))
            plt.pie(country_deaths['Cumulative_deaths'], labels=country_deaths['Country'], autopct='%1.1f%%', startangle=140,textprops={'fontsize': 5})
            plt.title('Cumulative Deaths Distribution',fontsize=6)
            st.pyplot(fig_deaths)
        else:
            st.write("No data available for selected countries.")
    else:
        st.write("Please select at least one country.")
