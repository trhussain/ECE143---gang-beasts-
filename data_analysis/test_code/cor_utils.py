import pandas as pd
from geopy.distance import geodesic
import numpy as np
from scipy.stats import pearsonr
from scipy.signal import correlate
import matplotlib.pyplot as plt

def calculate_distance_stats_between_foxes(fox_df1, fox_df2):
    """
    Calculate the average, longest, and shortest distance between two foxes.

    Args:
        fox_df1 (pd.DataFrame): DataFrame containing data for the first fox with 'timestamp', 'location-lat', 'location-long' columns.
        fox_df2 (pd.DataFrame): DataFrame containing data for the second fox with 'timestamp', 'location-lat', 'location-long' columns.

    Returns:
        dict: A dictionary with the average, longest, and shortest distance.
    """
    # Ensure the timestamp is in datetime format
    fox_df1['timestamp'] = pd.to_datetime(fox_df1['timestamp'])
    fox_df2['timestamp'] = pd.to_datetime(fox_df2['timestamp'])
    
    # Merge the two DataFrames on the nearest timestamps
    merged = pd.merge_asof(
        fox_df1.sort_values(by='timestamp'),
        fox_df2.sort_values(by='timestamp'),
        on='timestamp',
        suffixes=('_fox1', '_fox2'),
        direction='nearest'  # Match the closest timestamp
    )
    
    # Calculate the distance between the two foxes
    def calculate_distance(row):
        fox1_location = (row['location-lat_fox1'], row['location-long_fox1'])
        fox2_location = (row['location-lat_fox2'], row['location-long_fox2'])
        return geodesic(fox1_location, fox2_location).meters

    merged['distance'] = merged.apply(calculate_distance, axis=1)
    
    # Compute statistics
    average_distance = merged['distance'].mean()
    longest_distance = merged['distance'].max()
    shortest_distance = merged['distance'].min()
    
    # Return the results as a dictionary
    return {
        'average_distance': average_distance,
        'longest_distance': longest_distance,
        'shortest_distance': shortest_distance
    }

def calculate_monthly_average_distance_between_foxes(fox_df1, fox_df2):
    """
    Calculate the average distance between two foxes for each month.

    Args:
        fox_df1 (pd.DataFrame): DataFrame containing data for the first fox with 'timestamp', 'location-lat', 'location-long' columns.
        fox_df2 (pd.DataFrame): DataFrame containing data for the second fox with 'timestamp', 'location-lat', 'location-long' columns.

    Returns:
        pd.DataFrame: A DataFrame with each month and the corresponding average distance.
    """
    # Ensure the timestamp is in datetime format
    fox_df1['timestamp'] = pd.to_datetime(fox_df1['timestamp'])
    fox_df2['timestamp'] = pd.to_datetime(fox_df2['timestamp'])
    
    # Merge the two DataFrames on the nearest timestamps
    merged = pd.merge_asof(
        fox_df1.sort_values(by='timestamp'),
        fox_df2.sort_values(by='timestamp'),
        on='timestamp',
        suffixes=('_fox1', '_fox2'),
        direction='nearest'  # Match the closest timestamp
    )
    
    # Calculate the distance between the two foxes
    def calculate_distance(row):
        fox1_location = (row['location-lat_fox1'], row['location-long_fox1'])
        fox2_location = (row['location-lat_fox2'], row['location-long_fox2'])
        return geodesic(fox1_location, fox2_location).meters

    merged['distance'] = merged.apply(calculate_distance, axis=1)
    
    # Extract the month from the timestamp
    merged['month'] = merged['timestamp'].dt.to_period('M')
    
    # Calculate the average distance for each month
    monthly_avg_distance = merged.groupby('month')['distance'].mean().reset_index()
    monthly_avg_distance.rename(columns={'distance': 'average_distance'}, inplace=True)
    
    return monthly_avg_distance


