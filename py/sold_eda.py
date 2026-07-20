import pandas as pd
import matplotlib.pyplot as plt

# helper functions for organizing output
def print_section(title):
    print('\n' + '='  * 70)
    print(title.upper())
    print('=' * 70)

def print_subsection(title):
    print('\n' + '-' * 70)
    print(title)
    print('-' * 70)

def print_stat(label, value):
    print(f'{label:<20} {value}')

# %%
# ------------------------------------------------------
# Week 2/3: Dataset Structuring and Validation
# ------------------------------------------------------

sold_final = pd.read_csv('csv/CRMLSSoldFinal.csv')

print_section('Week 2/3: Dataset Structuring and Validation')
print_subsection('Data Structure')
# Inspect Structure
print_stat('Columns in Sold Dataset:', len(sold_final.columns))

# list all features
print('\nColumn Names:')
print(sold_final.columns.tolist())

# check column data types and change according to the Real Estate Primer guide
print('\nData Types:')
print(sold_final.dtypes)

print_subsection('Dataset Preview')
print(sold_final.head())

# %%
##### -------------------------------------------------- 
print_subsection('Property Type Filtering')
# Check property categories
print('Property types:')
print(sold_final['PropertyType'].unique())

sold_before_filter = len(sold_final)
# filter to Residential properties
sold_final = sold_final[sold_final['PropertyType'] == 'Residential']
sold_after_filter = len(sold_final)

print_stat('Sold rows before filtering:', sold_before_filter)
print_stat('Sold rows after filtering:', sold_after_filter)

# %%
##### -------------------------------------------------- 
print_section('Missing Value Review')

# Validate completeness: count NA values per columns and flag >90% missing
# summary table listing features with >90% missing
missing_summary = pd.DataFrame({'Missing Count': sold_final.isnull().sum(),
                                'Missing Percent': sold_final.isnull().mean() * 100}).round(2)

missing_summary = missing_summary[missing_summary['Missing Percent'] > 90]
print_subsection('Columns with >90% Missing Values')
print(missing_summary)

print_subsection('Column Removal')
# Decided to drop everything with >90% missing
drop_columns = ['WaterfrontYN', 'BasementYN', 'FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount',
                'BuilderName', 'TaxYear', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName',
                'BelowGradeFinishedArea', 'BusinessType', 'CoveredSpaces', 'LotSizeDimensions',
                'MiddleOrJuniorSchoolDistrict', 'BuildingAreaTotal']
sold_final = sold_final.drop(columns=drop_columns)

print_stat('Columns removed:', len(drop_columns))
print_stat('Columns after removing missing:', len(sold_final.columns))

##### -------------------------------------------------- 
# subdatasets for metadata and market analysis
market_fields = [

    # Transaction & Pricing
    'ClosePrice',
    'ListPrice',
    'OriginalListPrice',
    'DaysOnMarket',
    'ListingContractDate',
    'PurchaseContractDate',
    'CloseDate',
    'ContractStatusChangeDate',
    'MlsStatus',

    # Property Characteristics
    'LivingArea',
    'LotSizeAcres',
    'LotSizeArea',
    'LotSizeSquareFeet',
    'BedroomsTotal',
    'BathroomsTotalInteger',
    'GarageSpaces',
    'ParkingTotal',
    'MainLevelBedrooms',
    'Stories',
    'YearBuilt',
    'AssociationFee',
    'AssociationFeeFrequency',

    'AttachedGarageYN',
    'FireplaceYN',
    'ViewYN',
    'PoolPrivateYN',
    'NewConstructionYN',

    'Levels',
    'Flooring',

    # Property Classification
    'PropertyType',
    'PropertySubType',

    # Location
    'Latitude',
    'Longitude',
    'CountyOrParish',
    'City',
    'StateOrProvince',
    'PostalCode',
    'MLSAreaMajor',
    'SubdivisionName',
    'StreetNumberNumeric',
    'UnparsedAddress',

    # Schools
    'ElementarySchool',
    'MiddleOrJuniorSchool',
    'HighSchool',
    'HighSchoolDistrict'
]

