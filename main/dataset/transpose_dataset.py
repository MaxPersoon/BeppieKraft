import os
import pandas as pd

# Input = dataset where column indices are movieIDs and row indices are userIDs
# Output = dataset where column indices are userIDs and row indices are movieIDs
file_name = 'full_dataset.csv'
df_data = pd.read_csv(file_name)
df_data.index = df_data.iloc[:, 0]
df_data.index.name = "userID"
df_data = df_data.drop(df_data.columns[0], axis=1)
df_data.columns.name = "movieID"
print(df_data.head(5))
df_data = df_data.transpose()
print(df_data.head(5))
os.remove(file_name)
df_data.to_csv(file_name)
