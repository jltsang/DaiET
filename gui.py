from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
from DishesData import MealsData, Meal, Dish
from loadrecipes import load_recipes
from searchmeal import search_meal
from users import User

GENDERS = ["", "Male", "Female"]
COLORS_DISH_CARD = "#f9f9f9"

mealsData = None
mealsDataIndex = 0

def callbackGenerateMeals():
    global errorMessageLabel
    global mealsData
    global mealsDataIndex

    try:
        ageInt = int(inputAge.get())
        if (not (1 <= ageInt <= 90)):
            errorMessageLabel["text"] = "Please enter a supported age!"
            return    
    except ValueError:
        errorMessageLabel["text"] = "Please enter a valid age!"
        return
    if len(inputGender.get()) == 0:
        errorMessageLabel["text"] = "Please select your gender!"
        return    
    errorMessageLabel["text"] = ""

    ########################################## EDIT CODE HERE 🔽
    # mealsData should be an instance of the MealsData class

    age = int(inputAge.get())
    gender = inputGender.get()
    rec_data, rec_attr = load_recipes()
    user = (age,gender)
    rec_cat_list = rec_data["RecipeCategory"].unique()
    rec_cat = rec_cat_list.copy()
    user = User(age, gender)
    meal_start = rec_data[rec_data["RecipeCategory"] == rec_cat[0]].sample(n=1).index[0]
    meal_search = search_meal(user, rec_data, rec_attr, rec_cat, meal_start)
    meals = meal_search[0]
    dish_list = []
    for i in range(len(meals)):
       parts = rec_data.loc[meals[i]]["RecipeIngredientParts"][2:-1].replace('\"','')
       NewDish = Dish(rec_data.loc[meals[i]]["Name"], parts.split(','), rec_data.loc[meals[i]]["Calories"],
                      rec_data.loc[meals[i]]["ProteinContent"], rec_data.loc[meals[i]]["FatContent"],
                      rec_data.loc[meals[i]]["CarbohydrateContent"], rec_data.loc[meals[i]]["FiberContent"])
       dish_list.append(NewDish)
    total = round(meal_search[2]/5 * 100,2)
    NewMeal = Meal(dish_list, total)
    
    mealsData = MealsData([NewMeal])

    ########################################## EDIT CODE HERE 🔼
    mealsDataIndex = 0
    updateData()


def callbackPreviousMeals():
    global mealsDataIndex
    global mealsData
    if (mealsData != None and mealsDataIndex > 0):
        mealsDataIndex -= 1
        updateData()

def callbackNextMeals():
    global mealsDataIndex
    global mealsData
    if (mealsData != None and mealsDataIndex < len(mealsData.mealList) - 1):
        mealsDataIndex += 1
        updateData()

def updateData():
    global dishFrameComponents
    global totalText
    global buttonPrevMeal
    global buttonNextMeal
    global buttonGenerate

    if (mealsData == None):
        return

    meal = mealsData.mealList[mealsDataIndex]
    
    for dishI in range(4):
        dish = meal.getDish(dishI + 1)
        dishFrameComponents[f"dish{dishI + 1}"]["ingredients"].delete(0,END)
        if (dish != None):
            for ingredient in dish.ingredients:
                dishFrameComponents[f"dish{dishI + 1}"]["ingredients"].insert(END, ingredient)
        dishFrameComponents[f"dish{dishI + 1}"]["name"]["text"] = "" if dish == None else dish.name
        dishFrameComponents[f"dish{dishI + 1}"]["calories"]["text"] = "" if dish == None else str(dish.calories)
        dishFrameComponents[f"dish{dishI + 1}"]["protein"]["text"] = "" if dish == None else str(dish.protein)
        dishFrameComponents[f"dish{dishI + 1}"]["fat"]["text"] = "" if dish == None else str(dish.fat)
        dishFrameComponents[f"dish{dishI + 1}"]["carbs"]["text"] = "" if dish == None else str(dish.carbs)
        dishFrameComponents[f"dish{dishI + 1}"]["fiber"]["text"] = "" if dish == None else str(dish.fiber)

        # if (dish == None):
        #     dishFrameComponents[f"dishFrame{dishI + 1}"].grid_remove()
        # else:
        #     dishFrameComponents[f"dishFrame{dishI + 1}"].grid()
    
    totalText["text"] = "Total Rating: " + str(meal.totalScore)
    buttonPrevMeal["state"] = "disabled" if mealsDataIndex == 0 else "normal"
    buttonNextMeal["state"] = "disabled" if mealsDataIndex == len(mealsData.mealList) - 1 else "normal"

    buttonGenerate["text"] = "Regenerate!"

    