metadata_fields = [

    # Listing identifiers
    'ListingKey',
    'ListingKeyNumeric',
    'ListingId',

    # Agent information
    'ListAgentFirstName',
    'ListAgentLastName',
    'ListAgentFullName',
    'ListAgentEmail',

    'BuyerAgentFirstName',
    'BuyerAgentLastName',
    'BuyerAgentMlsId',

    'CoListAgentFirstName',
    'CoListAgentLastName',

    'BuyerAgentAOR',
    'ListAgentAOR',

    # Office information
    'ListOfficeName',
    'BuyerOfficeName',
    'CoListOfficeName',
    'BuyerOfficeAOR',

    # MLS system
    'OriginatingSystemName',
    'OriginatingSystemSubName',

    # Compensation
    'BuyerAgencyCompensationType',
    'BuyerAgencyCompensation'
]

metadata_df = sold_final[metadata_fields].copy()
market_df = sold_final[market_fields].copy()

print_stat('Metadata subset shape:', metadata_df.shape)
print_stat('Market Analysis subset shape:', market_df.shape)

# save as new csv files
#metadata_df.to_csv('csv/CRMLSSold_Metadata.csv', index=False)
#market_df.to_csv('csv/CRMLSSold_Market.csv', index=False)


##### -------------------------------------------------- 
# Analyze the distribution of key numeric fields
# For each field, generate plots and summaries that identify extreme outliers
# Ensure each feature has their expected data type prior to implementation
##### -------------------------------------------------- 

print_section('Key Numeric Fields')

key_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
              'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

print(sold_final[key_fields].dtypes)

# ------------------------------------------------------
# Numeric Distribution Review (percentile summaries)
# ------------------------------------------------------
print_subsection('Percentile Summary')
print(sold_final[key_fields].describe())

# ------------------------------------------------------
# Extreme Outliers (IQR)
# ------------------------------------------------------
print_subsection('Extremme Outliers (IQR)')
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
print_section('Visualizations')
print_subsection('Histograms with Outliers')
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

# ------------------------------------------------------
print_subsection('Histograms excluding Outliers')
# identified percentile cutoffs for each field to remove outliers from histograms
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
print_subsection('Boxplots')
# for boxplots, keep outliers
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()

for i, feature in enumerate(key_fields):
    axes[i].boxplot(sold_final[feature].dropna(), vert=False)
    axes[i].set_title(feature)
    axes[i].set_xlabel("")

plt.tight_layout()
plt.show()

# %%
# ------------------------------------------------------
# Week 4/5: Data Cleaning and Preparation
# ------------------------------------------------------

print_section('WWeek 4/5: Data Cleaning and Preparation')

print_subsection('Data Structure')
# Inspect Structure
print_stat('Columns in Sold Dataset:', len(sold_final.columns))
print_stat('Rows in Sold Dataset:', len(sold_final))

print_subsection('Dataset Preview')
print(sold_final.head())

##### -------------------------------------------------- 
print_subsection('Date Consistency Checks')
# Check property categories
date_fields = ['CloseDate', 'PurchaseContractDate', 'ListingContractDate', 'ContractStatusChangeDate']

print(sold_final[date_fields].head())
print('Date Fields:')
print(sold_final[date_fields].dtypes)

for i in date_fields:
    sold_final[i] = pd.to_datetime(sold_final[i], errors='coerce')

print_subsection("Date types after conversion")
print(sold_final[date_fields].head())
print('Date Fields:')
print(sold_final[date_fields].dtypes)

##### -------------------------------------------------- 
print_subsection('Invalid numeric values')
print('ClosePrice')
print(sold_final['ClosePrice'].describe())

print(sold_final['ClosePrice'].dtype)

print_stat('Non-positive values:', (sold_final['ClosePrice'] <= 0).sum())
# remove values with <= 0 price; meaningless to analysis
sold_final = sold_final[sold_final['ClosePrice'] > 0]

print('----------------------------------------------------------------------') 
print('LivingArea')
print_subsection('Invalid numeric values: LivingArea')
print(sold_final['LivingArea'].describe())