def analyze_fox_correlation_aligned(df1, df2):
    """
    Analyze the correlation between the movement patterns of two foxes based on longitude and latitude,
    aligning data points by timestamp.

    Parameters:
        df1 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 1.
        df2 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 2.

    Returns:
        dict: Pearson correlations for longitude and latitude after alignment.
    """
    # Merge DataFrames on timestamp
    merged_df = pd.merge(df1, df2, on='timestamp', suffixes=('_fox1', '_fox2'))
    
    # Extract aligned data
    time = pd.to_datetime(merged_df['timestamp'])
    fox1_long = merged_df['location-long_fox1'].values
    fox1_lat = merged_df['location-lat_fox1'].values
    fox2_long = merged_df['location-long_fox2'].values
    fox2_lat = merged_df['location-lat_fox2'].values

    # Pearson correlation for longitude and latitude
    corr_long, _ = pearsonr(fox1_long, fox2_long)
    corr_lat, _ = pearsonr(fox1_lat, fox2_lat)

    # Plot aligned trajectories
    plt.figure(figsize=(14, 6))
    
    # Longitude comparison
    plt.subplot(2, 1, 1)
    plt.plot(time, fox1_long, label='Fox 1 Longitude', marker='o')
    plt.plot(time, fox2_long, label='Fox 2 Longitude', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Longitude')
    plt.title('Aligned Longitude Over Time')
    plt.legend()

    # Latitude comparison
    plt.subplot(2, 1, 2)
    plt.plot(time, fox1_lat, label='Fox 1 Latitude', marker='o')
    plt.plot(time, fox2_lat, label='Fox 2 Latitude', marker='x')
    plt.xlabel('Time')
    plt.ylabel('Latitude')
    plt.title('Aligned Latitude Over Time')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

    # Return Pearson correlation results
    return {
        'pearson_corr_long': corr_long,
        'pearson_corr_lat': corr_lat,
    }

def analyze_fox_correlation_by_month(df1, df2):
    """
    Analyze the correlation between two foxes' movement patterns by month,
    aligning data points by timestamp.

    Parameters:
        df1 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 1.
        df2 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 2.

    Returns:
        pd.DataFrame: Correlation results (longitude and latitude) grouped by month.
    """
    # Convert timestamps to datetime objects
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Add month column for grouping
    df1['month'] = df1['timestamp'].dt.to_period('M')
    df2['month'] = df2['timestamp'].dt.to_period('M')

    # Merge DataFrames on timestamp
    merged_df = pd.merge(df1, df2, on='timestamp', suffixes=('_fox1', '_fox2'))
    merged_df['month'] = merged_df['timestamp'].dt.to_period('M')

    # Group by month and calculate Pearson correlations
    results = []
    for month, group in merged_df.groupby('month'):
        fox1_long = group['location-long_fox1'].values
        fox1_lat = group['location-lat_fox1'].values
        fox2_long = group['location-long_fox2'].values
        fox2_lat = group['location-lat_fox2'].values

        if len(fox1_long) > 1:  # Pearson correlation requires at least 2 points
            corr_long, _ = pearsonr(fox1_long, fox2_long)
            corr_lat, _ = pearsonr(fox1_lat, fox2_lat)
        else:
            corr_long, corr_lat = np.nan, np.nan  # Not enough data for correlation

        results.append({'month': month, 'pearson_corr_long': corr_long, 'pearson_corr_lat': corr_lat})

    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    # Plot correlations by month
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['month'].astype(str), results_df['pearson_corr_long'], label='Longitude Correlation', marker='o')
    plt.plot(results_df['month'].astype(str), results_df['pearson_corr_lat'], label='Latitude Correlation', marker='x')
    plt.xlabel('Month')
    plt.ylabel('Pearson Correlation')
    plt.title('Correlation by Month')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return results_df

