import pandas as pd

# List of the three daily sales CSV files
file_paths = [
    'data/daily_sales_data_0.csv',
    'data/daily_sales_data_1.csv',
    'data/daily_sales_data_2.csv'
]

# Create an empty list to store the processed dataframes
processed_data = []

for file in file_paths:
    # Read the CSV file into a pandas dataframe
    df = pd.read_csv(file)
    
    # 1. Filter the rows to only include "pink morsel"
    df = df[df['product'] == 'pink morsel'].copy()
    
    # 2. Clean the 'price' field by removing the '$' and converting it to a float
    df['price'] = df['price'].str.replace('$', '').astype(float)
    
    # 3. Create the 'sales' field by multiplying 'quantity' and 'price'
    df['Sales'] = df['quantity'] * df['price']
    
    # 4. Select only the necessary columns and capitalize them for the final output
    df = df[['Sales', 'date', 'region']]
    df.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)
    
    # Append the processed dataframe to our list
    processed_data.append(df)

# Combine all the processed dataframes into a single dataframe
final_df = pd.concat(processed_data, ignore_index=True)

# Write the final combined dataframe to a new CSV file
output_file = 'data/formatted_daily_sales.csv'
final_df.to_csv(output_file, index=False)

print(f"Data processing complete! Formatted output saved to '{output_file}'")