import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
random.seed(42)

# Generate dummy data
def generate_flight_data():
    # Create date range for the past 30 days to give more data to work with
    dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]
    
    # Generate data for each airline
    data = []
    airlines = ['American Airlines', 'Delta', 'Alaska Airlines']
    
    for date in dates:
        for airline in airlines:
            # Generate random number of flights (American Airlines has more as it's a hub)
            if airline == 'American Airlines':
                flights = random.randint(150, 200)
            else:
                flights = random.randint(20, 50)
            
            data.append({
                'Date': pd.to_datetime(date),
                'Airline': airline,
                'Flights': flights
            })
    
    return pd.DataFrame(data)

# Create the Streamlit app
def main():
    st.title('DFW Airport Flight Frequency Analysis')
    st.write('Analysis of daily flights departing from Dallas/Fort Worth International Airport')
    
    # Generate the data
    df = generate_flight_data()
    
    # Sidebar controls
    st.sidebar.header('Filters')
    
    # Airline selector
    airlines = df['Airline'].unique()
    selected_airlines = st.sidebar.multiselect(
        'Select Airlines',
        options=airlines,
        default=airlines
    )
    
    # Date range slider
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input(
        'Select Date Range',
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter the data based on selections
    if len(date_range) == 2:
        start_date, end_date = date_range
        mask = (
            (df['Airline'].isin(selected_airlines)) &
            (df['Date'].dt.date >= start_date) &
            (df['Date'].dt.date <= end_date)
        )
        filtered_df = df.loc[mask]
    
        # Create the visualization
        if not filtered_df.empty:
            fig = px.line(filtered_df, 
                         x='Date', 
                         y='Flights', 
                         color='Airline',
                         title='Daily Flights by Airline from DFW',
                         markers=True)
            
            # Customize the layout
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Number of Flights',
                legend_title='Airline',
                hovermode='x unified'
            )
            
            # Display the plot
            st.plotly_chart(fig, use_container_width=True)
            
            # Display summary statistics for the selected period
            st.subheader('Summary Statistics for Selected Period')
            summary = filtered_df.groupby('Airline')['Flights'].agg([
                ('Average Daily Flights', 'mean'),
                ('Minimum Flights', 'min'),
                ('Maximum Flights', 'max')
            ]).round(2)
            st.dataframe(summary)
            
            # Add total flights calculation
            total_flights = filtered_df.groupby('Airline')['Flights'].sum()
            st.subheader('Total Flights in Selected Period')
            st.dataframe(total_flights)
        else:
            st.warning('No data available for the selected filters.')
    else:
        st.error('Please select both start and end dates.')
    
    # Add a note about the data
    st.caption('Note: This visualization uses simulated data for demonstration purposes.')

if __name__ == '__main__':
    main()