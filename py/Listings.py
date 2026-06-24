import pandas as pd
from datetime import date

year = 2024
month = 1

# store listing dataframes in a list
## reduces need to concatenate after every new dataframe
listing_df = []

# record before concatenation row counts
listing_row_count = 0

# end loop after 202605 is passed
while (year < 2026) or (year == 2026 and month <= 5):
    listing_filename = f'csv/CRMLSListing{year}{month:02d}.csv'
    listing = pd.read_csv(listing_filename)

    listing_df.append(listing)

    listing_row_count += len(listing)

    month += 1
    # increment year if month passes cycle
    if month > 12:
        month = 1
        year += 1

# combine all dataframes
listing_final = pd.concat(listing_df)

print(f'Listing rows before concatenation: {listing_row_count}')
# Listing rows before concatenation: 930311
print(f'Listing rows after concatenation: {len(listing_final)}')
# Listing rows after concatenation: 930311

listing_before_filter = len(listing_final)
# filter to Residential properties
listing_final = listing_final[listing_final['PropertyType'] == 'Residential']
listing_after_filter = len(listing_final)

print(f'Listing rows before filtering: {listing_before_filter}')
# Listing rows before filtering: 930311
print(f'Listing rows after filtering: {listing_after_filter}')
# Listing rows after filtering: 591980

# save dataframe as csv file
listing_final.to_csv('csv/CRMLSListingFinal.csv', index=False)