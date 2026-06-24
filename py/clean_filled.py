import pandas as pd

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