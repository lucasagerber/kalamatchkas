"""
kalamatchkas.Kalamatchkas
saba pilots
description:  Kalamatchkas object that takes diet parameters and food lists, and returns random recipes
12.01.16
"""


import time
import random, os
from collections import OrderedDict
import pandas as pd
from .FoodList import FoodList
from .Recipe import Recipe
from .Diet import Diet
from .config import FOOD_PATH, OUT_DIREC, FOOD_LIST, LINE_BEGIN, BASE_FIELDS, API_KEY


class Kalamatchkas(object):

    def __init__(self, food_list, diet):
        """Initalize kalamatchkas object."""
        self.__food_list = food_list
        self.__diet = diet
        self.__recipe = Recipe()
        self.__key_fields = BASE_FIELDS
        self.__key_fields.extend([rule[0] for rule in self.diet.nutrient_rules  if rule[0] not in BASE_FIELDS])
        self.__food_group_fields = [rule[0] for rule in self.diet.foodgroup_rules]
    
    
    @property
    def food_list(self):
        return self.__food_list
    
    
    @property
    def diet(self):
        return self.__diet
    

    @property
    def recipe(self):
        return self.__recipe

    
    @recipe.setter
    def recipe(self, value):
        assert type(value) == Recipe, LINE_BEGIN + "ERROR: non recipe assigned to recipe property"
        self.__recipe = value
    
    
    @property
    def key_fields(self):
        return self.__key_fields
        
        
    @property
    def food_group_fields(self):
        return self.__food_group_fields
    
    
    def day(self, directory, days=1):
        """Create a day of random recipes based on dietary rules and calorie requirements."""
        recipes = list()
        
        print(LINE_BEGIN + "Days to compile:  {}\n".format(days))
        
        for i in range(1,days+1):
            print(LINE_BEGIN + "Day {}".format(i))
            self.create_recipe()
            recipes.append(self.recipe.dataframe.copy())
            
            # compile into various meals for day (...and handle cooking values?)
            
            self.save(directory)
            print(LINE_BEGIN + "Day {} compiled!\n".format(i))
        
        grocery_df = pd.concat(recipes).groupby("food").sum()[["serving","gram"]]
        grocery_df.loc[:, "ounce"] = grocery_df["gram"] * 0.03527396
        grocery_df.loc[:, "pound"] = grocery_df["gram"] * 0.00220462
        
        grocery_list = Recipe(grocery_df, "grocery_list")
        grocery_list.save(directory, index=True)


    def create_recipe(self):
        """Create a random recipe based on dietary rules and calorie requirements."""    
        print(LINE_BEGIN + "Compiling meals...")
        
        self.recipe = Recipe()
        
        foodgroup_rule_mins = list()
        for rule in self.diet.foodgroup_rules:
            foodgroup_rule_mins.extend([rule[0]] * rule[1])
        
        for foodgroup in foodgroup_rule_mins:
            new_food_df = self.food_list.select_food({'food_group':foodgroup})
            self.recipe.add_food(new_food_df)
        
        while self.recipe.dataframe.empty or self.recipe.dataframe["total_cal"].sum() < self.diet.calories:
            new_food_df = self.food_list.select_food()
            self.recipe.add_food(new_food_df)
        
        self.recipe.log(self.diet)
        if not self.recipe.test_rules(self.diet):
            print(LINE_BEGIN + "Balancing the nutrients...")
            original_recipe = Recipe(self.recipe.dataframe.copy())
            
            self.balance_nutrients()
            
            self.check()
            
            print(LINE_BEGIN + "Before balancing ...")
            original_recipe.summarize(print_out=True, fields=self.key_fields)
            print(LINE_BEGIN + "After balancing ...")
            self.recipe.summarize(print_out=True, fields=self.key_fields)
            
        print(LINE_BEGIN + "Compiled...")


    def balance_nutrients(self, iter=0, ratio=1):
        """Balance the nutrient levels of a random recipe through replacement, according to dietary rules."""       
        recipe_food_list = self.recipe.dataframe["food"].values
        food_df_dict = {food:self.compare_foods(food, ratio)  for food in recipe_food_list}

        self.recipe.dataframe.loc[:, "compare_df"] = self.recipe.dataframe['food'].apply(lambda x: not food_df_dict[x].empty)
        recipe_df_select = self.recipe.dataframe[self.recipe.dataframe["compare_df"]]
        self.recipe.dataframe.drop("compare_df", axis=1, inplace=True)
        
        if recipe_df_select.empty:
            if iter < 4:
                self.food_list.re_gram(gram_pct=.5, verbose=True)
                self.balance_nutrients(iter+1)
            elif iter == 4:
                self.food_list.re_gram(serving_size=True, verbose=True)
                print(LINE_BEGIN + "Ratio = 0.01")
                self.balance_nutrients(iter+1, ratio=.01)
            elif iter == 5 and ratio <= 200:
                print(LINE_BEGIN + "Ratio = " + str(ratio*2))
                self.balance_nutrients(iter, ratio*2)
            else:
                #self.balance_nutrients(iter=0)
                print(LINE_BEGIN + "Sorry, there are no options for this recipe")
        else:
            food_list_copy = self.food_list.dataframe.copy()
            food_replace_options = FoodList(food_list_copy[self.food_list.dataframe["food"].isin(recipe_df_select["food"].values)])
            food_replace_options.re_gram(gram_pct=ratio)
            food_replace = food_replace_options.select_food()
            
            food_new_options = Recipe(food_df_dict[food_replace["food"]])
            food_new_options.calculate_servings()
            food_new = food_new_options.select_food()
            
            self.recipe.del_food(food_replace)
            self.recipe.add_food(food_new)
            
            print("{0}{1} serving(s) of {2} replaced with {3} serving(s) of {4}".format(LINE_BEGIN, food_replace["serving"], food_replace["food"], food_new["serving"], food_new["food"]))
            
            self.recipe.log(self.diet, replacement=(food_replace, food_new))
            if not self.recipe.test_rules(self.diet):
                self.balance_nutrients(iter, ratio)
    

    def compare_foods(self, food, ratio=1):
        """Compare all possible foods to see if any will move closer to goals, based on a recipe and chosen food to replace."""
        #print(LINE_BEGIN + "Comparing " + old_food + " to all possible foods...")
        
        fields_needed = [rule.replace('_%', '') for rule in self.key_fields]
        
        recipe_sum, recipe_calories = self.recipe.summarize()
        
        self.food_list.calculate_calories()
        self.food_list.calculate_servings()
        self.food_list.calculate_provitamin_a()
        
        food_comparison = Recipe(self.food_list.dataframe.copy())
        
        food_row = self.food_list.dataframe.loc[self.food_list.dataframe["food"]==food, fields_needed].iloc[0] * ratio
        food_row_food_group = self.food_list.dataframe.loc[self.food_list.dataframe["food"]==food, ['food_group','serving']].iloc[0]
        
        food_comparison.dataframe[fields_needed] = food_comparison.dataframe[fields_needed] - food_row + recipe_sum[fields_needed]
        food_comparison.calculate_calorie_percents()

        for column in self.food_group_fields:
            if column not in recipe_sum.index:
                recipe_sum[column] = 0
                
        recipe_sum_food_groups = pd.DataFrame(recipe_sum).T[self.food_group_fields]
        
        food_comparison.dataframe = food_comparison.dataframe.join(pd.concat([recipe_sum_food_groups] * len(food_comparison.dataframe), ignore_index=True))
        
        food_comparison.dataframe = food_comparison.dataframe.apply(compare_food_group, axis=1, food_row_food_group=food_row_food_group)
        
        conditionals = bool(True) & ( food_comparison.dataframe["food"] != food )
        
        rules = list()
        rules.extend(self.diet.nutrient_rules)
        rules.extend(self.diet.calorie_range)
        rules.extend(self.diet.foodgroup_rules)
        
        for rule in rules:
            target = (rule[1] + rule[2])/2
            old_recipe_diff = abs(recipe_sum[rule[0]] - target)
            new_recipe_diff = abs(food_comparison.dataframe[rule[0]] - target)
            
            conditionals &= (
                ( (rule[1] <= food_comparison.dataframe[rule[0]]) & (food_comparison.dataframe[rule[0]] <= rule[2]) )
                | (new_recipe_diff <= old_recipe_diff)
            )

        return self.food_list.dataframe.loc[conditionals, :]

        
    def check(self):
        self.recipe.test_rules(self.diet, print_results=True)
        self.recipe.test_foodlist(self.food_list, print_results=True)
    

    def summarize(self, print_out=False, day=False):
        """Summarize the kalamatchkas recipe."""       
        return self.recipe.summarize(print_out, self.key_fields, day)
    
    
    def save(self, directory, log_on=False):
        """Save the kalamatchkas recipe."""
        self.recipe.save(directory, log_on)
    
    
def compare_food_group(dataframe, food_row_food_group):
    """Compares the food groups in food list, using recipe and chosen food."""
    assert 'serving' in dataframe.index, LINE_BEGIN + "ERROR: no serving column in food comparison series"
    assert 'serving' in food_row_food_group.index, LINE_BEGIN + "ERROR: no serving column in food row series"
    
    try:
        dataframe[dataframe['food_group']] += dataframe['serving']
    except KeyError:
        pass
        
    try:
        dataframe[food_row_food_group['food_group']] -= food_row_food_group['serving']
    except KeyError:
        pass
    
    return dataframe
    
    
def main(k_days=7):
    diet = Diet("Doron's Diet")
    food_list = FoodList(FOOD_PATH,
                        gram_amt=50,
                        columns={
                            "ndb_nos":"NDB_NO",
                            "food_name":"food",
                            "serving_size":"Unnamed: 9",
                            "food_group":"food_group",
                            "max_grams_meal":"Unnamed: 12",
                            "max_grams_day":"Unnamed: 13"
                        },
                        food_list_path=FOOD_LIST,
                        api_key=API_KEY
    )
    K = Kalamatchkas(food_list, diet)
    K.day(OUT_DIREC, days=k_days)
    
    
if __name__ == "__main__":
    main()