root = Tk()
root.title("DAIET - AI Based Meal Generation")
root.iconbitmap("./gui/daiet.ico")

# Variables
inputAge = StringVar()
inputGender = StringVar()
inputGender.set(GENDERS[0])

mainFrame = Frame(root)

# Frame : Logo
logoFrame = Frame(mainFrame)
logoImage = ImageTk.PhotoImage(Image.open("./gui/logo.png"))  
logoImageLabel = Label(logoFrame, image = logoImage)
logoImageLabel.pack()
logoFrame.grid(row=0, column=0)

# Frame : Input
frameInput = Frame(mainFrame)
Label(frameInput, text = "Age").grid(row=0,column=0)
frameInputAgeEntry = Entry(frameInput, textvariable=inputAge, width=5)
frameInputAgeEntry.insert(0, "")
frameInputAgeEntry.grid(row=0,column=1,padx=(0,10))
Label(frameInput, text = "Gender").grid(row=0,column=2)
op = ttk.OptionMenu(frameInput, inputGender, *GENDERS)
op.config(width=8)
op.grid(row=0,column=3,padx=(0,10))
buttonGenerate = Button(frameInput, text ="Generate Meals!", command = callbackGenerateMeals)
buttonGenerate.grid(row=0,column=4)
frameInput.grid(row=1, column=0)

# Frame : Error Message
errorMessageLabel = Label(mainFrame, text = "", fg="red")
errorMessageLabel.grid(row=2,column=0)

# Frame : Generated Meals
frameGenerateMeals = Frame(mainFrame)
ttk.Separator(frameGenerateMeals).grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
Label(frameGenerateMeals, text = "G E N E R A T E D   M E A L S", font=("Helvetica", 9, 'bold'), fg="#aaaaaa").grid(row=1, column=0, pady=(10, 5))
frameMealsGrid = Frame(frameGenerateMeals)
def dishFrame(frameMealsGrid, row, column, componentMap, dishData):
    dish = Frame(frameMealsGrid)
    dishContent = Frame(dish, bg= COLORS_DISH_CARD)
    dishUpperPanel = Frame(dishContent, bg= COLORS_DISH_CARD)
    Label(dishUpperPanel, text = "Name:", bg= COLORS_DISH_CARD).grid(row=0,column=0, sticky='e')
    componentMap["name"] = Label(dishUpperPanel, text = "" if dishData == None else dishData.name, bg= COLORS_DISH_CARD, font=("Helvetica", 9, 'bold'))
    componentMap["name"].grid(row=0,column=1, sticky='w')
    Label(dishUpperPanel, text = "Ingredients:", bg= COLORS_DISH_CARD).grid(row=1,column=0, sticky='en')
    ingredientsFrame = Frame(dishUpperPanel)
    scrollbar = Scrollbar(ingredientsFrame)
    scrollbar.pack(side = RIGHT, fill = BOTH)
    componentMap["ingredients"] = Listbox(ingredientsFrame)
    componentMap["ingredients"].pack(side = LEFT, fill = BOTH)
    componentMap["ingredients"].config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = componentMap["ingredients"].yview)
    ingredientsFrame.grid(row=1,column=1)
    dishUpperPanel.grid(row=0, column=0, padx=(10, 0), pady=(10, 10))
    ttk.Separator(dishContent).grid(row=1, column=0, sticky="ew", padx=10)
    dishLowerPanel = Frame(dishContent, bg= COLORS_DISH_CARD)
    Label(dishLowerPanel, text = "Calories", bg= COLORS_DISH_CARD).grid(row=0,column=0)
    Label(dishLowerPanel, text = "Protein", bg= COLORS_DISH_CARD).grid(row=0,column=1)
    Label(dishLowerPanel, text = "Fat", bg= COLORS_DISH_CARD).grid(row=0,column=2)
    Label(dishLowerPanel, text = "Carbs", bg= COLORS_DISH_CARD).grid(row=0,column=3)
    Label(dishLowerPanel, text = "Fiber", bg= COLORS_DISH_CARD).grid(row=0,column=4)
    componentMap["calories"] = Label(dishLowerPanel, text =  "" if dishData == None else dishData.calories, bg= COLORS_DISH_CARD)
    componentMap["calories"].grid(row=1,column=0)
    componentMap["protein"] = Label(dishLowerPanel, text = "" if dishData == None else dishData.protein, bg= COLORS_DISH_CARD)
    componentMap["protein"].grid(row=1,column=1)
    componentMap["fat"] = Label(dishLowerPanel, text = "" if dishData == None else dishData.fat, bg= COLORS_DISH_CARD)
    componentMap["fat"].grid(row=1,column=2)
    componentMap["carbs"] = Label(dishLowerPanel, text =  "" if dishData == None else dishData.carbs, bg= COLORS_DISH_CARD)
    componentMap["carbs"].grid(row=1,column=3)
    componentMap["fiber"] = Label(dishLowerPanel, text = "" if dishData == None else dishData.fiber, bg= COLORS_DISH_CARD)
    componentMap["fiber"].grid(row=1,column=4)
    dishLowerPanel.grid(row=2, column=0, padx=10, pady=(0, 10))
    dishContent.grid(row=0, column=0, padx=5, pady=5)
    dish.grid(row=row, column=column)
    return dish

