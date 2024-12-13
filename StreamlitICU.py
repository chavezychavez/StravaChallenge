import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Read the CSV file
@st.cache_data
def load_data():
    df = pd.read_csv('MultiAthlete_Activities_Summary_Updated.csv')
    return df

def create_comparison_chart(filtered_df, activity_type):
    comparison_data = []
    sprint_diff = filtered_df[f'{activity_type} Sprint Difference'].sum()
    olympic_diff = filtered_df[f'{activity_type} Olympic Difference'].sum()
    
    comparison_data.extend([
        {'Category': 'Sprint Distance Difference', 'Difference': sprint_diff},
        {'Category': 'Olympic Distance Difference', 'Difference': olympic_diff}
    ])
    
    comparison_df = pd.DataFrame(comparison_data)
    
    fig = px.bar(comparison_df, 
                 x='Category',
                 y='Difference',
                 title=f'{activity_type} Distance Differences',
                 color='Difference',
                 color_continuous_scale=['red', 'green'])
    
    fig.update_layout(
        yaxis_title="Distance Difference",
        xaxis_title="",
        showlegend=False,
        height=400
    )
    
    # Add a horizontal line at y=0
    fig.add_hline(y=0, line_dash="dash", line_color="black")
    
    return fig

def main():
    st.title('Athlete Training Analysis Dashboard')
    
    # Load data
    df = load_data()
    
    # Sidebar filters
    st.sidebar.header('Filters')
    
    # Name multiselect
    names = list(df['AthleteName'].unique())
    selected_names = st.sidebar.multiselect('Select Athletes', names, default=names)
    
    # Date Period multiselect
    periods = list(df['DatePeriod'].unique())
    selected_periods = st.sidebar.multiselect('Select Periods', periods, default=periods)
    
    # Filter data based on selections
    filtered_df = df[
        (df['AthleteName'].isin(selected_names)) &
        (df['DatePeriod'].isin(selected_periods))
    ]
    
    if not filtered_df.empty:
        # Activity types
        activity_types = ['Swim', 'Cycle', 'Run']
        
        # Create metrics for all activities
        st.subheader('Activity Statistics')
        cols = st.columns(len(activity_types))
        
        for idx, activity in enumerate(activity_types):
            with cols[idx]:
                st.subheader(f'{activity}')
                total_activities = filtered_df[f'{activity} Number of Activities'].sum()
                total_distance = filtered_df[f'{activity} Total Distance'].sum()
                st.metric(f"Total Activities", f"{total_activities}")
                st.metric(f"Total Distance", f"{total_distance:.2f}")
        
        # Create separate charts for each activity type
        st.subheader('Distance Comparisons')
        
        # Swim Chart
        st.markdown("### 🏊 Swimming Analysis")
        swim_fig = create_comparison_chart(filtered_df, 'Swim')
        st.plotly_chart(swim_fig, use_container_width=True)
        
        # Cycle Chart
        st.markdown("### 🚴 Cycling Analysis")
        cycle_fig = create_comparison_chart(filtered_df, 'Cycle')
        st.plotly_chart(cycle_fig, use_container_width=True)
        
        # Run Chart
        st.markdown("### 🏃 Running Analysis")
        run_fig = create_comparison_chart(filtered_df, 'Run')
        st.plotly_chart(run_fig, use_container_width=True)
        
        # Additional information
        st.info("""
        Interpretation:
        - Positive values (green) indicate exceeding the target distance
        - Negative values (red) indicate falling short of the target distance
        - Values show the combined totals for selected athletes and periods
        """)
        
        # Show filtered raw data
        if st.checkbox('Show Raw Data'):
            st.write(filtered_df)
            
        # Add download button for filtered data
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_athlete_data.csv",
            mime="text/csv",
        )
    
    else:
        st.warning("No data available for the selected combination of filters. Please adjust your selection.")

if __name__ == "__main__":
    main()
