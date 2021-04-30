import pandas as pd

raw = pd.read_csv("./raw_data/kyoto_restaurants.csv")

# Find out which columns to use from FirstCategory (restaurant cuisine category)
print(len(raw.FirstCategory.unique()))
# There are 97 unique cuisines in the dataset; need to narrow down 
proportion_cuisines = {}
total_cuisines = raw.shape[0] - raw['FirstCategory'].isna().sum()
for cuisine in raw.FirstCategory.unique():
	count = raw.loc[raw.FirstCategory == cuisine, 'FirstCategory'].count()
	proportion_cuisines[cuisine] = count/total_cuisines * 100
proportion_cuisines = {k: v for k, v in sorted(proportion_cuisines.items(), reverse=True, key=lambda x: x[1])}

# Seems like there are some overlapping categories that need to be fixed later 
# For example, 'Izakaya(Tavern)' and 'Izakaya(other)' are two distinct cuisines in the dataset, same with 'French' and 'Bistro'
# Top 20 most common accounts for almost 90% of the existing cuisines; narrow down to top 20 and make the rest "Other"
cuisines_other = list(proportion_cuisines.keys())[19:]

for row in raw.FirstCategory:
	raw.loc[raw.FirstCategory.isin(cuisines_other), 'FirstCategory'] = "Other"

column_list = ['Name','JapaneseName','FirstCategory','DinnerPrice','TotalRating','ReviewNum','Lat','Long']

processed = raw[column_list]
processed.rename(columns={'Name':'name', 'JapaneseName':'japan_name', 'FirstCategory':'cuisine', 'DinnerPrice':'price', 'TotalRating':'rating', 'ReviewNum':'num_reviews'}, inplace=True)
processed.to_json("./kyoto_restaurants_processed.json", orient="records")



