import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from sklearn.metrics import pairwise_distances_argmin_min

# Create a DataFrame from the CSV data
df = pd.read_csv(r"C:\Users\rasua\OneDrive\Documents\GitHub\WWCodeHack-2023\Data\final_data.csv")

# Assume user provides input in a dictionary format
user_input = {
    'Academic': 2,
    'Attendance': 3, 
    '6': 2.0,
    '7': 3,
    '8': 3.0,
    '9': 3.0,
    '10': 2.0,
    '11': 2.0,
    '12': 2,
    '13': 3.0,
    '14': 4,
    '15': 3.0,
    '16': 4.0,
    '17': 4.0,
    'Course': 'Science and engineering'
}

# Extract the relevant columns for clustering
columns_for_clustering = ['Academic', 'Attendance', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']

# Subset the DataFrame with the selected columns
X = df[columns_for_clustering]

# Impute missing values
imputer = SimpleImputer(strategy='mean')  # You can choose a different strategy if needed
X_imputed = pd.DataFrame(imputer.fit_transform(X), columns=columns_for_clustering)

# Perform k-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)  # Adjust the number of clusters as needed
df['Cluster'] = kmeans.fit_predict(X_imputed)

# Find the cluster of the user input
user_input_values = [user_input[col] for col in columns_for_clustering]
user_cluster = kmeans.predict([user_input_values])[0]

# Find the most similar data point in the user's cluster
cluster_data = df[df['Cluster'] == user_cluster]
closest_point_idx = pairwise_distances_argmin_min([user_input_values], X_imputed.iloc[cluster_data.index])[0][0]
closest_point = df.iloc[closest_point_idx]

# Extract the relevant information for the closest point
hours_week = closest_point['hours_week']
days_studied_week = closest_point['days_studied_week']
hours_at_time = closest_point['hours_at_time']
time_day_studied = closest_point['time_day_studied']

# Print the results
print(f"Most similar data point to user input:\n{closest_point}")
print(f"\nRecommended study pattern:\n"
      f"Hours per week: {hours_week}\n"
      f"Days studied per week: {days_studied_week}\n"
      f"Hours at a time: {hours_at_time}\n"
      f"Time of day studied: {time_day_studied}")