import pandas as pd
from datetime import date

# ------------------------------------------------------
# Monthly Dataset Aggregation
# ------------------------------------------------------

year = 2015
month = 1

# store sold dataframes in a list
## reduces need to concatenate after every new dataframe
sold_df = []

# record before concatenation row counts
sold_row_count = 0

# end loop after 202606 is passed
while (year < 2026) or (year == 2026 and month <= 6):
    sold_filename = f'csv/monthly_sold/CRMLSSold{year}{month:02d}.csv'
    sold = pd.read_csv(sold_filename)

    sold_df.append(sold)

    sold_row_count += len(sold)

    month += 1
    # increment year if month passes cycle
    if month > 12:
        month = 1
        year += 1

# combine all dataframes
sold_final = pd.concat(sold_df)

print(f'Sold rows before concatenation: {sold_row_count}')
### Sold rows before concatenation: 3713642
print(f'Sold rows after concatenation: {len(sold_final)}')
### Sold rows after concatenation: 3713642

# ------------------------------------------------------
# Filtering
# ------------------------------------------------------
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']

print(f'Sold rows after filtering: {len(sold_final)}')
### Sold rows after filtering: 2706093

# save dataframe as csv file
#sold_final.to_csv('csv/CRMLSSoldCS.csv', index=False)