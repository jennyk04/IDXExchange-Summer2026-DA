import pandas as pd
from datetime import date

# several datasets include two additional columns at the end; labeled with '_filled'
## safely remove the columns and save as new csv files

target_files = ['202403', '202404', '202405', 
                '202406', '202407', '202501']

for file in target_files:
    filename = f'csv/CRMLSSold{file}_filled.csv'
    df = pd.read_csv(filename)
    df = df.iloc[:, :-2]

    new_filename = f'csv/CRMLSSold{file}.csv'
    df.to_csv(new_filename, index=False)

year = 2024
month = 1

# store sold dataframes in a list
## reduces need to concatenate after every new dataframe
sold_df = []

# record before concatenation row counts
sold_row_count = 0

# end loop after 202605 is passed
while (year < 2026) or (year == 2026 and month <= 5):
    sold_filename = f'csv/CRMLSSold{year}{month:02d}.csv'
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
# Sold rows before concatenation: 639878
print(f'Sold rows after concatenation: {len(sold_final)}')
# Sold rows after concatenation: 639878

sold_before_filter = len(sold_final)
# filter to Residential properties
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
sold_after_filter = len(sold_final)

print(f'Sold rows before filtering: {sold_before_filter}')
# Sold rows before filtering: 639878
print(f'Sold rows after filtering: {sold_after_filter}')
# Sold rows after filtering: 430437

# save dataframe as csv file
sold_final.to_csv('csv/CRMLSSoldFinal.csv', index=False)