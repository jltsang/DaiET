class User:
    age_floor = [1, 3, 6, 10, 13, 16, 19, 30, 50, 60,
                 70]  #lower bound of each age group
    calories = [(1000, 920), (1350, 1260), (1600, 1470), (2060, 1980),
                (2700, 2170), (3010, 2280), (2530, 1930), (2420, 1870),
                (2420, 1870), (2140, 1610), (1960, 1540)]
    protein = [(18, 17), (22, 21), (30, 29), (43, 46), (62, 57), (72, 61),
               (71, 62), (71, 62), (71, 62), (71, 62), (71, 62)]
    fat = [(0, 0) for i in range(len(protein))]
    carbohydrates = [(0, 0) for i in range(len(protein))]
    for i in range(len(protein)):
        if i == 0:
            fat[i] = (round(protein[i][0] * 2.86), round(protein[i][1] * 2.86))
            carbohydrates[i] = ((round(protein[i][0] * 5.67),
                                 round(protein[i][1] * 5.67)))
        elif i < 6:
            fat[i] = ((round(protein[i][0] * 2.14),
                       round(protein[i][1] * 2.14)))
            carbohydrates[i] = ((round(protein[i][0] * 6.38),
                                 round(protein[i][1] * 6.38)))
        else:
            fat[i] = ((round(protein[i][0] * 1.8), round(protein[i][1] * 1.8)))
            carbohydrates[i] = ((round(protein[i][0] * 5.2),
                                 round(protein[i][1] * 5.2)))                   
    fiber = [(i, i) for i in [7, 10, 14, 17, 20, 23, 25, 25, 25, 25, 25]]

    threshold_table = {
        "Calories": calories,
        "CarbohydrateContent": carbohydrates,
        "FatContent": fat,
        "ProteinContent": protein,
        "FiberContent": fiber
    }
    threshold_units = {
        "Calories": "kcal",
        "CarbohydrateContent": "g",
        "FatContent": "g",
        "ProteinContent": "g",
        "FiberContent": "g"
    }

    def __init__(self, age=20, sex="male"):
        self.update_status(age, sex)

    def update_status(self, age, sex):
        self.age = int(age)
        self.sex = (1 if sex.lower() in ["female", "f"] else 0)
        self.age_group = -1
        for i in range(len(self.age_floor)):
            if self.age_floor[i] <= self.age:
                self.age_group += 1
        self.update_threshold()

    def update_threshold(self,
                         nutrients=["Calories", "CarbohydrateContent", "FatContent", "ProteinContent", "FiberContent"]):
        self.threshold = {}

        for i in nutrients:
            self.threshold[i] = self.threshold_table[i][self.age_group][self.sex]