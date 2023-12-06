import streamlit as st
import pandas as pd
import io
import zipfile
from operator import index
import streamlit as st
import plotly.express as px
import ts as ts
from pycaret.regression import setup, compare_models, pull, save_model, load_model
import pandas_profiling
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.ticker as tck

with st.sidebar:
    st.image("whether.gif")
    st.title("Whether App Prediction")
    choice = st.radio("Navigation",
                      ["Upload", "Profiling", "Sorted Data Frame", "Extreme  Climate Years", "Graph", "City-Graph",
                       "Min&Max Temp", "Finding the temperature trends over years", "yearly average Temperatures"])
    st.info("Explore weather trends effortlessly with our Streamlit app. View raw data, analyze monthly and yearly average temperatures, track temperature movements, and assess monthly rainfall. Use the dropdown to select a city and delve into insightful weather patterns. Streamlined, interactive, and informative.")

if choice == "Upload":
    uploaded_file = st.file_uploader("Upload a ZIP file containing CSV files", type="zip")
    if uploaded_file is not None:
        # Unzip the uploaded file
        with zipfile.ZipFile(io.BytesIO(uploaded_file.read()), 'r') as z:
            # Iterate over files in the zip file
            for file_info in z.infolist():
                with z.open(file_info) as file:
                    # Read each CSV file into a DataFrame
                    df = pd.read_csv(file)

                    # Display the first few rows of the DataFrame
                    st.title(f"{file_info.filename}")
                    st.write(df.head())

if choice == "Profiling":
    st.title("Streamlit Data Processing Example")

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                geolocation = temp
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
            else:
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = y
                df = pd.concat([df, temp])

    # Display the DataFrame
    st.header("Concatenated DataFrame")
    st.write(df)

    # Display the Geolocation DataFrame
    st.header("Geolocation DataFrame")
    st.write(geolocation)

if choice == "Sorted Data Frame":
    st.title("Streamlit Data Processing Example")

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])

        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])

    # Sort the DataFrame by 'time' and reset index
    df.sort_values(by='time', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Display the sorted and reset DataFrame
    st.header("Sorted and Reset DataFrame")
    st.write(df)

if choice == "Extreme  Climate Years":
    st.title("Hottest and coldest years for every Cities")

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])

    # Finding hottest and coldest years for every city
    max_temp = df.groupby(by=['city'], as_index=False)['tavg'].max()
    min_temp = df.groupby(by=['city'], as_index=False)['tavg'].min()

    citywise = max_temp.append(min_temp)  # appending two pandas series
    max_min = df.merge(citywise, how='inner', on=['city', 'tavg'])

    # Display the result
    st.header("Hottest and Coldest Years for Every City")
    st.write(max_min)

if choice == "Graph":
    # Set the title of your Streamlit app
    st.title("Streamlit Data Processing Example")

    # Create an empty DataFrame
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])

    # Sort the DataFrame by 'time' and reset index
    df.sort_values(by='time', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Finding hottest and coldest years for every city
    max_temp = df.groupby(by=['city'], as_index=False)['tavg'].max()
    min_temp = df.groupby(by=['city'], as_index=False)['tavg'].min()

    citywise = max_temp.append(min_temp)  # appending two pandas series
    max_min = df.merge(citywise, how='inner', on=['city', 'tavg'])

    # Sort the DataFrame by 'city' and 'time', reset index
    max_min.sort_values(by=['city', 'time'], inplace=True)
    max_min.reset_index(drop=True, inplace=True)

    # Plotly Express bar chart with color-coded bars
    fig = px.bar(max_min, x='time', y='tavg', color='city',
                 labels={'tavg': 'Temperature'},
                 title='Hottest and Coldest Years for Every City',
                 color_discrete_map={'city': 'Viridis'})
    fig.update_layout(xaxis=dict(type='category'))

    # Display the chart
    st.plotly_chart(fig)

if choice == "City-Graph":
    st.title("Extreme Temperatures for every city")

    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])

    # Sort the DataFrame by 'time' and reset index
    df.sort_values(by='time', ascending=True, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Finding hottest and coldest years for every city
    max_temp = df.groupby(by=['city'], as_index=False)['tavg'].max()
    min_temp = df.groupby(by=['city'], as_index=False)['tavg'].min()

    citywise = max_temp.append(min_temp)  # appending two pandas series
    max_min = df.merge(citywise, how='inner', on=['city', 'tavg'])

    # Sort the DataFrame by 'city' and 'time', reset index
    max_min.sort_values(by=['city', 'time'], inplace=True)
    max_min.reset_index(drop=True, inplace=True)

    # Create subplots for each city with some distance between them
    fig, ax = plt.subplots(4, 2, figsize=(10, 10))
    plt.suptitle('Hottest and Coldest Years')

    # Adjust the layout to add some distance between subplots
    plt.subplots_adjust(hspace=0.8)

    for axs, c in zip(ax.flatten(), df['city'].unique()):
        citywise = max_min.loc[max_min['city'] == c]  # filtering the dataframe by city to use in plotting
        color = ["red" if (val > min(citywise['tavg'])) else "green" for val in citywise['tavg']]

        ppp = sns.barplot(data=citywise, x=max_min['time'].dt.year, y='tavg', ax=axs, ci=None, palette=color)
        axs.set_title(c)
        axs.set_xlabel('Year')
        axs.set_ylabel('Temperatures')
        axs.set_xticklabels(axs.get_xticklabels(), rotation=45)

        # Annotating the Bars in each plot by looping over patches within the plot
        for bar in ppp.patches:
            ppp.annotate(format(bar.get_height(), '.2f'),
                         (bar.get_x() + bar.get_width() / 2, bar.get_height() / 2),
                         ha='center', va='center', rotation=90,
                         size=8)

    # Display the subplots
    st.pyplot(fig)

if choice == "Min&Max Temp":
    st.title("Daily Min &  Max temp distribution by cities")

    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])
    # Create subplots for each city with some distance between them
    fig, ax = plt.subplots(figsize=(15, 8))
    sns.set_style(style='darkgrid')

    # Violin plot for tmin
    sns.violinplot(data=df, x='city', y='tmin', alpha=0.01, ax=ax)

    # Violin plot for tmax
    sns.violinplot(data=df, x='city', y='tmax', ax=ax)

    ax.set_ylabel('Temperature')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_title('Daily Min and Max Temperature Distribution by Cities', fontsize=15)

    # Display the violin plot
    st.pyplot(fig)

