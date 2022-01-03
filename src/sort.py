import pandas as pd
  
csvData = pd.read_csv("evusheld-data.csv")
  
csvData.sort_values(["State Code", "County", "City", "Provider Name"], 
                    axis=0,
                    ascending=[True, True, True, True], 
                    inplace=True)
  
csvData.to_csv("evusheld-data.csv", index=False)
