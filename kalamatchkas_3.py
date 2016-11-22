"""
kalamatchkas
10.02.16
The Saba Pilots
"""


import random, os, sys
from collections import OrderedDict
import pandas as pd


RECIPE_COLUMNS = ['food', 'food_group', 'volume', 'gram', 'protein', 'fat', 'carb', 'sugar']


def load_food(path):
    """Load food file into dataframe."""
    assert os.path.exists(path), LINE_BEGIN + "ERROR: unable to find food file in " + path

    print(LINE_BEGIN + "Loading file... " + path)
    food_df = pd.read_excel(path)
    
    return food_df


def select_food(current_df, food_df):
    """Select a food based on dietary rules."""    
    rand_index = random.choice([item for item in food_df.index.values])

    df_chosen = food_df.loc[rand_index, :]
    #print(LINE_BEGIN + "Added food:  ", df_chosen["food"])

    return df_chosen


def add_food(current_df, df_chosen):
    """Add chosen food to current recipe."""
    assert not df_chosen.empty, LINE_BEGIN + "ERROR: no food to add"
    
    updated_df = current_df.append(df_chosen)
    updated_df = calculate_calories(updated_df)
    return updated_df


def create_recipe(meal, food_df, calories, macronutrient_rules):
    """Create a random recipe based on dietary rules and calorie requirements."""
    print(df_list)
    
    macronutrient_rules = [ (rule[0], rule[1]*calories, rule[2]*calories) for rule in macronutrient_rules ]
    
    recipe_df = pd.DataFrame(columns=RECIPE_COLUMNS)
    
    while recipe_df.empty or recipe_df["total_cal"].sum() < calories:
        new_food_df = select_food(recipe_df, food_df, macronutrient_rules)
        recipe_df = add_food(recipe_df, new_food_df)
        
    recipe_df = balance_recipe(recipe_df, food_df, )

    final_recipe_df = compile_recipe(recipe_df)

    print(LINE_BEGIN + meal.title() + " recipe compiled...")
    
    return final_recipe_df


def create_day(
        food_df,
        meals=[('breakfast',400),('lunch',700),('dinner',700)],
        macronutrient_rules=[('protein',.15,.30), ('fat',.15,.25), ('carb',.45,.60)]
    ):
    """Create a day of random recipes based on dietary rules and calorie requirements."""
    meals = OrderedDict(meals)
    df_list = list()
    
    for meal, calories in meals.items():
        df_list.append(create_recipe(meal, food_df, df_list, calories, macronutrient_rules))
        
    day_df = pd.concat(df_list, keys=meals.keys())
    
    print(LINE_BEGIN + "Day of meals compiled!")
    
    return day_df


def compile_recipe(recipe_df):
    """Compile raw list of ingredients into recipe."""
    final_df = recipe_df.groupby("food").sum()
    final_df['food_group'] = recipe_df.groupby("food")['food_group'].first()
    return final_df

    
def calculate_calories(dataframe):
    """Calculate calories of each food in dataframe."""   
    dataframe["protein_cal"] = dataframe["protein"] * 4
    dataframe["carb_cal"] = (dataframe["carb"] + dataframe["sugar"]) * 4
    dataframe["fat_cal"] = dataframe["fat"] * 9
    dataframe["total_cal"] = dataframe["protein_cal"] + dataframe["carb_cal"] + dataframe["fat_cal"]
    
    return dataframe
    

def test_day(dataframe):
    """Test the results of a day of recipes."""
    test_df = dataframe.reset_index().groupby(["level_0"])["protein_cal","carb_cal","fat_cal","total_cal"].sum()
    
    for col in ["protein_cal","carb_cal","fat_cal"]:
        test_df[col] = test_df[col] / test_df["total_cal"]
    
    print(test_df)

    
def main():
    foods = load_food(FOOD_PATH)
    day = create_day(foods)
    test_day(day)

    
if __name__ == "__main__":
    main()
