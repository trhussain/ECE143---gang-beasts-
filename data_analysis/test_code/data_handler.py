import pandas as pd 
import os 
from tabulate import tabulate
from geopy.distance import geodesic

class dataHandler: 
    def __init__(self): 
        current_dir = os.getcwd()
        # print(current_dir)
        csv_path = os.path.join(current_dir, "data_analysis", "data", "red_fox.csv")
        self.raw_df = pd.read_csv(csv_path)
        self.raw_df['timestamp'] = pd.to_datetime(self.raw_df['timestamp'])


        self.headers = self.raw_df.columns.tolist()
        self.raw_data = self.raw_df.values
        self.desired_df, self.unique = self.processData()
        

    def processData(self): 

        df = self.raw_df.sort_values(by='timestamp')
        columns_to_extract = ['location-long', 'location-lat', 'tag-local-identifier', 'timestamp' ]
        new_df = df[columns_to_extract]
        names = df['tag-local-identifier'].unique() 
                
                
        time_interval = pd.Timedelta(hours=5)
        
        
        unique_dfs = {}

        for unique_name in df['tag-local-identifier'].unique():
            # Filter rows corresponding to the unique name
            group = new_df[new_df['tag-local-identifier'] == unique_name].sort_values(by='timestamp')
            group.rename(columns={"tag-local-identifier" : "name"}, inplace=True)
            # Initialize a new filtered DataFrame
            filtered_group = [group.iloc[0]]  # Start with the first row

            # Iterate through the group and select rows based on the time interval
            for i in range(1, len(group)):
                if group.iloc[i]['timestamp'] - filtered_group[-1]['timestamp'] >= time_interval and geodesic( (group.iloc[i]['location-lat'], group.iloc[i]['location-long'] )
                                                                                                              , (filtered_group[-1]['location-lat'], filtered_group[-1]['location-long'] )).meters > 75:
                    filtered_group.append(group.iloc[i])

            # Create a DataFrame from the filtered rows
            unique_dfs[unique_name] = pd.DataFrame(filtered_group)
        for key, df in unique_dfs.items():
            rows, cols = df.shape
            print(f"DataFrame '{key}' has {rows} rows and {cols} columns.")        
        return (new_df, unique_dfs)

    def displayDataPretty(self, df, unique_dfs = None):
        displayLimit = 10

        # Check if the DataFrame exceeds the display limit
        if len(df) > displayLimit:
            half_limit = displayLimit // 2
            # Keep the first half and the last half of rows
            truncated_df = pd.concat([df.head(half_limit), pd.DataFrame([["..."] * len(df.columns)], columns=df.columns), df.tail(half_limit)])
        else:
            truncated_df = df

        # Tabulate the truncated DataFrame
        table = tabulate(truncated_df.values, headers=truncated_df.columns.tolist(), tablefmt="pretty", showindex=False)
        print(table)
        
                # Print each DataFrame
        if unique_dfs != None:
            for name, unique_df in unique_dfs.items():
                print(f"DataFrame for {name}:")
                print(unique_df)
                print("\n")
        
        pass
    def csv_to_geojson(self, df: pd.DataFrame):
        features = []
        for _, row in df.iterrows():
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row['location-long'], row['location-lat']]
                },
                "properties": {
                    "timestamp": row['timestamp'].isoformat(),
                    "gps_hdop": row['gps:hdop'],
                    "satellite_count": row['gps:satellite-count']
                }
            }
            features.append(feature)
        return {
            "type": "FeatureCollection",
            "features": features
        }
        
        
if __name__ == "__main__":
    myDH = dataHandler()
    geojson_data = myDH.csv_to_geojson(myDH.raw_df)
    
    