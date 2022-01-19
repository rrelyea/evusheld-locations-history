import pandas as pd
  
evusheldData = pd.read_csv("data/mAbs-Evusheld-data.csv")
  
evusheldData.sort_values(["state_code", "county", "city", "provider_name"], 
                    axis=0,
                    ascending=[True, True, True, True], 
                    inplace=True)
  
evusheldData.to_csv("evusheld-data.csv", index=False)

providerData = evusheldData
del providerData['national_drug_code']
del providerData['order_label']
del providerData['last_order_date']
del providerData['last_date_delivered']
del providerData['total_courses']
del providerData['courses_available']
del providerData['courses_available_date']
providerData.to_csv("data/provider-data.csv", index=False)

hhs_ids = pd.read_csv("data/HHS_IDs.csv")

geocodes = pd.DataFrame(providerData.geocoded_address.unique(), None, ["geocoded_address"])
geo_hhsid = geocodes.merge(hhs_ids, 'left', left_on='geocoded_address', right_on='geocoded_hospital_address')
geo_hhsid.to_csv("data/geo-hhsids.csv", index=False)