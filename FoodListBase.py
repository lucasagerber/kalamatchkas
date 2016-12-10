"""
kalamatchkas.FoodList
saba pilots
description:  FoodList object, dataframe of potential ingredients with nutritional information
12.01.16
"""


import random, os
import pandas as pd
from .config import LINE_BEGIN


class FoodListBase(object):

    def __init__(self, dataframe):
        """Load food file into dataframe."""
        self.dataframe = dataframe
        
        
    def get_df(self):
        """Returns dataframe for food list."""
        return self.dataframe

        
    def select_food(self, number):
        """Select a food from the food list."""
        # currently only works for 1 selection. . .
        assert not self.get_df().empty, LINE_BEGIN + "ERROR: food dataframe is empty"
        
        rand_index = random.choice(list(self.get_df().index.values)) #random.sample(list(self.get_df().index.values), number) would need to modify for multiple...
        food_df = self.get_df().ix[rand_index]
        
        return food_df


    def add_food(self, food_df):
        """Add chosen food to the food list."""
        assert not food_df.empty, LINE_BEGIN + "ERROR: no food to add"
        
        if food_df["food"] in self.get_df()["food"].values:
            updated_df = self.get_df()
            fields_update = ['gram', 'protein', 'fat', 'carb', 'sugar']
            updated_df.loc[updated_df["food"]==food_df["food"], fields_update] += food_df[fields_update]
        else:
            updated_df = self.get_df().append(food_df).reset_index(drop=True)
        
        self.dataframe = updated_df
        
        self.calculate_calories()
        
        #print(LINE_BEGIN + "Added food:  ", food_df["food"])
        
        
    def del_food(self, food_df):
        """Delete chosen food from the food list."""
        assert not food_df.empty, LINE_BEGIN + "ERROR: no food to delete"
        assert food_df["food"] in self.get_df()["food"].values, LINE_BEGIN + "ERROR: food to delete is not in recipe"
        
        updated_df = self.get_df()
        fields_update = ['gram', 'protein', 'fat', 'carb', 'sugar']
        updated_df.loc[updated_df["food"]==food_df["food"], fields_update] -= food_df[fields_update]
        
        updated_df = updated_df[updated_df["gram"] > 0].reset_index(drop=True)
        
        self.dataframe = updated_df
        
        self.calculate_calories()
            
        #print(LINE_BEGIN + "Deleted food:  ", food_df["food"])

        
    def calculate_calories(self):
        """Calculate calories of each food in the food list."""  
        self.dataframe["protein_cal"] = self.dataframe["protein"] * 4
        self.dataframe["carb_cal"] = (self.dataframe["carb"] + self.dataframe["sugar"]) * 4
        self.dataframe["fat_cal"] = self.dataframe["fat"] * 9
        self.dataframe["total_cal"] = self.dataframe["protein_cal"] + self.dataframe["carb_cal"] + self.dataframe["fat_cal"]

        
    def calculate_calorie_percents(self):
        """Calculate calories percents of each food in the food list.""" 
        for col in ["protein_cal","carb_cal","fat_cal"]:
            new_col = col + '_%'
            self.dataframe[new_col] = self.dataframe[col] / self.dataframe["total_cal"]

        
    def save(self, output_file):
        """Save food list to csv file."""
        out_df = self.get_df()
        out_df.to_csv(output_file)

    
def main():
    pass
    
    
if __name__ == "__main__":
    main()