print_stat('Non-positive values:', (sold_final['LivingArea'] <= 0).sum())
# remove values with <= 0 price; meaningless to analysis
sold_final = sold_final[sold_final['LivingArea'] > 0]

print('----------------------------------------------------------------------')
print('DaysOnMarket')
print_subsection('Invalid numeric values: DaysOnMarket')
print(sold_final['DaysOnMarket'].describe())

print_stat('Non-positive values:', (sold_final['DaysOnMarket'] < 0).sum())
# remove values with <= 0 price; meaningless to analysis
sold_final = sold_final[sold_final['DaysOnMarket'] >= 0]

print('----------------------------------------------------------------------')
print('BedroomsTotal')
print_subsection('Invalid numeric values: BedroomsTotal')
print(sold_final['BedroomsTotal'].describe())

print_stat('Non-positive values:', (sold_final['BedroomsTotal'] < 0).sum())
# remove values with <= 0 price; meaningless to analysis
sold_final = sold_final[sold_final['BedroomsTotal'] >= 0]

print('----------------------------------------------------------------------')
print('BathroomsTotalInteger')
print_subsection('Invalid numeric values: BathroomsTotalInteger')
print(sold_final['BathroomsTotalInteger'].describe())

print_stat('Non-positive values:', (sold_final['BathroomsTotalInteger'] < 0).sum())
# remove values with <= 0 price; meaningless to analysis
sold_final = sold_final[sold_final['BathroomsTotalInteger'] >= 0]

print('----------------------------------------------------------------------')
print_stat('Sold rows after removing invalid values:', len(sold_final))

##### -------------------------------------------------- 
print_subsection('Validate Logical Order of Date Fields')

# listing date occurs after the close date
sold_final['listing_after_close_flag'] = (sold_final['ListingContractDate'] > sold_final['CloseDate'])

# purchase date occurs after the close date
sold_final['purchase_after_close_flag'] = (sold_final['PurchaseContractDate'] > sold_final['CloseDate'])

# timeline is invalid because purchase happened before listing
sold_final['negative_timeline_flag'] = (sold_final['PurchaseContractDate'] < sold_final['ListingContractDate'])

flags = ['listing_after_close_flag', 'purchase_after_close_flag', 'negative_timeline_flag']
print(sold_final[flags].sum())

##### -------------------------------------------------- 
# Geographic Data Checks
# flag missing or invalid coordinates (non-california locations)

print_subsection('Geographic Data Checks')
geographic_fields = ['Latitude', 'Longitude']

# check data type
print(sold_final[geographic_fields].head())
print('Geographic Fields:')
print(sold_final[geographic_fields].dtypes)

for i in geographic_fields:
    sold_final[i] = pd.to_numeric(sold_final[i], errors='coerce')

print_subsection("Geographic types after conversion")
print(sold_final[geographic_fields].head())
print('Geographic Fields:')
print(sold_final[geographic_fields].dtypes)

print('----------------------------------------------------------------------')
# flag missing coordinates 
sold_final['missing_coordinates_flag'] = (sold_final['Latitude'].isna() | sold_final['Longitude'].isna())
print_stat('Missing coordinates:', sold_final['missing_coordinates_flag'].sum())

# sentinel null coordinates
sold_final['zero_coordinates_flag'] = ((sold_final['Latitude'] == 0) | (sold_final['Longitude'] == 0))
print_stat('Sentinel (zero) coordinates:', sold_final['zero_coordinates_flag'].sum())

# non-negative longitude (California coordinates should be negative)
sold_final['positive_lon_flag'] = (sold_final['Longitude'] > 0)
print_stat('Positive Longitude values:', sold_final['positive_lon_flag'].sum())

# out-of-state or implausible coordinates
sold_final['out_of_state_flag'] = ((sold_final['Latitude'] < 32) | (sold_final['Latitude'] > 42) | 
                                   (sold_final['Longitude'] < -124) | (sold_final['Longitude'] > -114))
print_stat('Out-of-state coordinates:', sold_final['out_of_state_flag'].sum())


# save dataframe as csv file
sold_final.to_csv('csv/CRMLSSoldFinal.csv', index=False)