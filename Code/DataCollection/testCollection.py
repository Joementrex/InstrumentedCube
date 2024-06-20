import pandas as pd

# Example data
data = [
    [1, 0, 0, 0],
    [1, 1, 0, 1],
    [1, 1, 1, 1],
    [1, 1, 2, 1],
    [1, 1, 3, 0],
    [1, 2, 0, 1],
    [1, 2, 1, 0],
    [1, 2, 2, 0],
    [1, 2, 3, 1]
]

# Create a DataFrame
df = pd.DataFrame(data, columns=['X1', 'X2', 'X3', 'Target'])

# Save the DataFrame to a CSV file
df.to_csv('data.csv', index=False)