"""
kalamatchkas.Recipe
saba pilots
description:  Recipe object, dataframe of a recipe
12.01.16
"""


import random, os
import pandas as pd
from .FoodListBase import FoodListBase
from .config import LINE_BEGIN, RECIPE_COLUMNS


class Recipe(FoodListBase):

    def __init__(self, dataframe=None):
        """Load dataframe into recipe."""
        assert (type(dataframe) in (pd.core.frame.DataFrame, pd.core.series.Series) or not dataframe), LINE_BEGIN + "ERROR: non dataframe/none entered to recipe"
        if type(dataframe) in (pd.core.frame.DataFrame, pd.core.series.Series):
            self.dataframe = dataframe
        else:
            self.dataframe = pd.DataFrame(columns=RECIPE_COLUMNS)


    def summarize(self, print_out=False, day=False):
        """Summarize and return the macronutrient levels of a recipe, option to print as well."""
        if day:
            summary_df = self.get_df().reset_index().groupby(["level_0"]).sum()
        else:
            summary_df = self.get_df().sum()
        
        summary_recipe = Recipe(summary_df)
        summary_recipe.calculate_calorie_percents()
        
        if print_out:
            print(summary_recipe.get_df()[["protein_cal_%","carb_cal_%","fat_cal_%","total_cal"]])
        
        return summary_recipe.get_df(), summary_recipe.get_df()["total_cal"]

        
    def write_instructions(self):
        pass


    def test(self, diet):
        """Test whether a recipe fits all the dietary rules."""
        #print(LINE_BEGIN + "Testing the recipe...")
        
        recipe_sum, calories = self.summarize()
        
        conditionals = bool(True)

        rules = list()
        rules.extend(diet.macronutrient_rules)
        rules.extend(diet.calorie_range)    
            
        for rule in rules:
            conditionals &= (rule[1] <= recipe_sum[rule[0]] <= rule[2])
        
        #print(LINE_BEGIN + "Recipe test found " + str(conditionals))
        #summarize_recipe(self.get_df(), print_out=True)
        return conditionals
        
        
    def save(self, output_file):
        """Save food list to csv file."""
        out_df = self.get_df()[['food_id', 'food', 'gram']]
        out_df.to_csv(output_file)

    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
