"""
kalamatchkas.Kalmatchkas
saba pilots
description:  Kalamatchas object that takes diet parameters and food lists, and returns random recipes
12.01.16
"""


import random, os
from collections import OrderedDict
import pandas as pd
from .FoodList import FoodList
from .Recipe import Recipe
from .Diet import Diet
from .config import FOOD_PATH, OUT_PATH, LINE_BEGIN, RECIPE_COLUMNS, API_KEY


class Kalamatchkas(object):

    def __init__(self, food_list, diet):
        """Initalize kalamatchkas object."""
        self.__food_list = food_list
        self.__diet = diet
        self.__recipe = Recipe()
    
    
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
    
    
    def day(self):
        """Create a day of random recipes based on dietary rules and calorie requirements."""
        self.create_recipe()
        
        # compile into various meals for day (...and handle cooking values?)
        
        print(LINE_BEGIN + "Day of meals compiled!")


    def create_recipe(self):
        """Create a random recipe based on dietary rules and calorie requirements."""    
        print(LINE_BEGIN + "Compiling meal...")
        
        self.recipe = Recipe()
        
        while self.recipe.dataframe.empty or self.recipe.dataframe["total_cal"].sum() < self.diet.calories:
            new_food_df = self.food_list.select_food(1)
            self.recipe.add_food(new_food_df)
        
        if not self.recipe.test(self.diet):
            print(LINE_BEGIN + "Balancing the macronutrient levels...")
            original_recipe = Recipe(self.recipe.dataframe.copy())
            
            self.balance_macronutrients()

            print(LINE_BEGIN + "Before balancing ...")
            original_recipe.summarize(print_out=True)
            print(LINE_BEGIN + "After balancing ...")
            self.recipe.summarize(print_out=True)
            
        print(LINE_BEGIN + "Meal compiled...")


    def balance_macronutrients(self):
        """Balance the macronutrient levels of a random recipe through replacement, according to dietary rules."""
        # currently only works for 1 replacement. . .
        n_replaces = 1
        
        recipe_food_list = self.recipe.dataframe["food"].values
        food_df_dict = {food:self.compare_foods(food)  for food in recipe_food_list}

        self.recipe.dataframe["compare_df"] = self.recipe.dataframe.apply(lambda x: not food_df_dict[x["food"]].empty, axis=1)
        recipe_df_select = self.recipe.dataframe[self.recipe.dataframe["compare_df"]]
        self.recipe.dataframe.drop("compare_df", axis=1, inplace=True)
        
        if recipe_df_select.empty:
            print(LINE_BEGIN + "Sorry, there are no options for this recipe")
        else:
            food_replace_options = Recipe(self.food_list.dataframe[self.food_list.dataframe["food"].isin(recipe_df_select["food"].values)])
            
            food_replace = food_replace_options.select_food(n_replaces)
            food_new_options = Recipe(food_df_dict[food_replace["food"]])
            
            food_new = food_new_options.select_food(n_replaces)
            
            self.recipe.del_food(food_replace)
            self.recipe.add_food(food_new)
            
            print(LINE_BEGIN + food_replace["food"] + " replaced with " + food_new["food"])
            
            if not self.recipe.test(self.diet):
                self.balance_macronutrients()
    

    def compare_foods(self, food):
        """Compare all possible foods to see if any will move closer to goals, based on a recipe and chosen food to replace."""
        #print(LINE_BEGIN + "Comparing " + old_food + " to all possible foods...")
        
        recipe_sum, recipe_calories = self.recipe.summarize()
        
        fields_needed = ["protein_cal","carb_cal","fat_cal","total_cal"]

        self.food_list.calculate_calories()
        food_comparison = Recipe(self.food_list.dataframe)
        food_row = self.food_list.dataframe.loc[self.food_list.dataframe["food"]==food, fields_needed].iloc[0]
        food_comparison.dataframe[fields_needed] = food_comparison.dataframe[fields_needed] - food_row + recipe_sum[fields_needed]
        food_comparison.calculate_calorie_percents()
        
        conditionals = bool(True) & ( food_comparison.dataframe["food"] != food )
        
        rules = list()
        rules.extend(self.diet.macronutrient_rules)
        rules.extend(self.diet.calorie_range)
        
        for rule in rules:
            target = (rule[1] + rule[2])/2
            old_recipe_diff = abs(recipe_sum[rule[0]] - target)
            new_recipe_diff = abs(food_comparison.dataframe[rule[0]] - target)
            
            conditionals &= (
                ( (rule[1] <= food_comparison.dataframe[rule[0]]) & (food_comparison.dataframe[rule[0]] <= rule[2]) )
                | (new_recipe_diff <= old_recipe_diff)
            )

        return self.food_list.dataframe.loc[conditionals, :]


    def summarize(self, print_out=False, day=False):
        """Summarize the kalamatchkas recipe."""
        return self.recipe.summarize(print_out, day)
    
    
    def save(self, path):
        """Save the kalamatchkas recipe."""
        return self.recipe.save(path)
    
    
    
def main():
    diet = Diet("Doron's Diet")
    food_list = FoodList(FOOD_PATH, column="NDB_NO", api_key=API_KEY)
    K = Kalamatchkas(food_list, diet)
    K.day()
    K.summarize(print_out=True, day=False)
    K.save(OUT_PATH)
    
    
if __name__ == "__main__":
    main()
