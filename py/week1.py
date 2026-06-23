import pandas as pd
from datetime import date

year = 2024
month = 1

# store listing dataframes in a list
## reduces need to concatenate after every new dataframe
listing_df = []
sold_df = []

# record before concatenation row counts
listing_row_count = 0
sold_row_count = 0

# end loop after 202605 is passed
while (year < 2026) or (year == 2026 and month <= 5):
    listing_filename = f'csv/CRMLSListing{year}{month:02d}.csv'
    sold_filename = f'csv/CRMLSSold{year}{month:02d}.csv'
    listing = pd.read_csv(listing_filename)
    sold = pd.read_csv(sold_filename)

    listing_df.append(listing)
    sold_df.append(sold)

    listing_row_count += len(listing)
    sold_row_count += len(sold)

    month += 1
    # increment year if month passes cycle
    if month > 12:
        month = 1
        year += 1

# combine all dataframes
listing_final = pd.concat(listing_df)
sold_final = pd.concat(sold_df)

print(f'Listing rows after concatenation: {listing_row_count}')
# Listing rows after concatenation: 930311
print(f'Listing rows after concatenation: {len(listing_final)}')
# Listing rows after concatenation: 930311

print(f'Sold rows after concatenation: {sold_row_count}')
# Sold rows after concatenation: 639878
print(f'Sold rows after concatenation: {len(sold_final)}')
# Sold rows after concatenation: 639878

listing_before_filter = len(listing_final)
# filter to Residential properties
listing_final = listing_final[listing_final['PropertyType'] == 'Residential']
listing_after_filter = len(listing_final)

print(f'Listing rows before filtering: {listing_before_filter}')
# Listing rows before filtering: 930311
print(f'Listing rows before filtering: {listing_after_filter}')
# Listing rows before filtering: 591980

sold_before_filter = len(sold_final)
# filter to Residential properties
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
sold_after_filter = len(sold_final)

print(f'Sold rows before filtering: {sold_before_filter}')
# Sold rows before filtering: 639878
print(f'Sold rows before filtering: {sold_after_filter}')
# Sold rows before filtering: 430437

# save dataframe as csv file
listing_final.to_csv('csv/CRMLSListingFinal.csv', index=False)
sold_final.to_csv('csv/CRMLSSoldFinal.csv', index=False)






