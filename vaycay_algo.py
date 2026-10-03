from pathlib import Path

import pandas as pd


dataset_path = Path(__file__).resolve().parent / "Country_Travel_Key_195_Countries_Final.csv"
df = pd.read_csv(dataset_path)


def temperature_matches(temp, preference):
    if preference == "Cold":
        return temp <= 10
    elif preference == "Mild":
        return temp > 10 and temp <= 20
    elif preference == "Warm":
        return temp > 20 and temp <= 28
    elif preference == "Hot":
        return temp > 28

    return False


def _importance_weights(preferences):
    trip_type_importance = preferences["trip_type_importance"]
    budget_importance = preferences["budget_importance"]
    temperature_importance = preferences["temperature_importance"]

    total_importance = (
        trip_type_importance
        + budget_importance
        + temperature_importance
    )

    return {
        "trip_type": trip_type_importance / total_importance,
        "budget": budget_importance / total_importance,
        "temperature": temperature_importance / total_importance,
    }

def recommend_countries(preferences):
    weights = _importance_weights(preferences)

    trip_type_weight = weights["trip_type"]
    budget_weight = weights["budget"]
    temperature_weight = weights["temperature"]

    def calculate_score(row):
        score = 0

        # Trip Type
        if row["Trip Type"] == preferences["trip_preference"]:
            score += trip_type_weight

        # Budget
        budget_difference = abs(
            row["Avg Trip Cost (1-5)"] - preferences["budget_preference"]
        )
        budget_match = 1 - (budget_difference / 4)
        score += budget_match * budget_weight

        # Temperature
        if temperature_matches(
            row["Avg Temp During Best Season (°C)"],
            preferences["temperature_preference"],
        ):
            score += temperature_weight

        return score

    scored_countries = df.copy()
    scored_countries["Score"] = scored_countries.apply(
        calculate_score,
        axis=1,
    )
    scored_countries["Recommendation %"] = (
        scored_countries["Score"] * 100
    )

    recommendations = scored_countries.sort_values(
        by="Score",
        ascending=False,
    )

    return recommendations[
        [
            "Country Name",
            "Most Popular Attraction",
            "Trip Type",
            "Best Season to Visit",
            "Avg Trip Cost (1-5)",
            "Avg Temp During Best Season (°C)",
            "Recommendation %",
            "Latitude",
            "Longitude",
        ]
    ].head(5)


def main():
    print("Data Load Check")
    print("Number of Countries: ", len(df))

    df.head()

    print("Columns in the dataset:")
    print(df.columns.tolist())

    print("\nDataset information:")
    df.info()

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nNumber of duplicate rows:", df.duplicated().sum())

    print("\nChoose your preferred trip type:")
    trip_types = df["Trip Type"].unique()
    for number, trip_type in enumerate(trip_types, start=1):
        print(f"{number}. {trip_type}")
    trip_choice = int(input("Enter your choice: "))
    trip_preference = trip_types[trip_choice - 1]
    print("\nSelected trip type:", trip_preference)

    print("\nChoose your preferred trip cost:")
    print("1. Very Low")
    print("2. Low")
    print("3. Moderate")
    print("4. High")
    print("5. Very High")
    budget_preference = int(
        input("Enter your preferred cost level (1-5): ")
    )
    print("\nSelected budget level:", budget_preference)

    print("\nChoose your preferred temperature:")
    print("1. Cold")
    print("2. Mild")
    print("3. Warm")
    print("4. Hot")
    temperature_choice = int(input("Enter your choice: "))
    temperature_preferences = {
        1: "Cold",
        2: "Mild",
        3: "Warm",
        4: "Hot",
    }
    temperature_preference = temperature_preferences[temperature_choice]
    print("\nSelected temperature:", temperature_preference)

    print("\nHow important is each category to you?")
    print("1 = Not Important")
    print("2 = Somewhat Important")
    print("3 = Important")
    print("4 = Very Important")
    trip_type_importance = int(input("\nTrip Type importance: "))
    budget_importance = int(input("Budget importance: "))
    temperature_importance = int(input("Temperature importance: "))

    preferences = {
        "trip_preference": trip_preference,
        "budget_preference": budget_preference,
        "temperature_preference": temperature_preference,
        "trip_type_importance": trip_type_importance,
        "budget_importance": budget_importance,
        "temperature_importance": temperature_importance,
    }
    weights = _importance_weights(preferences)

    print("\nYour calculated weights:")
    print("Trip Type:", round(weights["trip_type"] * 100, 2), "%")
    print("Budget:", round(weights["budget"] * 100, 2), "%")
    print("Temperature:", round(weights["temperature"] * 100, 2), "%")

    top_recommendations = recommend_countries(preferences)

    print("\n========================================")
    print("       YOUR VACATION RECOMMENDATIONS")
    print("========================================")
    print(top_recommendations.to_string(index=False))

    print("\n========================================")
    print("          TOP VACATION MATCHES")
    print("========================================")

    for _, row in top_recommendations.iterrows():
        percentage = round(row["Recommendation %"])
        print("\nCountry:", row["Country Name"])
        print("Popular Attraction:", row["Most Popular Attraction"])
        print("Trip Type:", row["Trip Type"])
        print("Best Season:", row["Best Season to Visit"])
        print("Average Trip Cost Level:", row["Avg Trip Cost (1-5)"])
        print(
            "Average Temperature:",
            row["Avg Temp During Best Season (°C)"],
            "°C",
        )
        print("Recommendation Match:", percentage, "%")
        print("----------------------------------------")


if __name__ == "__main__":
    main()