if choice == "Finding the temperature trends over years":
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
            else:
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = y
                df = pd.concat([df, temp])

    # Assuming df is your DataFrame with columns 'time', 'city', and 'tavg'
    # You need to replace this with your actual DataFrame and column names
    ts = df.set_index(['time', 'city'])

    # Multi-index grouping on time series 'ts' using groupby and grouper functions
    level_values = ts.index.get_level_values
    ts = ts.groupby([level_values(i) for i in [1]]
                    + [pd.Grouper(freq='M', level=0)]).mean()

    mavg = ts.reset_index()
    # Adding a month column for plotting month on x-axis
    mavg['month'] = mavg['time'].dt.month_name()

    # Create a Streamlit app
    st.title('Weather Analysis App')

    # Display raw data
    st.subheader('Raw Data')
    st.write(df.head())

    # Dropdown to select city
    selected_city = st.selectbox('Select City:', mavg['city'].unique())

    # Filter data for the selected city
    selected_city_data = mavg[mavg['city'] == selected_city]

    # Plotting Monthly Average Temperatures for the selected city
    st.subheader(f'Monthly Average Temperatures - {selected_city}')
    fig, ax = plt.subplots(figsize=(10, 9))
    for year in selected_city_data['time'].dt.year.unique():
        year_data = selected_city_data[selected_city_data['time'].dt.year == year]
        ax.plot(year_data['month'], year_data['tavg'], label=str(year))

    ax.set_xlabel('Month')
    ax.set_ylabel('Temperature')
    ax.legend(title='Year', bbox_to_anchor=(1.0, 1.06), loc='upper left')
    st.pyplot(fig)

if choice == "yearly average Temperatures":
    st.title('Yearly Average Temperatures')
    df = pd.DataFrame()

    # Loop through files in the specified directory
    for dirname, _, filenames in os.walk('/dataset/'):
        for filename in filenames:
            s = pd.Series([filename])
            x = s.str.split(pat='_', expand=True).iloc[0, 0]
            y = s.str.split(pat='_', expand=True).iloc[0, 1]

            if x == 'Station':
                temp_geolocation = pd.read_csv(os.path.join(dirname, filename))
            elif x != 'weather':
                temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
                temp['city'] = x
                df = pd.concat([df, temp])
        else:
            temp = pd.read_csv(os.path.join(dirname, filename), parse_dates=['time'])
            temp['city'] = y
            df = pd.concat([df, temp])
    ts = df.set_index(['time', 'city'])

    # Multi-index grouping on time series 'ts' using groupby and grouper functions
    level_values = ts.index.get_level_values
    ts = ts.groupby([level_values(i) for i in [1]] + [pd.Grouper(freq='Y', level=0)]).mean()

    yavg = ts.reset_index()
    # Adding a month column for plotting month on x-axis
    yavg['year'] = yavg['time'].dt.year

    # Display each subplot individually using st.line_chart()
    for city in yavg['city'].unique():
        # Create a separate plot for each city
        st.title(city)

        city_data = yavg[yavg['city'] == city]
        chart_data = pd.DataFrame(city_data[['year', 'tavg']])
        st.line_chart(chart_data.set_index('year'))

