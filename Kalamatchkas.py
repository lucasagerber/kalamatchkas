"""
kalamatchkas.Kalamatchkas
saba pilots
description:  Kalamatchkas object that takes diet parameters and food lists, and returns random recipes
12.01.16
"""


import time
from collections import OrderedDict
import pandas as pd
from .FoodList import FoodList
from .Recipe import Recipe
from .Diet import Diet
from .tools import k_print
from .config import FOOD_PATH, OUT_DIREC, FOOD_LIST, LINE_BEGIN, BASE_FIELDS, API_KEY, DEBUG
from .Doron import DORONDIET


class Kalamatchkas(object):

    def __init__(self, food_list, diet, debug=False):
        """Initalize kalamatchkas object."""
        food_list.calculate_maxday(diet)
        
        self.__debug = debug
        self.__food_list = food_list
        self.__diet = diet
        self.__key_fields = BASE_FIELDS
        self.__key_fields.extend([rule[0] for rule in self.diet.nutrient_rules  if rule[0] not in BASE_FIELDS])
        self.__food_group_fields = [rule[0] for rule in self.diet.foodgroup_rules]
    

    @property
    def debug(self):
        return self.__debug

        
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
            
            recipe.save(directory, log_on=self.debug)
            k_print("Day {} compiled!\n".format(i))
        
        if grocery_list:
            grocery_list = Recipe(pd.concat(recipes), "grocery_list")
            grocery_list.save(directory, detail=False)


    def create_recipe(self):
        """Create a random recipe based on dietary rules and calorie requirements."""    
        k_print("Compiling ...")
        
        start_time = time.time()
        
        recipe = Recipe()
        
        while recipe.dataframe.empty:
            
            self.food_list.re_gram(serving_size=True)
            
            # Step 1:  fill up the recipe
            
            recipe = self.fill_recipe(recipe)
            
            if self.debug:
                recipe.test_maxday(print_results=True)
            
            recipe.log(self.diet)
            
            # Step 2:  balance the nutrients
            
            if not recipe.test_rules(self.diet):
                k_print("Balancing the nutrients...")
                original_recipe, original_cal = recipe.summarize(fields=self.key_fields)
                
                recipe = self.balance_nutrients(recipe)
                
                if not recipe.dataframe.empty and self.debug:
                    k_print("Before balancing ...")
                    print(original_recipe)
                    k_print("After balancing ...")
        
        recipe.summarize(print_out=True, fields=self.key_fields)
            
        if self.debug:
            recipe.test(self.diet, self.food_list)
        
        k_print("Compiled...")
        
        end_time = time.time()
        
        elapsed_minutes = round((end_time - start_time) / 60, 2)
        
        k_print("Elapsed time: {} minutes".format(str(elapsed_minutes)))
        
        return recipe



    def fill_recipe(self, recipe):
        """Step 1:  Fill recipe up to calorie requirement by adding ingredients."""
        
        foodgroup_rule_mins = list()
        for rule in self.diet.foodgroup_rules:
            foodgroup_rule_mins.extend([rule[0]] * rule[1])
        
        food_list_maxday = self.food_list.copy()
        food_list_maxday_selector = maxday_condition_ize(food_list_maxday.dataframe)
        
        priority_dict = {"food":set()}
        
        for foodgroup in foodgroup_rule_mins:
            new_food_df = self.food_list.select_food({'food_group':foodgroup}, conditional=food_list_maxday_selector, priority_dict=priority_dict)
            recipe.add_food(new_food_df)
            food_list_maxday.add_food(new_food_df)
            food_list_maxday_selector = maxday_condition_ize(food_list_maxday.dataframe)
            priority_dict["food"].add(new_food_df["food"])
        
        while recipe.dataframe.empty or recipe.dataframe["total_cal"].sum() < self.diet.calories:
            new_food_df = self.food_list.select_food(conditional=food_list_maxday_selector, priority_dict=priority_dict)
            recipe.add_food(new_food_df)
            food_list_maxday.add_food(new_food_df)
            food_list_maxday_selector = maxday_condition_ize(food_list_maxday.dataframe)
            priority_dict["food"].add(new_food_df["food"])

        return recipe
    
    
    def balance_nutrients(self, recipe, iter=0, ratio=1):
        """Step 2:  Balance the nutrient levels of a random recipe through replacement, according to dietary rules."""       

        # compare every food in recipe to all foods in foodlist, and create dict of food >>> dataframe
        food_df_dict = self.create_food_compare_dict(recipe, ratio)
            
        # select all foods where the resulting comparison dataframe is not empty
        recipe.dataframe.loc[:, "compare_df"] = recipe.dataframe['food'].apply(lambda x: not food_df_dict[x].empty)
        recipe_df_select = recipe.dataframe[recipe.dataframe["compare_df"]]
        recipe.dataframe.drop("compare_df", axis=1, inplace=True)
        
        if recipe_df_select.empty:
            if iter < 1:
                self.food_list.re_gram(gram_pct=.5, verbose=True)
                recipe = self.balance_nutrients(recipe, iter+1)
            #elif iter == 1:
                #self.food_list.re_gram(serving_size=True, verbose=True)
                #k_print("Ratio = 0.5")
                #recipe = self.balance_nutrients(recipe, iter+1, ratio=.5)
            #elif iter == 2 and ratio <= 4:
                #k_print("Ratio = " + str(ratio*2))
                #recipe = self.balance_nutrients(recipe, iter, ratio*2)
            else:
                if self.debug:
                    recipe.write_name("failed_day")
                    recipe.save(OUT_DIREC, detail=True, log_on=True)
                k_print("Sorry, there are no options for this recipe")
                return Recipe()
            
        else:
            # select a food from recipe to replace
            food_replace_options = FoodList(self.food_list.dataframe[self.food_list.dataframe["food"].isin(recipe_df_select["food"].values)]).copy()
            food_replace = food_replace_options.select_food()
            
            # select a new food to replace with
            food_new_options = FoodList(food_df_dict[food_replace["food"]])
            food_new_options.complete()    # is this necessary?
            priority_dict = dict()
            priority_dict["food"] = recipe.dataframe["food"].values.tolist()
            food_new = food_new_options.select_food(priority_dict=priority_dict)
            
            # replace the two foods in the recipe, and print and log the replacement
            recipe.del_food(food_replace)
            recipe.add_food(food_new)
            
            k_print("{} serving(s) of {} replaced with {} serving(s) of {}".format(food_replace["serving"], food_replace["food"], food_new["serving"], food_new["food"]))
            
            recipe.log(self.diet, replacement=(food_replace, food_new))
            #if self.debug:
                #recipe.test_compare_foods(self.diet)
            
            # test if the recipe passes rules, and, if not, run balance nutrients again
            if not recipe.test_rules(self.diet):
                recipe = self.balance_nutrients(recipe, iter, ratio)
            
        return recipe


    def create_food_compare_dict(self, recipe, ratio=1):
        """Create a dictionary of foods that could be replaced with each other."""
        recipe_sum, recipe_calories = recipe.summarize()
        
        fields_needed = [rule.replace('_%', '') for rule in self.key_fields]

        food_list_recipe_df = self.food_list.dataframe[self.food_list.dataframe["food"].isin(recipe.dataframe["food"].values)]
        
        food_list_regram = self.food_list.copy()       
        food_list_regram.re_gram(gram_pct=ratio)
        food_list_regram.complete()
        
        food_df_dict = {food_row["food"]:self.compare_foods(food_list_regram, recipe, recipe_sum, food_row, fields_needed)  for i, food_row in food_list_recipe_df.iterrows()}
        
        return food_df_dict
        

    def compare_foods(self, food_list, recipe, recipe_sum, food_row, fields_needed):
        """Compare all possible foods to see if any will move closer to goals, based on a recipe and chosen food to replace."""
        
        # copy food list to use a comparison, delete the food being compared
        food_comparison = food_list.copy()
        food_comparison.dataframe = food_comparison.dataframe.loc[food_comparison.dataframe["food"] != food_row["food"], :]
       
        
        # run each comparison using dict of function and arguments, switch order after fixing issues
        compare_dict = OrderedDict([
            (self.compare_foods_keyfields, {
                "food_comparison": food_comparison,
                "recipe_sum": recipe_sum,
                "food_row": food_row,
                "fields_needed": fields_needed,
            }),
            (self.compare_foods_foodgroups, {
                "food_comparison": food_comparison,
                "recipe_sum": recipe_sum,
                "food_row": food_row,
            }),
            (self.compare_foods_improve, {
                "food_comparison": food_comparison,
                "recipe_sum": recipe_sum,
            }),
            (self.compare_foods_maxday, {
                "food_comparison": food_comparison,
                "recipe": recipe,
                "food_row": food_row,
            }),
        ])
        
        #k_print("Start:  {}".format(str(len(food_comparison.dataframe))), self.debug)
        
        for func, args in compare_dict.items():
            food_comparison.dataframe = func(**args)
            #k_print("{}, {}".format(func.__name__, str(len(food_comparison.dataframe))), self.debug)
            if food_comparison.dataframe.empty:
                break
        
        
        # return food list dataframe sliced to only those foods that fit all conditionals
        return food_list.dataframe.loc[food_list.dataframe["food"].isin(food_comparison.dataframe["food"].values), :]


    def compare_foods_keyfields(self, food_comparison, recipe_sum, food_row, fields_needed):
        """Compare all possible foods on key fields to see if any will move closer to goals, based on a recipe and chosen food to replace.
        Key fields:  calculate what key fields would be with replacement and slice."""
        food_comparison.dataframe[fields_needed] = food_comparison.dataframe[fields_needed] - food_row[fields_needed] + recipe_sum[fields_needed]
        food_comparison.calculate_calorie_percents()
        
        key_field_rules = list()
        key_field_rules.extend(self.diet.nutrient_rules)
        key_field_rules.extend(self.diet.calorie_range)
        
        return rule_slice(key_field_rules, food_comparison.dataframe, recipe_sum)
    
    
    def compare_foods_foodgroups(self, food_comparison, recipe_sum, food_row):
        """Compare all possible foods on food groups to see if any will move closer to goals, based on a recipe and chosen food to replace.
        Food groups:  calculate what food group totals would be with replacement and slice."""
        food_row_food_group = food_row[['food_group','serving']]
        compare_df = food_comparison.dataframe
        
        for column in self.food_group_fields:
            if column not in recipe_sum.index:
                recipe_sum[column] = 0
        
        recipe_sum_food_groups = pd.DataFrame(recipe_sum).T[self.food_group_fields]
        compare_df = compare_df.join(pd.concat([recipe_sum_food_groups] * len(compare_df), ignore_index=True))
        
        compare_df = compare_df.apply(calculate_food_group, axis=1, food_row_food_group=food_row_food_group)
        
        return rule_slice(self.diet.foodgroup_rules, compare_df, recipe_sum)
        

    def compare_foods_maxday(self, food_comparison, recipe, food_row):
        """Compare all possible foods on max grams/day to see if any will move closer to goals, based on a recipe and chosen food to replace."""
        compare_df = food_comparison.dataframe
        compare_df = pd.merge(compare_df, recipe.dataframe[["food","gram"]], on="food", how="left", suffixes=("","_recipe"))
        compare_df.loc[compare_df["food"]==food_row["food"], "gram_food"] = food_row["gram"]
        compare_df.loc[:, ["gram_recipe","gram_food"]] = compare_df.loc[:, ["gram_recipe","gram_food"]].fillna(0)
        compare_df.loc[:, "gram"] = compare_df.loc[:, "gram"] + compare_df.loc[:, "gram_recipe"] - compare_df.loc[:, "gram_food"]
        
        maxday_conditional = maxday_condition_ize(compare_df)
        
        return compare_df.loc[maxday_conditional, :].reset_index(drop=True)


    def compare_foods_improve(self, food_comparison, recipe_sum):
        """Compare foods to see if at least one rule improved."""
        
        rules = list()
        rules.extend(self.diet.nutrient_rules)
        rules.extend(self.diet.calorie_range)
        rules.extend(self.diet.foodgroup_rules)
        
        compare_df = food_comparison.dataframe
        
        return improve_slice(rules, compare_df, recipe_sum)
        
        

