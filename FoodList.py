"""
kalamatchkas.FoodList
saba pilots
description:  FoodList object, dataframe of potential ingredients with nutritional information
12.01.16
"""


import random, os
import pandas as pd
from collections import defaultdict
from .FoodListBase import FoodListBase
from .config import LINE_BEGIN
from .Usda import Usda


class FoodList(FoodListBase):

    def __init__(self, path, api_key=None):
        """Load food file into dataframe."""
        assert os.path.exists(path), LINE_BEGIN + "ERROR: unable to find food file in " + path

        print(LINE_BEGIN + "Loading file... " + path)
        
        self.dataframe = pd.read_excel(path)
        
        if api_key:
            ndb_nos = self.get_ndbnos()
            
            usda = Usda(api_key)
            
            foods = [usda.food_report(ndb_no)  for ndb_no in ndb_nos]

            food_data = defaultdict(lambda: [])
            
            for food in foods:
                food.re_gram(5)
                food_data['food_id'].append(food.ndbno)
                food_data['food'].append(food.name)
                food_data['gram'].append(food.gram)
                food_data['protein'].append(food.protein)
                food_data['fat'].append(food.fat)
                food_data['carb'].append(food.carb)
                food_data['sugar'].append(food.sugar)
                
            self.dataframe = pd.DataFrame(food_data)
            #print(self.get_df())
        
        
    def get_ndbnos(self):
        """Gather and return a unique list of NDB_NOs from dataframe."""
        ndb_nos = list(self.get_df()["NBD_NO"].apply(str).apply(str.strip).unique())
        
        return [ndb_no for ndb_no in ndb_nos if ndb_no.isnumeric()]

    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
