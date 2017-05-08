"""
kalamatchkas.Recipe
saba pilots
description:  Recipe object, dataframe of a recipe
12.01.16
"""


import pandas as pd
import numpy as np
from .FoodListBase import FoodListBase
from .config import LINE_BEGIN, BASE_FIELDS
from .tools import create_destination, test_print, order_columns


class Recipe(FoodListBase):

    def __init__(self, dataframe=None, name=None):
        """Load dataframe into recipe."""
        self.dataframe = dataframe
        self.log_by_version = list()
        self.log_by_grocery_list = list()
        self.log_by_sum = pd.DataFrame()
        self.log_by_food = pd.DataFrame(columns=['food'])
        self.write_name(name)


    @property
    def name(self):
        return self.__name
        
        
    @property
    def log_by_version(self):
        return self.__log_by_version
    
    
    @log_by_version.setter
    def log_by_version(self, value):
        assert (type(value) == list), LINE_BEGIN + "ERROR: non list assigned to log_by_version property"
        self.__log_by_version = value


    @property
    def log_by_grocery_list(self):
        return self.__log_by_grocery_list
    
    
    @log_by_grocery_list.setter
    def log_by_grocery_list(self, value):
        assert (type(value) == list), LINE_BEGIN + "ERROR: non list assigned to log_by_grocery_list property"
        self.__log_by_grocery_list = value
        
    
    @property
    def log_by_sum(self):
        return self.__log_by_sum
    
    
    @log_by_sum.setter
    def log_by_sum(self, value):
        assert (type(value) in (pd.core.frame.DataFrame, pd.core.series.Series) or not value), LINE_BEGIN + "ERROR: non dataframe/series/none assigned to log_by_sum property"
        if type(value) in (pd.core.frame.DataFrame, pd.core.series.Series):
            self.__log_by_sum = value
        else:
            self.__log_by_sum = pd.DataFrame()
    
    
    @property
    def log_by_food(self):
        return self.__log_by_food
    
    
    @log_by_food.setter
    def log_by_food(self, value):
        assert (type(value) in (pd.core.frame.DataFrame, pd.core.series.Series) or not value), LINE_BEGIN + "ERROR: non dataframe/series/none assigned to log_by_food property"
        if type(value) in (pd.core.frame.DataFrame, pd.core.series.Series):
            self.__log_by_food = value
        else:
            self.__log_by_food = pd.DataFrame(columns=['food'])
    
    
    @property
    def grocery_list(self):
        grocery_df = self.dataframe.groupby("food").sum()[["serving","gram"]]
        grocery_df.loc[:, "ounce"] = grocery_df["gram"] * 0.03527396
        grocery_df.loc[:, "pound"] = grocery_df["gram"] * 0.00220462
        return grocery_df
    
    
    def summarize(self, print_out=False, fields=None, day=False):
        """Summarize and return the nutrient levels of a recipe, option to print as well."""
        if day:
            summary_df = self.dataframe.reset_index().groupby(["level_0"]).sum()
        else:
            summary_df = self.dataframe.sum()
        
        summary_recipe = Recipe(summary_df)
        summary_recipe.calculate_calorie_percents()

        food_group_totals = self.dataframe.groupby('food_group')['serving'].sum()
        
        if not fields:
            fields = summary_recipe.dataframe.index
        
        if print_out:
            print(pd.concat([summary_recipe.dataframe[fields], food_group_totals]))

        return pd.concat([summary_recipe.dataframe[fields], food_group_totals]), summary_recipe.dataframe["total_cal"]
    
    
    def log(self, diet, replacement=None):
        """Update the recipe logs."""
        
        self.log_by_version.append(self.dataframe)
        self.log_by_grocery_list.append(self.dataframe.groupby("food").sum()[["serving","gram"]])
        
        key_fields = BASE_FIELDS
        key_fields.extend([rule[0] for rule in diet.nutrient_rules  if rule[0] not in BASE_FIELDS])
        
        summary, total_cal = self.summarize(fields=key_fields)
        
        if replacement:
            summary['food_replaced'] = replacement[0]['food']
            summary['food_replaced_serving'] = replacement[0]['serving']
            summary['food_added'] = replacement[1]['food']
            summary['food_added_serving'] = replacement[1]['serving']
        
        self.log_by_sum = self.log_by_sum.append(summary, ignore_index=True)
        
        col_len = len(self.log_by_food.columns)
        self.log_by_food = pd.merge(self.log_by_food, self.dataframe[['food','serving']], on='food', how='outer', suffixes=(col_len-2,col_len-1))
        self.log_by_food.rename(columns={'serving':'serving'+str(col_len-1)}, inplace=True)
    
    
    def test_maxday(self, print_results=False):
        """Test whether a recipe follows all the food maximums."""
        conditional = bool(True) & (
            ( self.dataframe["gram"] > self.dataframe["max_grams_day"] )
            & ( self.dataframe["max_grams_day"] != -1 )
        )
        
        result_df = self.dataframe.loc[conditional , ["food","gram","max_grams_day"]]
        result_final = result_df.empty
        
        test_print(result_final, result_df, "Max gram/day", verbose=print_results)
        
        return result_final
    
    
    def test_diet(self, diet, print_results=False):
        """Test whether a recipe fits all the dietary rules."""        
        recipe_sum, calories = self.summarize()
        
        conditionals = bool(True)
        conditionals_dict = dict()

        rules = list()
        rules.extend(diet.nutrient_rules)
        rules.extend(diet.calorie_range)
        rules.extend(diet.foodgroup_rules)
        
        for column in [rule[0] for rule in diet.foodgroup_rules]:
            if column not in recipe_sum.index:
                recipe_sum[column] = 0
            
        for rule in rules:
            boolean_rule = (rule[1] <= recipe_sum[rule[0]] <= rule[2])
            conditionals_dict[rule[0]] = boolean_rule
            conditionals &= boolean_rule
        
        test_print(conditionals, conditionals_dict, "Key field rules", verbose=print_results)
        
        return conditionals
        
        
    def test_foodlist(self, food_list, print_results=False):
        """Test whether a recipe fits all the dietary rules.""" 
        food_list_copy = food_list.copy()
        
        # replace serving column with servings from recipe and regram
        food_list_copy.dataframe.drop('serving', axis=1, inplace=True)
        food_list_copy.dataframe = pd.merge(food_list_copy.dataframe, self.dataframe[['food','serving']], how='inner', on='food')
        food_list_copy.re_gram(n_serving=True)
        
        # sort by food name and reset index, using only float columns
        fields_to_use = [col for col in food_list_copy.dataframe.columns if food_list_copy.dataframe[col].dtype == "float64" and col != "gram_ratio"]
        food_list_copy.dataframe = food_list_copy.dataframe.sort_values('food').reset_index(drop=True)[fields_to_use]
        self_dataframe_copy = self.dataframe[food_list_copy.dataframe.columns][fields_to_use]
        
        # test equivalence of dataframes, using numpy.isclose for floating points
        test_df = pd.DataFrame(np.isclose(food_list_copy.dataframe, self_dataframe_copy), columns=fields_to_use)
        
        result_cols = test_df.all()
        result_final = test_df.values.all()
        
        test_print(result_final, result_cols, "Food list", verbose=print_results)
        
        return result_final
    

    def test_rules(self, diet, print_results=False):
        """Test whether a recipe fits all the rules of diet and max foods."""
        result = self.test_diet(diet, print_results) & self.test_maxday(print_results)
        
        return result

        
    def test_compare_foods(self, diet, print_results=True):
        """Test whether last replacement moved closer to all goals."""
        current_row = self.log_by_sum.iloc[-1].fillna(0)
        prior_row = self.log_by_sum.iloc[-2].fillna(0)

        for column in [rule[0] for rule in diet.foodgroup_rules]:
            for row in [current_row, prior_row]:
                if column not in row.index:
                    row[column] = 0
                
        conditionals = bool(True)
        conditionals_dict = dict()

        for name, conditional, values in self.test_compare_foods_keyfields(diet, current_row, prior_row):
            conditionals &= conditional
            conditionals_dict[name] = conditional, values
            
        maxday_name, maxday_conditional, maxday_values = self.test_compare_foods_maxday(current_row)
        conditionals &= maxday_conditional
        conditionals_dict[maxday_name] = maxday_conditional, maxday_values
        
        test_print(conditionals, conditionals_dict, "Compare foods", verbose=print_results)
        
        return conditionals

    
    def test_compare_foods_keyfields(self, diet, current_row, prior_row):
        """Test whether last replacement moved closer to all goals."""
        rules = list()
        rules.extend(diet.nutrient_rules)
        rules.extend(diet.calorie_range)
        rules.extend(diet.foodgroup_rules)
        
        for rule in rules:
            target = (rule[1] + rule[2])/2
            old_recipe_diff = abs(prior_row[rule[0]] - target)
            new_recipe_diff = abs(current_row[rule[0]] - target)
            
            boolean_rule = (
                ( (rule[1] <= current_row[rule[0]]) & (current_row[rule[0]] <= rule[2]) )
                | (new_recipe_diff <= old_recipe_diff)
            )
            
            yield rule[0], boolean_rule, (current_row[rule[0]], prior_row[rule[0]])


    def test_compare_foods_maxday(self, current_row):
        """Test whether last replacement moved closer to all goals.
        Check that recent replacement did not go over maximum amount."""
        new_food_row = self.dataframe.loc[self.dataframe["food"] == current_row["food_added"], :].iloc[0]
        maxday_rule = (
            ( new_food_row["gram"] <= new_food_row["max_grams_day"] )
            | ( new_food_row["max_grams_day"] == -1 )
        )
        
        
        return "max_grams_day", maxday_rule, (new_food_row["food"], new_food_row["gram"])
        

    def test(self, diet, food_list, print_results=True):
        """Test that a recipe fits all the rules and is correctly constituted from the food list."""
        self.test_rules(diet, print_results=print_results)
        self.test_foodlist(food_list, print_results=print_results)
    
    
    def save(self, output_directory, detail=True, log_on=False):
        """Save recipe and log of recipe to csv file."""
        dest, detail_dest, log_by_sum_dest, log_by_food_dest = create_destination(output_directory, self.name, 'csv')
        
        out_grocery_df = self.grocery_list
        out_grocery_df.to_csv(dest, index=True)
        
        if detail:
            columns = order_columns(self.dataframe.columns.tolist())
            out_df = self.dataframe[columns]
            out_df.to_csv(detail_dest, index=False)
        
        if log_on:
            out_log_by_sum = self.log_by_sum
            out_log_by_sum.to_csv(log_by_sum_dest, index=True)
        
            out_log_by_food = self.log_by_food
            out_log_by_food.to_csv(log_by_food_dest, index=False)
    
    
    def write_name(self, name):
        """Write out a name for the recipe.  Default is 'day'."""
        if not name:
            self.__name = "day"
        else:
            self.__name = name
    
    
    def write_instructions(self):
        pass    
        
    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
