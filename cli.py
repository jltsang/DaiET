from users import User
from searchmeal import search_meal
from ufsearchmeal import ufsearch_meal
import pandas as pd
import random
from loadrecipes import load_recipes

'''
The nutrient thresholds are taken directly from the Philippine Dietary Reference Intakes 2015
https://www.fnri.dost.gov.ph/images/images/news/PDRI-2018.pdf

Loads the recipes from the database. The default database
is a subset of the "Food.com - Recipes and Reviews"
dataset from https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews
Units: calories - kCal, fat - g, protein - g, carbohydrates - g, fiber - g
'''


#terminal based text user interface
def text_ui(rec_data, rec_attr):
  user = User(input("Please input your age: "),input("Please input your biological sex (M/F): "))

  rec_cat_list = rec_data["RecipeCategory"].unique()
  rec_cat = rec_cat_list.copy()

  meals = []
  nutrients = []
  heuristics = []
  age = []
  sex = []

  u_meals = []
  u_nutrients = []
  u_heuristics = []

  while True:
    print("Current parameters:")
    print("Age:", str(user.age), "Sex:", "M" if user.sex == 0 else "F")
    print("[1] Generate a new set of meals.")
    print("[2] Change your parameters.")
    print("[3] Save all results generated to csv")
    print("[Other] Exit dAIet.")

    choice = input("Select an option: ")

    if choice == "1":
      rounds = int(input("Enter number of rounds: "))
      print("\nGenerating your meals...")
      for round in range(rounds):

        # random samples
        user.update_status(random.randint(1,80), random.choice("MF"))

        # comparison
        # new_rec = pd.concat([rec_data[rec_data["RecipeCategory"] == rec_cat[0]].sample(n=500), rec_data[rec_data["RecipeCategory"] == rec_cat[1]].sample(n=500)])
        # new_rec = pd.concat([new_rec, rec_data[rec_data["RecipeCategory"] == rec_cat[2]].sample(n=500)])
        # meal_start = new_rec[new_rec["RecipeCategory"] == rec_cat[0]].sample(n=1).index[0]
        # meal, nutrient, heuristic = search_meal(user, new_rec, rec_attr, rec_cat, meal_start)

        meal_start = rec_data[rec_data["RecipeCategory"] == rec_cat[0]].sample(n=1).index[0]
        meal, nutrient, heuristic = search_meal(user, rec_data, rec_attr, rec_cat, meal_start)
        # u_meal, u_nutrient, u_heuristic = ufsearch_meal(user, new_rec, rec_attr, rec_cat, meal_start)

        meals.append(meal)
        nutrients.append(nutrient)
        heuristics.append(heuristic)
        # u_meals.append(u_meal)
        # u_nutrients.append(u_nutrient)
        # u_heuristics.append(u_heuristic)
        age.append(user.age)
        sex.append("M" if user.sex == 0 else "F")

    elif choice == "2":
      user.update_status(input("Please input your age: "), input("Please input your biological sex (M/F): "))

    elif choice == "3":
      resultdict = {}
      resultdict["Meal Index"] = meals
      resultdict["Age"] = age
      resultdict["Sex"] = sex

      for i in range(len(rec_cat)):
        resultdict[rec_cat[i]] = [rec_data.loc[j[i]]["Name"] for j in meals]

      for i in range(len(rec_attr)):
        resultdict[rec_attr[i]] = [j[i] for j in nutrients]

      resultdict["Heuristic"] = heuristics     
      resultsdf = pd.DataFrame(resultdict)

      # saving the dataframe
      resultsdf.to_csv('searchresults.csv')

      # u_resultdict = {}
      # u_resultdict["Meal Index"] = u_meals
      # u_resultdict["Age"] = age
      # u_resultdict["Sex"] = sex
      # for i in range(len(rec_cat)):
      #   u_resultdict[rec_cat[i]] = [rec_data.loc[j[i]]["Name"] for j in u_meals]
      # for i in range(len(rec_attr)):
      #   u_resultdict[rec_attr[i]] = [j[i] for j in u_nutrients]
      # u_resultdict["Heuristic"] = u_heuristics     
      # u_resultsdf = pd.DataFrame(u_resultdict)
      # u_resultsdf.to_csv('uninformed_search_results.csv') 

    else:
        print("Exiting daIet...")
        exit()

#load database and launch text ui
def main():
    rec_data, rec_attr = load_recipes()
    text_ui(rec_data, rec_attr)

if __name__ == "__main__":
    print("Welcome to dAIet. Opening text interface now...")
    main()
