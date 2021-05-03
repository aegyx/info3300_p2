import pandas as pd

raw = pd.read_csv("./raw_data/kyoto_restaurants.csv")

# Find out which columns to use from FirstCategory (restaurant cuisine category)
print(len(raw.FirstCategory.unique()))

# There are 97 unique cuisines in the dataset; need to narrow down 
# Seems like there are some overlapping categories that need to be fixed. For example, 'Izakaya(Tavern)' and 'Izakaya(other)' are two distinct cuisines in the dataset, same with 'French' and 'Bistro'

cuisines_dict = {}
cuisines_dict['Izakaya (Alcohol)'] = ['Izakaya (Tavern)', 'Bar', 'Pub', 'Beer', 'Beer bar', 'Beer garden', 'Izakaya (other)', 'Nihonshu (Japanese sake)', 'Stand Bar', 'Wine bar'] 
cuisines_dict['Japanese (Meat Dishes)'] = ['Kushi-age (Fried Skewer)', 'Yakiniku (BBQ Beef)', 'Tonkatsu (Pork cutlet)', 'Robatayaki', 'Yakitori (Grilled chicken)', 'Shabu Shabu', 'Horumon (BBQ Offel)', 'Motsu Nabe (Offel Hot Pot)', 'Pork Shabu Shabu', 'Beef dishes', 'Sukiyaki', 'Chiritori nabe (tripe)', 'Hot Pot (other)', 'Meat dishes', 'Sumibiyaki', 'Genghis Khan (BBQ Rum)']  # japanese (meat)
cuisines_dict['Japanese (Noodles)'] = ['Ramen', 'Soba', 'Udon', 'Champon Noodle', 'Standing style soba', 'Dandan noodles', 'Udon Suki', 'Tsukemen'] 
cuisines_dict['Japanese (Other)'] = ['Kyoto Cuisine', 'Kappo (Traditional Japanese)', 'Kaiseki (Traditional Japanese)', 'Okonomiyaki', 'Teppanyaki', 'Fowl', 'Okinawan Cuisine', 'Japanese food (other)', 'Regional Cuisine (Other)', 'Takoyaki', 'Curry (other)', 'Oyako-don (Chicken Bowl)'] 
cuisines_dict['Japanese (Seafood)'] = ['Tempura', 'Sushi', 'Seafood', 'Fugu (Blowfish)', 'Unagi (Freshwater eel)' 'Suppon (Soft-shelled Turtle)', 'Oden', 'Crab']    
cuisines_dict['Asian (Non-Japanese)'] = ['Chinese', 'Cantonese Cuisine', 'Thailand cooking', 'Korean cuisine', 'Shanghai Cuisine', 'Sichuan Cuisine', 'Viet Nam cuisine', 'Chinese hot pot / fire pot', 'Shanghai Cuisine', 'India', 'Indonesia cuisine']  
cuisines_dict['Western'] = ['Italian', 'French', 'Pasta', 'Hamburger Steak', 'Steak', 'Pizza', 'Bistro', 'Spain', 'Western Cuisine', 'Mexico cuisine', 'Western (Others)', 'European-style Curry', 'Modern French', 'Western Food (Other)']   

cuisines_list = ['Izakaya (Alcohol)', 'Japanese (Meat Dishes)', 'Japanese (Noodles)', 'Japanese (Other)', 'Japanese (Seafood)', 'Asian (Non-Japanese)', 'Western']

for restaurant in raw.FirstCategory:
	for category in cuisines_dict:
			raw.loc[raw.FirstCategory.isin(cuisines_dict[category]), 'FirstCategory'] = category

for restaurant in raw.FirstCategory:
	raw.loc[~raw.FirstCategory.isin(cuisines_list), 'FirstCategory'] = "Other"

proportion_cuisines = {}
total_cuisines = raw.shape[0] - raw['FirstCategory'].isna().sum()
for cuisine in raw.FirstCategory.unique():
	count = raw.loc[raw.FirstCategory == cuisine, 'FirstCategory'].count()
	proportion_cuisines[cuisine] = count/total_cuisines * 100
proportion_cuisines = {k: v for k, v in sorted(proportion_cuisines.items(), reverse=True, key=lambda x: x[1])}


column_list = ['Name','JapaneseName','FirstCategory','DinnerPrice','TotalRating','ReviewNum','Lat','Long']

processed = raw[column_list]
processed.rename(columns={'Name':'name', 'JapaneseName':'japan_name', 'FirstCategory':'cuisine', 'DinnerPrice':'price', 'TotalRating':'rating', 'ReviewNum':'num_reviews'}, inplace=True)
processed.to_json("./kyoto_restaurants_processed.json", orient="records")


