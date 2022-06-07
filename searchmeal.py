def search_meal(user, rec_data, rec_attr, rec_cat, meal_start):
  nutrients = []
  meal_list = [] #stores only the index of the selected meals

  if len(rec_cat) == 0:
    print("No available categories. Exiting...")
    return -1

  # random start for breakfast
  meal_list.append(meal_start)

  nutrients += [rec_data.loc[meal_list[0]][rec_attr[i]]/rec_data.loc[meal_list[0]]["RecipeServings"] for i in range(len(rec_attr))]
  heuristic = 0

  
  # search for the best recipe in the next category
  for i in range(1,len(rec_cat)):
    max_index = None
    max_heuristic = 0

    for idx,row in rec_data[rec_data["RecipeCategory"] == rec_cat[i]].iterrows():
      temp_nutrients = nutrients.copy()

      # heuristic function
      for j in range(len(rec_attr)):
        temp_nutrients[j] += (row[rec_attr[j]]/row["RecipeServings"])
        temp_nutrients[j] /= user.threshold[rec_attr[j]]

        if temp_nutrients[j] > 1:
          temp_nutrients[j] = 2 - temp_nutrients[j]
          
      temp_heuristic = sum(temp_nutrients)

      # updating best choice    
      if temp_heuristic > max_heuristic:
        max_index = idx
        max_heuristic = temp_heuristic
        
    if max_index != None:
      meal_list.append(max_index)
      nutrients = [nutrients[j] + (rec_data.loc[max_index][rec_attr[j]]/rec_data.loc[max_index]["RecipeServings"]) for j in range(len(rec_attr))]
      heuristic = max_heuristic
      
  # All meals are chosen
  for meal in range(len(meal_list)):
    print(rec_cat[meal]+": "+rec_data.loc[meal_list[meal]]["Name"])
  print("Heuristic: "+str(heuristic)+"\n")

  return meal_list, nutrients, heuristic