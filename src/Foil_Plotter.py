import pandas as pd

# Load the CSV file with the correct delimiter
file_path = 'CFD_3D_skrzydla_przednie2023_batmanowe_NACA6409_Wyniki.csv'
df = pd.read_csv(file_path, delimiter=';')

#setting the right row for names of columns
df.columns = df.iloc[0]
df = df[1:]

# Reset the index
df.reset_index(drop=True, inplace=True)

# Display the DataFrame to check the new column names
print(df.head())