import pandas as pd

def load_recipes(recipe_path="./csv_files/recipes.csv"):
    nutrient_labels = [
        "Calories", "CarbohydrateContent", "FatContent", "ProteinContent", "FiberContent"
    ]
    recipes = pd.read_csv(recipe_path)
    recipes = recipes.dropna(subset=["Name"] + nutrient_labels + ["RecipeServings"])
    return recipes, nutrient_labels