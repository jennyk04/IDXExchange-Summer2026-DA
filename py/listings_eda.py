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

# ------------------------------------------------------
# Week 2/3: Dataset Structuring and Validation
# ------------------------------------------------------

listing_final = pd.read_csv('csv/CRMLSListingFinal.csv')

print_section('Week 2/3: Dataset Structuring and Validation')
print_subsection('Data Structure')
# Inspect Structure
print_stat('Columns in Listings Dataset:', len(listing_final.columns))

# list all features
print('\nColumn Names:')
print(listing_final.columns.tolist())

# check column data types and change according to the Real Estate Primer guide
print('\nData Types:')
print(listing_final.dtypes)

print_subsection('Dataset Preview')
print(listing_final.head())

##### -------------------------------------------------- 
print_subsection('Property Type Filtering')
# Check property categories
print('Property types:')
print(listing_final['PropertyType'].unique())

listing_before_filter = len(listing_final)
# filter to Residential properties
listing_final = listing_final[listing_final['PropertyType'] == 'Residential']
listing_after_filter = len(listing_final)

print_stat('Listings rows before filtering:', listing_before_filter)
print_stat('Listings rows after filtering:', listing_after_filter)

##### -------------------------------------------------- 
print_section('Missing Value Review')

# Validate completeness: count NA values per columns and flag >90% missing
# summary table listing features with >90% missing
missing_summary = pd.DataFrame({'Missing Count': listing_final.isnull().sum(),
                                'Missing Percent': listing_final.isnull().mean() * 100}).round(2)

missing_summary = missing_summary[missing_summary['Missing Percent'] > 90]
print_subsection('Columns with >90% Missing Values')
print(missing_summary)

print_subsection('Column Removal')
# Decided to drop everything but BuildingAreaTotal
# also drop duplicate columns (names with .1 at the end)
drop_columns = ['FireplacesTotal', 'AboveGradeFinishedArea', 'TaxAnnualAmount', 'BuilderName',
                'TaxYear', 'ElementarySchoolDistrict', 'CoBuyerAgentFirstName', 'BelowGradeFinishedArea',
                'BusinessType', 'CoveredSpaces', 'LotSizeDimensions', 'MiddleOrJuniorSchoolDistrict', 'PropertyType.1',
                'ListAgentFirstName.1', 'DaysOnMarket.1', 'LivingArea.1', 'Longitude.1', 'Latitude.1', 'ListPrice.1',
                'ListAgentLastName.1', 'CloseDate.1', 'BuyerOfficeName.1', 'UnparsedAddress.1']
listing_final = listing_final.drop(columns=drop_columns)

print_stat('Columns removed:', len(drop_columns))
print_stat('Columns after removing missing:', len(listing_final.columns))

##### -------------------------------------------------- 
# subdatasets for metadata and market analysis
market_fields = [

    # Pricing & Transaction
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
    'BuildingAreaTotal',
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
    'NewConstructionYN',

    # Classification
    'PropertyType',
    'PropertySubType',

    # Geographic
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

    # Office information
    'ListOfficeName',
    'BuyerOfficeName',
    'CoListOfficeName',
    'BuyerOfficeAOR',

    # Compensation
    'BuyerAgencyCompensation',
    'BuyerAgencyCompensationType'
]

metadata_df = listing_final[metadata_fields].copy()
market_df = listing_final[market_fields].copy()

print_stat('Metadata subset shape:', metadata_df.shape)
print_stat('Market Analysis subset shape:', market_df.shape)

# save as new csv files
metadata_df.to_csv('csv/CRMLSListing_Metadata.csv', index=False)
market_df.to_csv('csv/CRMLSListing_Market.csv', index=False)

##### -------------------------------------------------- 
# Analyze the distribution of key numeric fields
# For each field, generate plots and summaries that identify extreme outliers
# Ensure each feature has their expected data type prior to implementation
##### -------------------------------------------------- 

print_section('Key Numeric Fields')

key_fields = ['ClosePrice', 'ListPrice', 'OriginalListPrice', 'LivingArea', 'LotSizeAcres',
              'BedroomsTotal', 'BathroomsTotalInteger', 'DaysOnMarket', 'YearBuilt']

print(listing_final[key_fields].dtypes)

# ------------------------------------------------------
# Numeric Distribution Review (percentile summaries)
# ------------------------------------------------------
print_subsection('Percentile Summary')
print(listing_final[key_fields].describe())

# ------------------------------------------------------
# Extreme Outliers (IQR)
# ------------------------------------------------------
print_subsection('Extremme Outliers (IQR)')
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
    listing_final[feature].dropna().hist(
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
print_subsection('Boxplots')
# for boxplots, keep outliers
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()

for i, feature in enumerate(key_fields):
    axes[i].boxplot(listing_final[feature].dropna(), vert=False)
    axes[i].set_title(feature)
    axes[i].set_xlabel("")

plt.tight_layout()
plt.show()


# save dataframe as csv file
listing_final.to_csv('csv/CRMLSListingFinal.csv', index=False)