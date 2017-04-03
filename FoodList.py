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
from .Usda import Usda
from .UsdaDicts import usda_nutrient_name_dict
from .Food import Food
from .config import LINE_BEGIN
from .tools import k_print


class FoodList(FoodListBase):

    def __init__(self, path, food_list_path=None, gram_amt=5, columns=None, api_key=None):
        """Load food file into dataframe."""
        assert type(path) in (pd.core.frame.DataFrame, pd.core.series.Series, str), LINE_BEGIN + "ERROR: please enter either a path or dataframe/series."
        
        if type(path) == str:
            assert os.path.exists(path), LINE_BEGIN + "ERROR: unable to find food file in " + path
        elif type(path) in (pd.core.frame.DataFrame, pd.core.series.Series):
            self.dataframe = path
            return

        if food_list_path and os.path.exists(food_list_path):
            k_print("Loading file... " + food_list_path + "\n")
            self.dataframe = pd.read_csv(food_list_path)
            return
        
        k_print("Loading file... " + path + "\n")
        
        self.dataframe = pd.read_excel(path)
        
        if columns and api_key:
            df_information = self.get_info(columns)
            
            usda = Usda(api_key)
            
            df_information.loc[:, 'food_report'] = df_information['ndb_nos'].apply(usda.food_report)
            df_information = df_information[df_information['food_report'].apply(lambda x: type(x) == Food)]

            food_data = defaultdict(lambda: [])
            
            for row in df_information.itertuples():
                food = getattr(row, 'food_report')
                
                if 'serving_size' in columns.keys():
                    serving_size = getattr(row, 'serving_size')
                    food.re_gram(serving_size)
                    food_data['serving_size'].append(serving_size)
                else:
                    food.re_gram(gram_amt)
                    
                food_data['food_id'].append(food.ndbno)
                
                if 'food_name' in columns.keys():
                    food_data['food'].append(getattr(row, 'food_name'))
                    food_data['usda_name'].append(food.name)
                else:
                    food_data['food'].append(food.name)
                
                if 'food_group' in columns.keys():
                    food_data['food_group'].append(getattr(row, 'food_group'))
                else:
                    food_data['food_group'].append(food.group)
                    
                if 'max_grams_meal' in columns.keys():
                    food_data['max_grams_meal'].append(getattr(row, 'max_grams_meal'))
                
                if 'max_grams_day' in columns.keys():
                    food_data['max_grams_day'].append(getattr(row, 'max_grams_day'))
                    
                food_data['gram'].append(food.gram)
                
                for key, val in usda_nutrient_name_dict.items():
                    food_data[key].append(food.nutrients[val]["value"])
                
            self.dataframe = pd.DataFrame(food_data)
            self.dataframe.loc[:, ('max_grams_meal','max_grams_day')] = self.dataframe[['max_grams_meal','max_grams_day']].fillna(-1)
            
            if food_list_path:
                self.save(food_list_path)
    
    
    def re_gram(self, gram_amt=None, gram_pct=None, serving_size=False, n_serving=False, verbose=False):
        assert bool(gram_amt) ^ bool(gram_pct) ^ serving_size ^ n_serving, LINE_BEGIN + "ERROR: input either gram amount or percent"
        
        if n_serving:
            assert 'serving' in self.dataframe.columns, LINE_BEGIN + "ERROR: this dataframe has no serving numbers specified"
            assert 'serving_size' in self.dataframe.columns, LINE_BEGIN + "ERROR: this dataframe has no serving sizes specified"
            if verbose:
                k_print("Changing food list to number of servings")
            self.dataframe.loc[:, 'gram_ratio'] = self.dataframe['serving_size'] * self.dataframe['serving'] / self.dataframe['gram']
            self.dataframe.loc[:, 'gram'] = self.dataframe['serving_size'] * self.dataframe['serving']
        elif serving_size:
            assert 'serving_size' in self.dataframe.columns, LINE_BEGIN + "ERROR: this dataframe has no serving sizes specified"
            if verbose:
                k_print("Changing food list to serving sizes")
            self.dataframe.loc[:, 'gram_ratio'] = self.dataframe['serving_size'] / self.dataframe['gram']
            self.dataframe.loc[:, 'gram'] = self.dataframe['serving_size']   
        elif gram_amt:
            if verbose:
                k_print("Changing food list to {0} grams".format(gram_amt))
            self.dataframe.loc[:, 'gram_ratio'] = gram_amt / self.dataframe['gram']
            self.dataframe.loc[:, 'gram'] = gram_amt
        elif gram_pct:
            if verbose:
                k_print("Changing food list to {0}% of current grams".format(gram_pct*100))
            self.dataframe.loc[:, 'gram_ratio'] = gram_pct #this line gives the pandas indexing warning...
            self.dataframe.loc[:, 'gram'] *= self.dataframe['gram_ratio']
        
        for key in usda_nutrient_name_dict.keys():
            self.dataframe.loc[:, key] *= self.dataframe['gram_ratio']
        
        self.complete()
    
    
    def calculate_maxday(self, diet):
        """Calculate daily maximum food amounts based on meal amounts and number of days."""
        food_list_selector = (self.dataframe['max_grams_meal'] != -1) & (self.dataframe['max_grams_day'] == -1)
        self.dataframe.loc[food_list_selector, 'max_grams_day'] = self.dataframe['max_grams_meal'] * len(diet.meals)
    
    
    def get_info(self, columns):
        """Gather and return a unique list of NDB_NOs from dataframe."""
        self.dataframe[columns['ndb_nos']] = self.dataframe[columns['ndb_nos']].apply(str).apply(str.strip)
        df_ndbnos_only = self.dataframe[self.dataframe[columns['ndb_nos']].apply(str.isnumeric)]
        
        col_reversed = {v:k for k,v in columns.items()}
        df_ndbnos_only.rename(columns=col_reversed, inplace=True)
        
        return df_ndbnos_only[list(columns.keys())]

    
def main():
    pass
    
    
if __name__ == "__main__":
    main()
