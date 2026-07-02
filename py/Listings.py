import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

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

# ------------------------------------------------------
# Week 2/3: Dataset Structuring and Validation
# ------------------------------------------------------

# Inspect Structure
print(listing_final.columns)
## dataset contains duplicates of columns:
### PropertyType.1, DaysOnMarket.1, LivingArea.1, Latitude.1

print(f'Columns in Sold Listing Dataset: {len(listing_final.columns)}')
### Columns in Listing Dataset: 84

# check column data types and change according to the Real Estate Primer guide
print(listing_final.dtypes)

print(listing_final.head())

# Check property categories
print(listing_final['PropertyType'].unique())
### 'Residential', 'CommercialLease', 'Land', 'ResidentialLease',
### 'ManufacturedInPark', 'ResidentialIncome', 'CommercialSale',
### 'BusinessOpportunity'

listing_before_filter = len(listing_final)
# filter to Residential properties
listing_final = listing_final[listing_final['PropertyType'] == 'Residential']
listing_after_filter = len(listing_final)

print(f'Listing rows before filtering: {listing_before_filter}')
# Listing rows before filtering: 930311
print(f'Listing rows after filtering: {listing_after_filter}')
# Listing rows after filtering: 591980

# Validate completeness: count NA values per columns and flag >90% missing
print(listing_final.isnull().sum())
percent_missing = listing_final.isnull().sum() * 100 / len(listing_final)
print(percent_missing)

# summary table listing features with >90% missing
missing_summary = pd.DataFrame({'Missing Count': sold_final.isnull().sum(),
                                'Missing Percent': sold_final.isnull().mean() * 100}).round(2)

missing_summary = missing_summary[missing_summary['Missing Percent'] > 90]
print(missing_summary)

# Decided to drop everything but BuildingAreaTotal
listing_final = listing_final.drop(columns=['FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName',
                                            'TaxYear', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea',
                                            'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict'])

print(f'Rows after removing missing columns: {len(listing_final.columns)}')
### Rows after removing missing columns: 72


##### -------------------------------------------------- 
# Analyze the distribution of key numeric fields
# For each field, generate plots and summaries that identify extreme outliers
# Ensure each feature has their expected data type prior to implementation
##### -------------------------------------------------- 

key_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
              'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

print(listing_final[key_fields].dtypes)

# ------------------------------------------------------
# Numeric Distribution Review (percentile summaries)
# ------------------------------------------------------

print(listing_final[key_fields].describe())

# ------------------------------------------------------
# Extreme Outliers (IQR)
# ------------------------------------------------------
outliers = []

for feature in key_fields:
    # calculate IQR from first and third quartile
    Q1 = listing_final[feature].quantile(0.25)
    Q3 = listing_final[feature].quantile(0.75)
    IQR = Q3 - Q1

    # limits for extreme outliers
    # below lower bound or above upper bound are outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # count the number of outliers
    outlier_count = ((listing_final[feature] < lower_bound) | (listing_final[feature] > upper_bound)).sum()
    # percentage of outliers
    outlier_percent = outlier_count / len(listing_final) * 100

    outliers.append({'Feature': feature, 'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
                            'Lower Bound': lower_bound, 'Upper Bound': upper_bound,
                            'Outlier Count': outlier_count, 'Outlier Percent': outlier_percent})

outlier_summary = pd.DataFrame(outliers).round(2)
outlier_summary

# ------------------------------------------------------
# Histograms
# ------------------------------------------------------

import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

for i, feature in enumerate(key_fields):
    listing_final[feature].dropna().hist(
        bins=50,
        ax=axes[i]
    )

    axes[i].set_title(feature)
    axes[i].set_xlabel("")
    axes[i].set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# identified percentile cutoffs for each field to remove outliers from histograms
percentile_cutoffs = {
    'ClosePrice': 0.995,
    'ListPrice': 0.99,
    'OriginalListPrice': 0.99,
    'LivingArea': 0.995,
    'LotSizeAcres': 0.98,
    'BedroomsTotal': 1.00,
    'BathroomsTotalInteger': 0.995,
    'DaysOnMarket': 0.99,
    'YearBuilt': 1.00
}

# 3x3 figure to display 9 plots in one image
fig, axes = plt.subplots(3, 3, figsize=(16, 12))
axes = axes.flatten()

for i, feature in enumerate(key_fields):

    data = listing_final[feature].dropna()

    upper = data.quantile(percentile_cutoffs[feature])

    axes[i].hist(data[data <= upper], bins=50)

    axes[i].set_title(feature)
    axes[i].set_xlabel("")
    axes[i].set_ylabel("Frequency")

plt.tight_layout()
plt.show()


# ------------------------------------------------------
# Boxplots
# ------------------------------------------------------

fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()

for i, col in enumerate(key_fields):
    axes[i].boxplot(listing_final[col].dropna(), vert=False)
    axes[i].set_title(col)
    axes[i].set_xlabel("")

plt.tight_layout()
plt.show()


# save dataframe as csv file
listing_final.to_csv('csv/CRMLSListingFinal.csv', index=False)