def maxday_condition_ize(dataframe):
    """Return boolean series denoting whether any food in df has reached maximum amount per day."""
    conditional = bool(True) & (
        ( dataframe["gram"] <= dataframe["max_grams_day"] )
        | ( dataframe["max_grams_day"] == -1 )
    )
    
    return conditional
    
        
def rule_slice(rules, compare_df, recipe_sum):
    """Slice a dataframe based on conditionals of improving rules and return sliced df."""
    
    conditionals = bool(True)
    
    for rule in rules:
        target = (rule[1] + rule[2])/2
        old_recipe_diff = abs(recipe_sum[rule[0]] - target)
        new_recipe_diff = abs(compare_df[rule[0]] - target)
        
        conditionals &= (
            ( (rule[1] <= compare_df[rule[0]]) & (compare_df[rule[0]] <= rule[2]) )
            | (new_recipe_diff <= old_recipe_diff)
        )

    return compare_df.loc[conditionals, :].reset_index(drop=True)

    
def improve_slice(rules, compare_df, recipe_sum):
    """Slice a dataframe based on conditionals of improving any rule and return sliced df."""
    
    conditionals = bool(False)
    
    for rule in rules:
        target = (rule[1] + rule[2])/2
        old_recipe_diff = abs(recipe_sum[rule[0]] - target)
        new_recipe_diff = abs(compare_df[rule[0]] - target)
        
        conditionals |= (
            ~( (rule[1] <= recipe_sum[rule[0]]) & (recipe_sum[rule[0]] <= rule[2]) )
            & (new_recipe_diff < old_recipe_diff)
        )

    return compare_df.loc[conditionals, :].reset_index(drop=True)
    
    
def calculate_food_group(dataframe, food_row_food_group):
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
    diet = Diet(**DORONDIET)
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
    K = Kalamatchkas(food_list, diet, DEBUG)
    K.day(OUT_DIREC, days=k_days)
    
    
if __name__ == "__main__":
    main()
