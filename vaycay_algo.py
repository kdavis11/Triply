import pandas as pd
df = pd.read_csv("Country_Travel_Key_195_Countries_Final.csv")

print("Data Load Check")
print("Number of Countries: ", len(df))

df.head()

print("Columns in the dataset:")
print(df.columns.tolist())

# Display dataset info
print("\nDataset information:")
df.info()

# Checking for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Checking for duplicate rows
print("\nNumber of duplicate rows:", df.duplicated().sum())

print("Choose your preferred activity:")
print("1. Beach")
print("2. Adventure")
print("3. Culture")
print("4. Nature")
print("5. City")

activity_choice = input("Enter your choice: ")

activities = {
    "1": "Beach",
    "2": "Adventure",
    "3": "Culture",
    "4": "Nature",
    "5": "City"
}

activity_preference = activities.get(activity_choice)

print("\nSelected activity:", activity_preference)
print("\nChoose your preferred geography:")
print("1. Beach/Coastal")
print("2. Tropical")
print("3. Mountain")
print("4. Urban")
print("5. Safari")
print("6. Historical")

geography_choice = input("Enter your choice: ")

geographies = {
    "1": "Beach/Coastal",
    "2": "Tropical",
    "3": "Mountain",
    "4": "Urban",
    "5": "Safari",
    "6": "Historical"
}

geography_preference = geographies.get(geography_choice)

print("\nSelected geography:", geography_preference)
print("\nChoose your preferred travel season:")
print("1. Winter")
print("2. Spring")
print("3. Summer")
print("4. Fall")

season_choice = input("Enter your choice: ")

seasons = {
    "1": "Winter",
    "2": "Spring",
    "3": "Summer",
    "4": "Fall"
}

season_preference = seasons.get(season_choice)

print("\nSelected season:", season_preference)

print("\nNow select how important each category is to you.")
print("1 = Not Important")
print("2 = Somewhat Important")
print("3 = Important")
print("4 = Very Important")

activity_importance = int(
    input("\nHow important is Activity? ")
)

geography_importance = int(
    input("How important is Geography? ")
)

season_importance = int(
    input("How important is Season? ")
)

# Add all of the importance levels together
total_importance = (
    activity_importance +
    geography_importance +
    season_importance
)

# Convert each importance level into a weight
activity_weight = activity_importance / total_importance
geography_weight = geography_importance / total_importance
season_weight = season_importance / total_importance

print("\nYour calculated weights:")
print("Activity:", round(activity_weight * 100, 2), "%")
print("Geography:", round(geography_weight * 100, 2), "%")
print("Season:", round(season_weight * 100, 2), "%")

