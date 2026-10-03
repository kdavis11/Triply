from flask import Flask, render_template, request

from vaycay_algo import df, recommend_countries

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/preferences")
def preferences():

    trip_types = df["Trip Type"].unique()
    

    return render_template(
        "preferences.html",
        trip_types=trip_types,
    )
@app.route("/recommendations", methods=["POST"])
def recommendations():
    try:
        preferences = build_preferences(request.form)
    except ValueError as error:
        return str(error), 400

    top_recommendations = recommend_countries(preferences)

    return render_template(
        "results.html",
        recommendations=top_recommendations.to_dict(orient="records"),
    )

    
def build_preferences(form):
    """Validate submitted values and adapt the form fields to the algorithm."""

    temperature_options = {
        1: "Cold",
        2: "Mild",
        3: "Warm",
        4: "Hot",
    }

    try:
        trip_type_preference = form["trip_type"]
        budget_preference = int(form["budget_preference"])
        temperature_choice = int(form["temperature_preference"])

        trip_type_importance = int(form["trip_type_importance"])
        budget_importance = int(form["budget_importance"])
        temperature_importance = int(form["temperature_importance"])

    except (KeyError, TypeError, ValueError) as error:
        raise ValueError(
            "Please complete every preference with a valid choice."
        ) from error

    if trip_type_preference not in set(df["Trip Type"]):
        raise ValueError("Please choose a valid trip type.")

    if budget_preference not in range(1, 6):
        raise ValueError("Please choose a budget from 1 to 5.")

    if temperature_choice not in temperature_options:
        raise ValueError("Please choose a valid temperature.")

    importance_values = (
        trip_type_importance,
        budget_importance,
        temperature_importance,
    )

    if any(value not in range(1, 5) for value in importance_values):
        raise ValueError("Importance values must be from 1 to 4.")

    return {
        "trip_preference": trip_type_preference,
        "budget_preference": budget_preference,
        "temperature_preference": temperature_options[temperature_choice],
        "trip_type_importance": trip_type_importance,
        "budget_importance": budget_importance,
        "temperature_importance": temperature_importance,
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)