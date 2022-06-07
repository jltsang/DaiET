def ufsearch_meal(user, rec_data, rec_attr, rec_cat, meal_start):
    nutrients = []
    meal_list = []

    if len(rec_cat) == 0:
        print("No available categories. Exiting...")
        return meal_list, nutrients, 0

    else:
        # random start for breakfast
        meal_list.append(meal_start)

        nutrients += [rec_data.loc[meal_list[0]][rec_attr[i]]/rec_data.loc[meal_list[0]]["RecipeServings"] for i in range(len(rec_attr))]
        max = 0
        max_x = 0
        max_y = 0
        max_nut = []

        # depth first search
        for idx, row in rec_data[rec_data["RecipeCategory"] == rec_cat[1]].iterrows():
            temp_nutrients = nutrients.copy()
            temp_nutrients = [row[rec_attr[i]]/row["RecipeServings"] for i in range(len(rec_attr))]
            temp_nutrients = [nutrients[j] + temp_nutrients[j] for j in range(len(nutrients))]

            for idy, row2 in rec_data[rec_data["RecipeCategory"] == rec_cat[2]].iterrows():
                temp2_nutrients = temp_nutrients.copy()
                temp2_nutrients = [row2[rec_attr[i]]/row2["RecipeServings"] for i in range(len(rec_attr))]
                temp2_nutrients = [temp_nutrients[j] + temp2_nutrients[j] for j in range(len(temp_nutrients))]
                sub = temp2_nutrients.copy()
        
                for j in range(len(rec_attr)):
                    temp2_nutrients[j] /= user.threshold[rec_attr[j]]
                    if temp2_nutrients[j] > 1:
                        temp2_nutrients[j] = 2 - temp2_nutrients[j]

                temp_heuristic = sum(temp2_nutrients)
                if temp_heuristic > max:
                    max = temp_heuristic
                    max_x = idx
                    max_y = idy
                    max_nut = sub.copy()

        
        meal_list.append(max_x)
        meal_list.append(max_y)
        nutrients = max_nut.copy()
        for meal in range(len(meal_list)):
            print(rec_cat[meal]+": "+rec_data.loc[meal_list[meal]]["Name"])
        print("Heuristic: "+str(max)+"\n")

    return meal_list, nutrients, max