import pandas as pd
import geopandas as gpd
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
# Week 6: Feature Engineering and Market Metrics
# ------------------------------------------------------

print_section('Week 6: Feature Engineering and Market Metrics')

# read school district GeoJSON into a GeoDataFrame
listing_final = pd.read_csv('csv/CRMLSListingFinal.csv')
print_stat('Listing dataset row count:', listing_final.shape[0])
district_geo = gpd.read_file('csv/school_district/DistrictAreas2526_-284845464123469011.geojson')
print(district_geo.head())
print_stat('Row count in district geodataframe:', district_geo.shape[0])
print_stat('Column count in district geodataframe:', district_geo.shape[1])

# filter to "Unified" school districts
print_subsection('Filter to "Unified" school district')
print(district_geo['DistrictType'].unique())
district_geo = district_geo[district_geo['DistrictType'] == 'Unified'].copy()
print_stat('Row count in after district filtering:', district_geo.shape[0])

# convert each property's Latitude and Longitude into a geographic point
print_subsection('Coordinates Conversion')
print('Observe geometry field, which stores each district as a polygon:')
print(district_geo['geometry'].head())

# convert listing_final into geodataframe with coordinates into geographic point
property_geo = gpd.GeoDataFrame(listing_final.copy(), geometry=gpd.points_from_xy(listing_final['Longitude'], listing_final['Latitude']), crs='EPSG:4326')
print()
print('Converted Listing dataframe into Property geodataframe:')
print(property_geo.head())

print()
print('Ensure both district and property geodataframes use same CRS:')
# CRS: coordinate reference system
district_geo = district_geo.to_crs(property_geo.crs)
print_stat("District CRS:", district_geo.crs)
print_stat("Property CRS:", property_geo.crs)

# perform spatial join to determine which unified district polygon contains each property
print_subsection("Spatial Join")
print('Spatial join to determine which unified district polygon each property belongs in.')

print_stat('Rows before spatial join:', property_geo.shape[0])
property_geo = gpd.sjoin(property_geo, district_geo[['DistrictName', 'geometry']], how='left', predicate='within')
# confirm that the spatial join did not remove or duplicate rows
print('Rows after spatial join:', property_geo.shape[0])

print()
print('District Names:')
print(property_geo['DistrictName'].unique()[:5])
print(property_geo['DistrictName'].head())

print_stat('Properties assigned a district:', property_geo['DistrictName'].notna().sum())
print_stat('Properties without a district:', property_geo['DistrictName'].isna().sum())
# 114341, assuming they are from invalid coordinates and non-unified districts

print_subsection('Unmapped District Review')
unmapped = property_geo['DistrictName'].isna()
print_stat('Unmapped with missing coordinates:', (unmapped & property_geo['missing_coordinates_flag']).sum())
print_stat('Unmapped with zero coordinates:', (unmapped & property_geo['zero_coordinates_flag']).sum())
print_stat('Unmapped with positive longitude:', (unmapped & property_geo['positive_lon_flag']).sum())
print_stat('Unmapped outside CA coordinates:', (unmapped & property_geo['out_of_state_flag']).sum())
print_stat('Unmapped CA coordinates:', (property_geo['DistrictName'].isna() & ~property_geo['missing_coordinates_flag'] &
                                        ~property_geo['out_of_state_flag'] & ~property_geo['positive_lon_flag'] & ~property_geo['zero_coordinates_flag']).sum())

# add resulting column into original listing dataframe
listing_final['DistrictName'] = property_geo['DistrictName']

# save dataframe as csv file
listing_final.to_csv('csv/CRMLSListingFinal.csv', index=False)