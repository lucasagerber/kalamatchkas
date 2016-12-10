
Kalamatchkas
========

Kalamatchkas creates kalamatchkas of food.

Example
--------

In this example I create a diet and make a kalamatchkas based on an ingredient list: ::

    import kalamatchkas

    # Input your dietary parameters
    
    my_meals = [('breakfast',400),('lunch',700),('dinner',700)]
    my_rules = [('protein_cal_%',.15,.30), ('fat_cal_%',.15,.25), ('carb_cal_%',.45,.60)]
    my_diet = kalamatchkas.Diet("My Diet", meals=my_meals, macronutrient_rules=my_rules)

    # Create your list of ingredients
    # You'll need a USDA API KEY (get one here:
    # https://ndb.nal.usda.gov/ndb/doc/index#, see "Gaining Access" and click sign up now)

    path = #location of sample ingredients file, ingredient_doron v4.xlsx
    ingredients = kalamatchkas.FoodList(path, API_KEY)

    # Put these in a kalamatchkas object ... and generate a day of kalamatchkas
    
    K = kalamatchkas.Kalamatchkas(ingredients, my_diet)
    K.day()

    # Summarize the nutrient content of the kalamatchkas
    
    K.recipe.summarize(print_out=True, day=False)

    # Save the kalamatchkas out to a csv file
    
    K.recipe.save('C:/Documents/wherever/my_kalamatchkas.csv')
