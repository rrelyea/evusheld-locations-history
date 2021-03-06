import pandas as pd

def sortDataFile(fileName):
  dataFile = pd.read_csv(fileName)
  
  # ensure standard casing, so that sorting works better.
  dataFile['city'] = dataFile['city'].str.title()
  dataFile['county'] = dataFile['county'].str.title()

  dataFile.sort_values(["state_code", "county", "city", "provider_name"], 
                      axis=0,
                      ascending=[True, True, True, True], 
                      inplace=True)

  dataFile.to_csv(fileName, index=False)

sortDataFile("evusheld-data.csv")
sortDataFile("sotrovimab-data.csv")
sortDataFile("bebtelovimab-data.csv")
sortDataFile("paxlovid-data.csv")