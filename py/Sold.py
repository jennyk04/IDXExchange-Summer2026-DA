import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

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

# ------------------------------------------------------
# Week 1: Monthly Dataset Aggregation
# ------------------------------------------------------

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
### Sold rows before concatenation: 639878
print(f'Sold rows after concatenation: {len(sold_final)}')
### Sold rows after concatenation: 639878

# ------------------------------------------------------
# Week 2/3: Dataset Structuring and Validation
# ------------------------------------------------------

# Inspect Structure
print(sold_final.columns)
print(f'Columns in Sold Listing Dataset: {len(sold_final.columns)}')
### Columns in Sold Listing Dataset: 82

# check column data types and change according to the Real Estate Primer guide
print(sold_final.dtypes)

##### -------------------------------------------------- 
# expected data types
numeric_fields = ['ClosePrice','ListPrice','OriginalListPrice','LivingArea','AboveGradeFinishedArea',
                  'BelowGradeFinishedArea','BuildingAreaTotal','LotSizeAcres','LotSizeArea', 'LotSizeSquareFeet',
                  'BedroomsTotal','BathroomsTotalInteger','FireplacesTotal','GarageSpaces','CoveredSpaces',
                  'ParkingTotal','MainLevelBedrooms','Stories','DaysOnMarket','YearBuilt','TaxAnnualAmount',
                  'TaxYear','AssociationFee','Latitude','Longitude','StreetNumberNumeric','ListingKeyNumeric',
                  'BuyerAgencyCompensation']

date_fields = ['CloseDate','ListingContractDate','PurchaseContractDate','ContractStatusChangeDate']

categorical_fields = [
    # IDs
    'ListingKey','ListingId','BuyerAgentMlsId',

    # Agent names
    'ListAgentFirstName','ListAgentLastName','ListAgentFullName','CoListAgentFirstName',
    'CoListAgentLastName','BuyerAgentFirstName','BuyerAgentLastName','CoBuyerAgentFirstName',

    # Offices
    'ListOfficeName','BuyerOfficeName','CoListOfficeName',

    # Other text
    'ListAgentEmail','CountyOrParish','MLSAreaMajor','PropertyType','PropertySubType',
    'City','StateOrProvince','PostalCode','SubdivisionName','ElementarySchool',
    'MiddleOrJuniorSchool','HighSchool','ElementarySchoolDistrict','MiddleOrJuniorSchoolDistrict',
    'HighSchoolDistrict','BuilderName','Levels','Flooring','AssociationFeeFrequency',
    'BusinessType','LotSizeDimensions','UnparsedAddress','OriginatingSystemName',
    'OriginatingSystemSubName','BuyerAgentAOR','BuyerOfficeAOR','ListAgentAOR',
    'BuyerAgencyCompensationType','MlsStatus'
]

bool_fields = ['ViewYN','WaterfrontYN','BasementYN','PoolPrivateYN',
               'AttachedGarageYN','FireplaceYN','NewConstructionYN']


# TODO: change column data types after selecting important features
## report the DtypeWarning that shows up during the initial read_csv scripts

##### -------------------------------------------------- 

print(sold_final.head())

# Check property categories
print(sold_final['PropertyType'].unique())
### 'Residential', 'CommercialLease', 'Land', 'ResidentialLease',
### 'ManufacturedInPark', 'ResidentialIncome', 'CommercialSale',
### 'BusinessOpportunity'

sold_before_filter = len(sold_final)
# filter to Residential properties
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
sold_after_filter = len(sold_final)

print(f'Sold rows before filtering: {sold_before_filter}')
### Sold rows before filtering: 639878
print(f'Sold rows after filtering: {sold_after_filter}')
### Sold rows after filtering: 430437

# Validate completeness: count NA values per columns and flag >90% missing
print(sold_final.isnull().sum())
percent_missing = sold_final.isnull().sum() * 100 / len(sold_final)
print(percent_missing)

# summary table listing features with >90% missing
missing_summary = pd.DataFrame({'Missing Count': sold_final.isnull().sum(),
                                'Missing Percent': sold_final.isnull().mean() * 100}).round(2)

missing_summary = missing_summary[missing_summary['Missing Percent'] > 90]
print(missing_summary)

# Decided to drop everything but BuildingAreaTotal
sold_final = sold_final.drop(columns=['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount',
                                      'BuilderName', 'TaxYear', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName',
                                      'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions',
                                      'MiddleOrJuniorSchoolDistrict'])

print(f'Rows after removing missing columns: {len(sold_final.columns)}')
### Rows after removing missing columns: 68

##### -------------------------------------------------- 
# Analyze the distribution of key numeric fields
# For each field, generate plots and summaries that identify extreme outliers
# Ensure each feature has their expected data type prior to implementation
##### -------------------------------------------------- 

key_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
              'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

print(sold_final[key_fields].dtypes)

# ------------------------------------------------------
# Numeric Distribution Review (percentile summaries)
# ------------------------------------------------------

print(sold_final[key_fields].describe())

# ------------------------------------------------------
# Extreme Outliers (IQR)
# ------------------------------------------------------
outliers = []

for feature in key_fields:
    # calculate IQR from first and third quartile
    Q1 = sold_final[feature].quantile(0.25)
    Q3 = sold_final[feature].quantile(0.75)
    IQR = Q3 - Q1

    # limits for extreme outliers
    # below lower bound or above upper bound are outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # count the number of outliers
    outlier_count = ((sold_final[feature] < lower_bound) | (sold_final[feature] > upper_bound)).sum()
    # percentage of outliers
    outlier_percent = outlier_count / len(sold_final) * 100

    outliers.append({'Feature': feature, 'Q1': Q1, 'Q3': Q3, 'IQR': IQR,
                            'Lower Bound': lower_bound, 'Upper Bound': upper_bound,
                            'Outlier Count': outlier_count, 'Outlier Percent': outlier_percent})

outlier_summary = pd.DataFrame(outliers).round(2)
print(outlier_summary)


# ------------------------------------------------------
# Histograms
# ------------------------------------------------------

# histograms with outliers
# 3x3 figure to display 9 plots in one image
fig, axes = plt.subplots(3, 3, figsize=(15, 12))
axes = axes.flatten()

for i, feature in enumerate(key_fields):
    sold_final[feature].dropna().hist(
        bins=50,
        ax=axes[i]
    )

    axes[i].set_title(feature)
    axes[i].set_xlabel("")
    axes[i].set_ylabel("Frequency")

plt.tight_layout()
plt.show()

# identified percential cutoffs for each field to remove outliers from histograms
percentile_cutoffs = {
    'ClosePrice': 0.99,
    'ListPrice': 0.99,
    'OriginalListPrice': 0.99,
    'LivingArea': 0.995,
    'LotSizeAcres': 0.98,
    'BedroomsTotal': 1.00,
    'BathroomsTotalInteger': 1.00,
    'DaysOnMarket': 0.99,
    'YearBuilt': 1.00
}

# 3x3 figure to display 9 plots in one image
fig, axes = plt.subplots(3, 3, figsize=(16, 12))
axes = axes.flatten()

for i, feature in enumerate(key_fields):

    data = sold_final[feature].dropna()

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

# for boxplots, keep outliers
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()

for i, feature in enumerate(key_fields):
    axes[i].boxplot(sold_final[feature].dropna(), vert=False)
    axes[i].set_title(feature)
    axes[i].set_xlabel("")

plt.tight_layout()
plt.show()

# save dataframe as csv file
sold_final.to_csv('csv/CRMLSSoldFinal.csv', index=False)