def analyze_fox_correlation_end_of_day(df1, df2):
    """
    Analyze the correlation between the movement patterns of two foxes based on longitude and latitude,
    using only the location at the end of each day.

    Parameters:
        df1 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 1.
        df2 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 2.

    Returns:
        dict: Pearson correlations for longitude and latitude after alignment.
    """
    # Convert timestamps to datetime objects
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Group by date and select the last record for each day
    df1_end_of_day = df1.groupby(df1['timestamp'].dt.date).last().reset_index(drop=True)
    df2_end_of_day = df2.groupby(df2['timestamp'].dt.date).last().reset_index(drop=True)

    # Merge DataFrames on timestamp
    merged_df = pd.merge(df1_end_of_day, df2_end_of_day, on='timestamp', suffixes=('_fox1', '_fox2'))
    
    # Extract aligned data
    time = pd.to_datetime(merged_df['timestamp'])
    fox1_long = merged_df['location-long_fox1'].values
    fox1_lat = merged_df['location-lat_fox1'].values
    fox2_long = merged_df['location-long_fox2'].values
    fox2_lat = merged_df['location-lat_fox2'].values

    # Pearson correlation for longitude and latitude
    corr_long, _ = pearsonr(fox1_long, fox2_long)
    corr_lat, _ = pearsonr(fox1_lat, fox2_lat)

    # Plot aligned end-of-day trajectories
    plt.figure(figsize=(14, 6))
    
    # Longitude comparison
    plt.subplot(2, 1, 1)
    plt.plot(time, fox1_long, label='Fox 1 Longitude', marker='o')
    plt.plot(time, fox2_long, label='Fox 2 Longitude', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Longitude')
    plt.title('End-of-Day Longitude Over Time')
    plt.legend()

    # Latitude comparison
    plt.subplot(2, 1, 2)
    plt.plot(time, fox1_lat, label='Fox 1 Latitude', marker='o')
    plt.plot(time, fox2_lat, label='Fox 2 Latitude', marker='x')
    plt.xlabel('Date')
    plt.ylabel('Latitude')
    plt.title('End-of-Day Latitude Over Time')
    plt.legend()

    # Show the plots
    plt.tight_layout()
    plt.show()

    # Return Pearson correlation results
    return {
        'pearson_corr_long': corr_long,
        'pearson_corr_lat': corr_lat,
    }

def analyze_fox_correlation_end_of_day_by_month(df1, df2):
    """
    Analyze the correlation between the movement patterns of two foxes based on longitude and latitude,
    using only the location at the end of each day and grouping by month.

    Parameters:
        df1 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 1.
        df2 (pd.DataFrame): DataFrame with 'timestamp', 'location-long', and 'location-lat' for Fox 2.

    Returns:
        pd.DataFrame: Correlation results (longitude and latitude) grouped by month.
    """
    # Convert timestamps to datetime objects
    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Group by date and select the last record for each day
    df1_end_of_day = df1.groupby(df1['timestamp'].dt.date).last().reset_index(drop=True)
    df2_end_of_day = df2.groupby(df2['timestamp'].dt.date).last().reset_index(drop=True)

    # Add a month column for grouping
    df1_end_of_day['month'] = df1_end_of_day['timestamp'].dt.to_period('M')
    df2_end_of_day['month'] = df2_end_of_day['timestamp'].dt.to_period('M')

    # Merge the end-of-day DataFrames
    merged_df = pd.merge(
        df1_end_of_day,
        df2_end_of_day,
        on='timestamp',
        suffixes=('_fox1', '_fox2')
    )

    # Add a month column to the merged DataFrame
    merged_df['month'] = merged_df['timestamp'].dt.to_period('M')

    # Group by month and calculate Pearson correlations
    results = []
    for month, group in merged_df.groupby('month'):
        fox1_long = group['location-long_fox1'].values
        fox1_lat = group['location-lat_fox1'].values
        fox2_long = group['location-long_fox2'].values
        fox2_lat = group['location-lat_fox2'].values

        # Ensure there are at least two data points for correlation
        if len(fox1_long) > 1:
            corr_long, _ = pearsonr(fox1_long, fox2_long)
            corr_lat, _ = pearsonr(fox1_lat, fox2_lat)
        else:
            corr_long, corr_lat = np.nan, np.nan  # Not enough data for correlation

        results.append({'month': month, 'pearson_corr_long': corr_long, 'pearson_corr_lat': corr_lat})

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)

    # Plot correlations by month
    plt.figure(figsize=(10, 6))
    plt.plot(results_df['month'].astype(str), results_df['pearson_corr_long'], label='Longitude Correlation', marker='o')
    plt.plot(results_df['month'].astype(str), results_df['pearson_corr_lat'], label='Latitude Correlation', marker='x')
    plt.xlabel('Month')
    plt.ylabel('Pearson Correlation')
    plt.title('End-of-Day Correlation by Month')
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return results_df