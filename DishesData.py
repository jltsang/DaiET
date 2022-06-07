class MealsData:
    def __init__(self, mealList):
        self.mealList = mealList # List of Meal instances

class Meal:
    def __init__(self, dishList, totalScore):
        assert len(dishList) <= 4
        self.dishList = dishList # List of Dish instances
        self.totalScore = totalScore # Int

    def getDish(self, dishNumber):
        if not (1 <= dishNumber <= len(self.dishList)):
            return None
        return self.dishList[dishNumber - 1]
        
        
class Dish:
    def __init__(self, name, ingredients, calories, protein, fat, carbs, fiber):
        self.name = name # String
        self.ingredients = ingredients # List of Strings
        self.calories = calories # Int
        self.protein = protein # Int
        self.fat = fat # Int
        self.carbs = carbs # Int
        self.fiber = fiber # Int