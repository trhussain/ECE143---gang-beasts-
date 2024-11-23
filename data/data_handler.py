import pandas as pd 
import os 
from tabulate import tabulate
# need to extract lat long and animal name 
# default to not include row, but tag the row as "not included" 


class dataHandler: 
    def __init__(self): 
        current_dir = os.getcwd()
        csv_path = os.path.join(current_dir, "data", "arctic.csv")

        self.raw_df = pd.read_csv(csv_path)
        self.headers = self.raw_df.columns.tolist()
        self.raw_data = self.raw_df.values
        self.desired_df = self.processData()
        
        

    def processData(self): 
        # grabs headers that match anything within this list 
        desiredHeaders = ['lat', 'latitude', 'long', 'lon','name', 'fox'] 
        matches = [header for header in self.headers if any(keyword in header for keyword in desiredHeaders)]

        #  from raw_df
        desired_df = self.raw_df[matches]
        
        # rename lat lon headers to appropiate plotting requirements --- hard coded 
        desired_df.rename(columns= {"location-long": "LON", "location-lat": "LAT", "study-name": "info"}, inplace=True)
        return desired_df

    def displayDataPretty(self):
        displayLimit = 10
        df = self.desired_df

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
        pass
        
        
if __name__ == "__main__":
    myDH = dataHandler()
    myDH.displayDataPretty()
    # print(tabulate(myDH.rawData, headers=myDH.headers, tablefmt="pretty", showindex=False))