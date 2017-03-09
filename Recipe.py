"""
kalamatchkas.Recipe
saba pilots
description:  Recipe object, dataframe of a recipe
12.01.16
"""


import random, os
import pandas as pd
from .FoodListBase import FoodListBase
from .FoodList import FoodList
from .config import LINE_BEGIN, BASE_FIELDS
from .tools import create_destination


class Recipe(FoodListBase):

    def __init__(self, dataframe=None):
        """Load dataframe into recipe."""
        self.dataframe = dataframe
        self.log_by_sum = pd.DataFrame()
        self.log_by_food = pd.DataFrame(columns=['food'])
        self.__name = self.write_name()


    @property
    def name(self):
        return self.__name
    
    
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
    
    
    def test_rules(self, diet, print_results=False):
        """Test whether a recipe fits all the dietary rules."""
        #print(LINE_BEGIN + "Testing the recipe follows rules...")
        
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
            
        if print_results:
        
            key_fields = BASE_FIELDS
            key_fields.extend([rule[0] for rule in diet.nutrient_rules  if rule[0] not in BASE_FIELDS])
            
            self.summarize(print_out=True, fields=key_fields)
            
            if not conditionals:
                for k, v in conditionals_dict.items():
                    print("{0}{1} : {2}".format(LINE_BEGIN, k, v))
            
            print(LINE_BEGIN + "Rules test found " + str(conditionals))
        
        return conditionals
        
        
    def test_foodlist(self, food_list, print_results=False):
        """Test whether a recipe fits all the dietary rules."""
        #print(LINE_BEGIN + "Testing the recipe compared to food list...")
        
        food_list_df_copy = food_list.dataframe.drop('serving', axis=1)
        food_list_copy = FoodList(pd.merge(food_list_df_copy, self.dataframe[['food','serving']], how='left', on='food'))
        food_list_copy.dataframe.loc[:, 'serving'] = food_list_copy.dataframe['serving'].fillna(0)
        food_list_copy.re_gram(n_serving=True)
        
        food_list_copy.dataframe = food_list_copy.dataframe[food_list_copy.dataframe['food'].isin(self.dataframe['food'].values)].sort_values('food').reset_index(drop=True).drop('gram_ratio', axis=1)
        self_dataframe_copy = self.dataframe.sort_values('food').reset_index(drop=True)[food_list_copy.dataframe.columns]
        
        test_df = food_list_copy.dataframe == self_dataframe_copy
        
        result_cols = test_df.all()
        result_final = test_df.values.all()
        
        if print_results:
        
            if not result_final:
                print(result_cols)
                
            print(LINE_BEGIN + "Food list test found " + str(result_final))
        
        return result_final
    
    
    def save(self, output_directory):
        """Save recipe and log of recipe to csv file."""
        dest, log_by_sum_dest, log_by_food_dest = create_destination(output_directory, self.name, 'csv')
        
        out_df = self.dataframe
        out_df.to_csv(dest, index=False)
        
        out_log_by_sum = self.log_by_sum
        out_log_by_sum.to_csv(log_by_sum_dest)
        
        out_log_by_food = self.log_by_food
        out_log_by_food.to_csv(log_by_food_dest, index=False)
    
    
    def write_name(self):
        return "recipe"
    
    
    def write_instructions(self):
        pass    
        
    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
