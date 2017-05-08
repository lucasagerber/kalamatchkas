"""
kalamatchkas.Diet
saba pilots
description:  Diet object, information on person's diet
12.10.16
"""


from collections import OrderedDict
from .config import LINE_BEGIN


class Diet(object):

    def __init__(self,
            diet_name,
            meals=[('breakfast',400),('lunch',700),('dinner',700)],
            calorie_error=.05,
            nutrient_rules=[
                    ('protein_cal_%',.15,.30),
                    ('fat_cal_%',0,.25),
                    ('carb_cal_%',.45,.60),
                    ('sugar_cal_%',0,.10),
                    ('fat_saturated_cal_%',0,.06),
                    ('fiber',0,15),
                    ('folate',400,1000),
                    ('sodium',0,1137),
                    ('vitamin_b12',3.75,1000000),
                    ('riboflavin',1.3,400),
                    ('phosphorus',700,4000),
                    ('calcium',300,500),
                    ('retinol',0,3000),
                    ('provitamin_a',900,1000000),
            ],
            foodgroup_rules=[
                    ('vegetables',7,9),
                    ('grains',4,8),
                    ('proteins',1,6),
                    ('fats',3,6),
                    ('acids',1,3),
                    ('condiments',1,9),
            ]
        ):
        """Creates a diet object."""
        self.__name = diet_name
        self.__meals = OrderedDict(meals)
        self.__calorie_error = calorie_error
        self.__nutrient_rules = nutrient_rules
        self.__foodgroup_rules = foodgroup_rules
        
        print(self)


    @property
    def name(self):
        return self.__name
    
    
    @property
    def meals(self):
        return self.__meals
    
    
    @property
    def calories(self):
        return sum(self.__meals.values())
    
    
    @property
    def calorie_error(self):
        return self.__calorie_error
    
    
    @property
    def calorie_range(self):
        return [ ('total_cal', self.calories*(1-self.calorie_error), self.calories*(1+self.calorie_error)) ]
    
    
    @property
    def nutrient_rules(self):
        return self.__nutrient_rules
        
        
    @property
    def foodgroup_rules(self):
        return self.__foodgroup_rules
    
    
    def __str__(self):
        print_string = "\n" + LINE_BEGIN + self.name + ":\n" + LINE_BEGIN + str(len(self.meals.keys())) + " meals:\n"
        for meal, cals in self.meals.items():
            print_string += LINE_BEGIN + "    " + meal.title() + ", " + str(cals) + " calories\n"
            
        print_string += LINE_BEGIN + "With the following dietary rules:\n"
        for name, min_val, max_val in self.nutrient_rules:
            name = name.replace('_cal_%', '')
            if max_val < 1:
                intro_string = "    Percent of calories from "
                min_val = str(min_val*100) + '%'
                max_val = str(max_val*100) + '%'
            else:
                intro_string = "    Grams of "
                min_val = str(min_val)
                max_val = str(max_val)
            print_string += "{}{}{}, {} to {}\n".format(LINE_BEGIN, intro_string, name.title(), min_val, max_val)

        for name, min_val, max_val in self.foodgroup_rules:
            intro_string = "    Servings of "
            min_val = str(min_val)
            max_val = str(max_val)
            print_string += "{}{}{}, {} to {}\n".format(LINE_BEGIN, intro_string, name.title(), min_val, max_val)
            
        return print_string
        

def main():
    pass
    
    
if __name__ == "__main__":
    main()            
        