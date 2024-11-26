
import pandas as pd
from geopy.distance import geodesic
import numpy as np
from sklearn.cluster import KMeans

def total_distance(df):
    """
    This function calculates the total distance traveled by the animal in meters
    """
    distance = 0
    for i in range(1, len(df)):
        distance += ((df.iloc[i]['location-long'] - df.iloc[i-1]['location-long'])**2 + (df.iloc[i]['location-lat'] - df.iloc[i-1]['location-lat'])**2)**0.5

    # change the distance into meters
    return distance * 111139

def average_speed_per_day(df):
    """
    This function calculates the average speed of the animal in m/day
    """
    distance = total_distance(df)

    time = (pd.to_datetime(df.iloc[-1]['timestamp']) - pd.to_datetime(df.iloc[0]['timestamp'])).days
    print(time)

    return distance / time

def calculate_average_distance_auto_sections(df, interval_minutes=90):
    """
    Calculate the average distance moved for each automatically derived section of the day.

    Args:
        df (pd.DataFrame): DataFrame containing 'timestamp', 'location-lat', 'location-long' columns.
        interval_minutes (int): The interval in minutes for grouping timestamps.

    Returns:
        pd.DataFrame: A DataFrame with sections and average distances.
    """
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by timestamp
    df = df.sort_values(by='timestamp')
    
    # Calculate distances between consecutive points
    def compute_distance(row):
        if pd.isna(row['prev_lat']) or pd.isna(row['prev_long']):
            return 0
        return geodesic((row['prev_lat'], row['prev_long']), (row['location-lat'], row['location-long'])).meters

    df['prev_lat'] = df['location-lat'].shift()
    df['prev_long'] = df['location-long'].shift()
    df['distance'] = df.apply(compute_distance, axis=1)
    
    # Create sections based on intervals
    df['section'] = (df['timestamp'].dt.hour * 60 + df['timestamp'].dt.minute) // interval_minutes
    
    # Calculate the average distance for each section
    avg_distances = (
        df.groupby(['section'])['distance']
        .mean()
        .reset_index()
        .rename(columns={'distance': 'avg_distance'})
    )
    
    # Add section labels for clarity
    avg_distances['section_label'] = avg_distances['section'].apply(
        lambda x: f"{(x * interval_minutes) // 60:02d}:{(x * interval_minutes) % 60:02d} to "
                  f"{((x + 1) * interval_minutes) // 60:02d}:{((x + 1) * interval_minutes) % 60:02d}"
    )
    
    return avg_distances

def calculate_total_distance_per_day_per_month(df):
    """
    Calculate the total moving distance per day and aggregate it by month.

    Args:
        df (pd.DataFrame): DataFrame containing 'timestamp', 'location-lat', 'location-long' columns.

    Returns:
        pd.DataFrame: A DataFrame with months and the average daily total distance.
    """
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by timestamp
    df = df.sort_values(by='timestamp')
    
    # Calculate distances between consecutive points
    def compute_distance(row):
        if pd.isna(row['prev_lat']) or pd.isna(row['prev_long']):
            return 0
        return geodesic((row['prev_lat'], row['prev_long']), (row['location-lat'], row['location-long'])).meters

    df['prev_lat'] = df['location-lat'].shift()
    df['prev_long'] = df['location-long'].shift()
    df['distance'] = df.apply(compute_distance, axis=1)
    
    # Extract the day and month from the timestamp
    df['day'] = df['timestamp'].dt.date
    df['month'] = df['timestamp'].dt.to_period('M')
    
    # Calculate total distance per day
    daily_total = (
        df.groupby(['day'])['distance']
        .sum()
        .reset_index()
        .rename(columns={'distance': 'total_distance_per_day'})
    )
    
    # Aggregate by month to get the average daily total distance
    monthly_avg = (
        daily_total.groupby(daily_total['day'].apply(lambda x: x.strftime('%Y-%m')))['total_distance_per_day']
        .mean()
        .reset_index()
        .rename(columns={'day': 'month', 'total_distance_per_day': 'avg_daily_total_distance'})
    )
    
    return monthly_avg

