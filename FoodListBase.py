"""
kalamatchkas.FoodListBase
saba pilots
description:  FoodListBase object, dataframe of ingredients with nutritional information
12.01.16
"""


import random
import pandas as pd
from .config import LINE_BEGIN, FIELDS_DONT_UPDATE
from .tools import order_columns


class FoodListBase(object):

    def __init__(self, dataframe):
        """Load food file into dataframe."""
        self.__dataframe = dataframe
        
        
    @property
    def dataframe(self):
        return self.__dataframe
    
    
    @dataframe.setter
    def dataframe(self, value):
        assert (type(value) in (pd.core.frame.DataFrame, pd.core.series.Series) or not value), LINE_BEGIN + "ERROR: non dataframe/series/none assigned to dataframe property"
        if type(value) in (pd.core.frame.DataFrame, pd.core.series.Series):
            self.__dataframe = value
        else:
            self.__dataframe = pd.DataFrame()

        
    def select_food(self, conditional_dict={}, conditional=None, priority_dict={}):
        """Select a food from the food list."""
        assert not self.dataframe.empty, LINE_BEGIN + "ERROR: food dataframe is empty"
                
        select_dataframe = self.dataframe
        
        # select on any conditionals
        if type(conditional) == pd.core.series.Series:
            select_dataframe = select_dataframe[conditional]

        # select on any conditional dict
        if conditional_dict:
            conditionals = bool(True)
            for k, v in conditional_dict.items():
                conditionals &= (select_dataframe[k] == v)
            
            select_dataframe = select_dataframe[conditionals]

        # prioritize from priority dict
        if priority_dict:
            priority = bool(True)
            for k, v in priority_dict.items():
                priority &= (select_dataframe[k].isin(v))
            
            priority_dataframe = select_dataframe[priority]
            
            if not priority_dataframe.empty:
                select_dataframe = priority_dataframe
        
        rand_index = random.choice(select_dataframe.index.values.tolist())
        food_df = self.dataframe.ix[rand_index]
        
        return food_df


    def add_food(self, food_df):
        """Add chosen food to the food list."""
        assert not food_df.empty, LINE_BEGIN + "ERROR: no food to add"
        
        if not self.dataframe.empty and food_df["food"] in self.dataframe["food"].values:
            updated_df = self.dataframe
            fields_to_update = [field for field in updated_df.columns if updated_df[field].dtype == 'float64' and field not in FIELDS_DONT_UPDATE]
            updated_df.loc[updated_df["food"]==food_df["food"], fields_to_update] += food_df[fields_to_update]
        else:
            updated_df = self.dataframe.append(food_df).reset_index(drop=True)
        
        self.dataframe = updated_df.sort_values('food').reset_index(drop=True)
        
        self.complete()
        
        
    def del_food(self, food_df):
        """Delete chosen food from the food list."""
        assert not food_df.empty, LINE_BEGIN + "ERROR: no food to delete"
        assert food_df["food"] in self.dataframe["food"].values, LINE_BEGIN + "ERROR: food to delete is not in recipe"
        
        updated_df = self.dataframe
        fields_to_update = [field for field in updated_df.columns if updated_df[field].dtype == 'float64' and field not in FIELDS_DONT_UPDATE]
        updated_df.loc[updated_df["food"]==food_df["food"], fields_to_update] -= food_df[fields_to_update]
        
        updated_df = updated_df[updated_df["gram"] > 0]
        
        self.dataframe = updated_df.sort_values('food').reset_index(drop=True)
        
        self.complete()

        
    def calculate_calories(self):
        """Calculate calories of each food in the food list."""
        self.dataframe.loc[:, "protein_cal"] = self.dataframe["protein"] * 4
        self.dataframe.loc[:, "carb_cal"] = (self.dataframe["carb"] + self.dataframe["sugar"]) * 4
        self.dataframe.loc[:, "sugar_cal"] = self.dataframe["sugar"] * 4
        self.dataframe.loc[:, "fat_cal"] = self.dataframe["fat"] * 9
        self.dataframe.loc[:, "fat_saturated_cal"] = self.dataframe["fat_saturated"] * 9
        self.dataframe.loc[:, "total_cal"] = self.dataframe["protein_cal"] + self.dataframe["carb_cal"] + self.dataframe["fat_cal"]


    def calculate_calorie_percents(self):
        """Calculate calories percents of each food in the food list."""
        for col in ["protein_cal","carb_cal","fat_cal","sugar_cal","fat_saturated_cal"]:
            new_col = col + '_%'
            self.dataframe[new_col] = self.dataframe[col] / self.dataframe["total_cal"]
            
    
    def calculate_servings(self):
        """Calculate number of servings of each food in the food list."""
        self.dataframe.loc[:, 'serving'] = self.dataframe['gram'] / self.dataframe['serving_size']

        
    def calculate_provitamin_a(self):
        """Calculate number of servings of each food in the food list."""
        self.dataframe.loc[:, 'provitamin_a'] = (self.dataframe['carotene_beta'] / 12) + (self.dataframe['carotene_alpha'] / 24) + (self.dataframe['cryptoxanthin_beta'] / 24)
    
    
    def complete(self):
        """Calculate calories, servings, and provitamin A."""
        self.calculate_calories()
        self.calculate_servings()
        self.calculate_provitamin_a()
    
    
    def save(self, output_file):
        """Save food list to csv file."""
        columns = order_columns(self.dataframe.columns.tolist())
        out_df = self.dataframe[columns]
        out_df.to_csv(output_file, index=False)

    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
