"""
kalamatchkas.config
saba pilots
description:  configuration file for kalamatchas program
"""


# file of foods to load
FOOD_PATH = "C:/Users/Lucas/Documents/GitHub/kalamatchkas/sample/ingredient_doron v5.xlsx"

# file to output recipes
OUT_PATH = "C:/Users/Lucas/Documents/GitHub/kalamatchkas/sample/test_out.csv"

# string used to begin each printed line
LINE_BEGIN = ">*~@~*> "

# columns in recipe and ingredient file
RECIPE_COLUMNS = ['food_id', 'food', 'gram', 'protein', 'fat', 'carb', 'sugar']

# api key for searching usda database
API_KEY = "Gb3vhyvcHwFhZNtbD2fqWc3oeNdwYA22qqND1fyU"

# base url for searching usda database
BASE_URL = "http://api.nal.usda.gov/ndb/"