dishFrameComponents = {
    "dish1" : {},
    "dish2" : {},
    "dish3" : {},
    "dish4" : {}
}

dish1 = None if mealsData == None else (mealsData.mealList[mealsDataIndex].getDish(1))
dish2 = None if mealsData == None else (mealsData.mealList[mealsDataIndex].getDish(2))
dish3 = None if mealsData == None else (mealsData.mealList[mealsDataIndex].getDish(3))
dish4 = None if mealsData == None else (mealsData.mealList[mealsDataIndex].getDish(4))

dishFrameComponents["dishFrame1"] = dishFrame(frameMealsGrid, 0, 0, dishFrameComponents["dish1"], dish1)
dishFrameComponents["dishFrame2"] = dishFrame(frameMealsGrid, 0, 1, dishFrameComponents["dish2"], dish2)
dishFrameComponents["dishFrame3"] = dishFrame(frameMealsGrid, 1, 0, dishFrameComponents["dish3"], dish3)
dishFrameComponents["dishFrame4"] = dishFrame(frameMealsGrid, 1, 1, dishFrameComponents["dish4"], dish4)
# dishFrameComponents["dishFrame1"].grid_remove()
# dishFrameComponents["dishFrame2"].grid_remove()
# dishFrameComponents["dishFrame3"].grid_remove()
# dishFrameComponents["dishFrame4"].grid_remove()


frameMealsGrid.grid(row=2, column=0)
totalText = Label(frameGenerateMeals, text = "", font=("Helvetica", 10, 'bold'))
totalText.grid(row=3, column=0, pady=(10, 5))
frameGenerateMeals.grid(row=3, column=0)

# Frame : Lower Input
frameLowerInput = Frame(mainFrame)
buttonPrevMeal = Button(frameLowerInput, text ="Previous Meal", command = callbackPreviousMeals, state="disabled")
buttonPrevMeal.grid(row=0,column=0, padx=2)
buttonNextMeal = Button(frameLowerInput, text ="Next Meal", command = callbackNextMeals, state="disabled")
buttonNextMeal.grid(row=0,column=1, padx=2)
frameLowerInput.grid(row=4, column=0, pady=(10, 0))

mainFrame.grid(padx=10, pady=10)

root.resizable(False, False) 
root.mainloop()