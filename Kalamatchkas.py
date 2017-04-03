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
from .tools import k_print
from .config import FOOD_PATH, OUT_DIREC, FOOD_LIST, LINE_BEGIN, BASE_FIELDS, API_KEY


class Kalamatchkas(object):

    def __init__(self, food_list, diet):
        """Initalize kalamatchkas object."""
        food_list.calculate_maxday(diet)
        
        self.__food_list = food_list
        self.__diet = diet
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
    def key_fields(self):
        return self.__key_fields
    
    
    @property
    def food_group_fields(self):
        return self.__food_group_fields
    
    
    def day(self, directory, days=1, grocery_list=True):
        """Create a day of random recipes based on dietary rules and calorie requirements."""
        recipes = list()
        
        k_print("Days to compile:  {}\n".format(days))
        
        for i in range(1,days+1):
            k_print("Day {}".format(i))
            
            recipe = self.create_recipe()
            recipes.append(recipe.dataframe)
            
            # compile into various meals for day (...and handle cooking values?)
            
            recipe.save(directory)
            k_print("Day {} compiled!\n".format(i))
        
        if grocery_list:
            grocery_list = Recipe(pd.concat(recipes), "grocery_list")
            grocery_list.save(directory, detail=False)


    def create_recipe(self):
        """Create a random recipe based on dietary rules and calorie requirements."""    
        k_print("Compiling ...")
        
        self.food_list.re_gram(serving_size=True)
        
        recipe = Recipe()
        
        # Step 1:  fill up the recipe
        
        recipe = self.fill_recipe(recipe)
        
        recipe.log(self.diet)
        
        # Step 2:  balance the nutrients
        
        if not recipe.test_rules(self.diet):
            k_print("Balancing the nutrients...")
            original_recipe, original_cal = recipe.summarize(fields=self.key_fields)
            
            recipe = self.balance_nutrients(recipe)
            
            k_print("Before balancing ...")
            print(original_recipe)
            k_print("After balancing ...")
            recipe.summarize(print_out=True, fields=self.key_fields)
        
        recipe.test(self.diet, self.food_list)
        k_print("Compiled...")
        
        return recipe



    def fill_recipe(self, recipe):
        """Step 1:  Fill recipe up to calorie requirement by adding ingredients."""
        
        foodgroup_rule_mins = list()
        for rule in self.diet.foodgroup_rules:
            foodgroup_rule_mins.extend([rule[0]] * rule[1])
        
        food_list_maxday = FoodList(self.food_list.dataframe.copy())
        food_list_maxday_selector = bool(True) & (
            ( food_list_maxday.dataframe["gram"] <= food_list_maxday.dataframe["max_grams_day"] )
            | ( food_list_maxday.dataframe["max_grams_day"] == -1 )
        )
        
        for foodgroup in foodgroup_rule_mins:
            new_food_df = self.food_list.select_food({'food_group':foodgroup}, conditional=food_list_maxday_selector)
            recipe.add_food(new_food_df)
            food_list_maxday.add_food(new_food_df)
        
        while recipe.dataframe.empty or recipe.dataframe["total_cal"].sum() < self.diet.calories:
            new_food_df = self.food_list.select_food(conditional=food_list_maxday_selector)
            recipe.add_food(new_food_df)
            food_list_maxday.add_food(new_food_df)
            
        return recipe
    
    
    def balance_nutrients(self, recipe, iter=0, ratio=1):
        """Step 2:  Balance the nutrient levels of a random recipe through replacement, according to dietary rules."""       
        recipe_food_list = recipe.dataframe["food"].values
        food_df_dict = {food:self.compare_foods(recipe, food, ratio)  for food in recipe_food_list}

        recipe.dataframe.loc[:, "compare_df"] = recipe.dataframe['food'].apply(lambda x: not food_df_dict[x].empty)
        recipe_df_select = recipe.dataframe[recipe.dataframe["compare_df"]]
        recipe.dataframe.drop("compare_df", axis=1, inplace=True)
        
        if recipe_df_select.empty:
            if iter < 4:
                self.food_list.re_gram(gram_pct=.5, verbose=True)
                recipe = self.balance_nutrients(recipe, iter+1)
            elif iter == 4:
                self.food_list.re_gram(serving_size=True, verbose=True)
                k_print("Ratio = 0.01")
                recipe = self.balance_nutrients(recipe, iter+1, ratio=.01)
            elif iter == 5 and ratio <= 200:
                k_print("Ratio = " + str(ratio*2))
                recipe = self.balance_nutrients(recipe, iter, ratio*2)
            else:
                k_print("Sorry, there are no options for this recipe")
        else:
            food_list_copy = self.food_list.dataframe.copy()
            food_replace_options = FoodList(food_list_copy[self.food_list.dataframe["food"].isin(recipe_df_select["food"].values)])
            food_replace_options.re_gram(gram_pct=ratio)    # regram only if the ratio doesn't equal 1?
            food_replace = food_replace_options.select_food()
            
            food_new_options = Recipe(food_df_dict[food_replace["food"]])
            food_new_options.complete()    # is this necessary?
            food_new = food_new_options.select_food()
            
            recipe.del_food(food_replace)
            recipe.add_food(food_new)
            
            k_print("{0} serving(s) of {1} replaced with {2} serving(s) of {3}".format(food_replace["serving"], food_replace["food"], food_new["serving"], food_new["food"]))
            
            recipe.log(self.diet, replacement=(food_replace, food_new))
            
            if not recipe.test_rules(self.diet):
                recipe = self.balance_nutrients(recipe, iter, ratio)
            
        return recipe
    

    def compare_foods(self, recipe, food, ratio=1):
        """Compare all possible foods to see if any will move closer to goals, based on a recipe and chosen food to replace."""
        fields_needed = [rule.replace('_%', '') for rule in self.key_fields]
        
        recipe_sum, recipe_calories = recipe.summarize()
        
        self.food_list.complete()
        
        food_comparison = Recipe(self.food_list.dataframe.copy())
        
        food_row = self.food_list.dataframe.loc[self.food_list.dataframe["food"]==food, :] * ratio
        food_row_food_group = self.food_list.dataframe.loc[self.food_list.dataframe["food"]==food, ['food_group','serving']].iloc[0]
        
        # calculate what key fields would be with replacement
        food_comparison.dataframe[fields_needed] = food_comparison.dataframe[fields_needed] - food_row.iloc[0][fields_needed] + recipe_sum[fields_needed]
        food_comparison.calculate_calorie_percents()

        # calculate what gram amount would be with replacement
        food_comparison.dataframe = pd.merge(food_comparison.dataframe, recipe.dataframe[['food','gram']], on='food', how='left', suffixes=('','_recipe'))
        food_comparison.dataframe = pd.merge(food_comparison.dataframe, food_row[['food','gram']], on='food', how='left', suffixes=('','_food'))
        food_comparison.dataframe.loc[:, ['gram_recipe','gram_food']] = food_comparison.dataframe.loc[:, ['gram_recipe','gram_food']].fillna(0)
        food_comparison.dataframe.loc[:, 'gram'] = food_comparison.dataframe.loc[:, 'gram'] + food_comparison.dataframe.loc[:, 'gram_recipe'] - food_comparison.dataframe.loc[:, 'gram_food']
        
        # calculate what food group totals would be with replacement
        for column in self.food_group_fields:
            if column not in recipe_sum.index:
                recipe_sum[column] = 0
                
        recipe_sum_food_groups = pd.DataFrame(recipe_sum).T[self.food_group_fields]
        
        food_comparison.dataframe = food_comparison.dataframe.join(pd.concat([recipe_sum_food_groups] * len(food_comparison.dataframe), ignore_index=True))
        
        food_comparison.dataframe = food_comparison.dataframe.apply(compare_food_group, axis=1, food_row_food_group=food_row_food_group)
        
        # compute conditionals and return dataframe
        conditionals = bool(True)
        conditionals &= ( food_comparison.dataframe["food"] != food )
        conditionals &= (
            ( food_comparison.dataframe["gram"] <= food_comparison.dataframe["max_grams_day"] )
            | ( food_comparison.dataframe["max_grams_day"] == -1 )
        )
        
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