def calculate_moving_directions(df, interval_minutes=90):
    """
    Calculate the moving directions of an animal at each time section.

    Args:
        df (pd.DataFrame): DataFrame containing 'timestamp', 'location-lat', 'location-long' columns.
        interval_minutes (int): Interval in minutes to define sections.

    Returns:
        pd.DataFrame: A DataFrame with sections and predominant moving directions.
    """
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by timestamp
    df = df.sort_values(by='timestamp')
    
    # Calculate bearings (directions) between consecutive points
    def calculate_bearing(lat1, lon1, lat2, lon2):
        # Convert degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
        d_lon = lon2 - lon1
        x = np.sin(d_lon) * np.cos(lat2)
        y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(d_lon)
        initial_bearing = np.arctan2(x, y)
        initial_bearing = np.degrees(initial_bearing)
        return (initial_bearing + 360) % 360  # Normalize to 0-360 degrees

    df['prev_lat'] = df['location-lat'].shift()
    df['prev_long'] = df['location-long'].shift()
    df['bearing'] = df.apply(
        lambda row: calculate_bearing(row['prev_lat'], row['prev_long'], row['location-lat'], row['location-long'])
        if not pd.isna(row['prev_lat']) else None, axis=1
    )
    
    # Assign sections based on intervals
    df['section'] = (df['timestamp'].dt.hour * 60 + df['timestamp'].dt.minute) // interval_minutes
    
    # Map bearings to cardinal directions
    def bearing_to_direction(bearing):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = int((bearing + 22.5) // 45) % 8
        return directions[index]

    df['direction'] = df['bearing'].apply(lambda x: bearing_to_direction(x) if not pd.isna(x) else None)
    
    # Analyze predominant direction in each section
    predominant_directions = (
        df.groupby(['section'])['direction']
        .apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
        .reset_index()
        .rename(columns={'direction': 'predominant_direction'})
    )
    
    # Add section labels for clarity
    predominant_directions['section_label'] = predominant_directions['section'].apply(
        lambda x: f"{(x * interval_minutes) // 60:02d}:{(x * interval_minutes) % 60:02d} to "
                  f"{((x + 1) * interval_minutes) // 60:02d}:{((x + 1) * interval_minutes) % 60:02d}"
    )
    
    return predominant_directions

def calculate_monthly_distance_and_direction(df):
    """
    Calculate the total moving distance and direction for each month by comparing
    the start location of the month to the end location.

    Args:
        df (pd.DataFrame): DataFrame containing 'timestamp', 'location-lat', 'location-long' columns.

    Returns:
        pd.DataFrame: A DataFrame with months, total distance, and direction.
    """
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Extract month from timestamp
    df['month'] = df['timestamp'].dt.to_period('M')
    
    # Sort by timestamp
    df = df.sort_values(by='timestamp')
    
    # Get the first and last location for each month
    monthly_locations = df.groupby('month').agg(
        start_lat=('location-lat', 'first'),
        start_long=('location-long', 'first'),
        end_lat=('location-lat', 'last'),
        end_long=('location-long', 'last')
    ).reset_index()
    
    # Calculate distance and bearing between start and end locations
    def calculate_distance_and_bearing(row):
        start = (row['start_lat'], row['start_long'])
        end = (row['end_lat'], row['end_long'])
        distance = geodesic(start, end).meters
        
        # Calculate bearing
        def calculate_bearing(lat1, lon1, lat2, lon2):
            # Convert degrees to radians
            lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
            d_lon = lon2 - lon1
            x = np.sin(d_lon) * np.cos(lat2)
            y = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(d_lon)
            initial_bearing = np.arctan2(x, y)
            initial_bearing = np.degrees(initial_bearing)
            return (initial_bearing + 360) % 360  # Normalize to 0-360 degrees

        bearing = calculate_bearing(row['start_lat'], row['start_long'], row['end_lat'], row['end_long'])
        
        return pd.Series({'total_distance': distance, 'bearing': bearing})
    
    # Apply the distance and bearing calculation
    monthly_locations[['total_distance', 'bearing']] = monthly_locations.apply(
        calculate_distance_and_bearing, axis=1
    )
    
    # Map bearings to cardinal directions
    def bearing_to_direction(bearing):
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        index = int((bearing + 22.5) // 45) % 8
        return directions[index]
    
    monthly_locations['direction'] = monthly_locations['bearing'].apply(bearing_to_direction)
    
    # Select relevant columns
    result = monthly_locations[['month', 'total_distance', 'direction']]
    
    return result


def calculate_frequent_areas(df, num_clusters=5):
    """
    This function calculates the most frequent areas visited by an animal.

    Args:
        df (pd.DataFrame): DataFrame containing 'timestamp', 'location-lat', and 'location-long' columns.
        num_clusters (int): Number of clusters to use for KMeans clustering.

    Returns:
        pd.DataFrame: A DataFrame with the most frequent areas and their frequencies.
        
    """
    # Ensure the timestamp is in datetime format
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Sort the data by timestamp
    df = df.sort_values(by='timestamp')
    
    # Extract the latitude and longitude columns
    X = df[['location-lat', 'location-long']]
    
    # Fit a KMeans clustering model
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(X)
    
    # Assign cluster labels to each point
    df['cluster'] = kmeans.predict(X)
    
    # Calculate the frequency of each cluster
    frequent_areas = (
        df.groupby('cluster')
        .size()
        .reset_index(name='frequency')
        .sort_values(by='frequency', ascending=False)
    )
    
    # Get the cluster centers
    cluster_centers = kmeans.cluster_centers_
    
    # Add cluster centers to the frequent areas DataFrame
    frequent_areas['location-lat'] = frequent_areas['cluster'].apply(lambda x: cluster_centers[x][0])
    frequent_areas['location-long'] = frequent_areas['cluster'].apply(lambda x: cluster_centers[x][1])
    
    # Calculate the most frequent time for each cluster appearance
    frequent_times = (
        df.groupby('cluster')['timestamp']
        .apply(lambda x: x.dt.hour.mode()[0] if not x.dt.hour.mode().empty else None)
        .reset_index(name='most_frequent_hour')
    )
    
    # Merge the frequent times with the frequent areas DataFrame
    frequent_areas = frequent_areas.merge(frequent_times, on='cluster')
    
    return frequent_areas