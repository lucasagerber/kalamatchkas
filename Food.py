"""
kalamatchkas.Food
saba pilots
description:  Food object, nutritional information on a food
12.11.16
"""


from collections import defaultdict
from .UsdaDicts import usda_nutrient_name_dict


class Food(object):

    def __init__(self, query_result):
        self.__ndbno = query_result["ndbno"]
        self.__name = query_result["name"]
        
        if "fg" in query_result.keys():
            self.__group = query_result["fg"]
        else:
            self.__group = ""
            
        self.__gram = 100
        
        self.__nutrients = defaultdict(lambda: dict({'value':0}))
        for nutrient in query_result["nutrients"]:
            nutrient["value"] = float(nutrient["value"])
            self.__nutrients[int(nutrient.pop("nutrient_id"))] = nutrient
                
        print(self)


    @property
    def ndbno(self):
        return self.__ndbno


    @property
    def name(self):
        return self.__name


    @property
    def group(self):
        return self.__group
    
    
    @property
    def gram(self):
        return self.__gram


    @property
    def nutrients(self):
        return self.__nutrients


    @property
    def folate(self):
        return self.__nutrients[usda_nutrient_name_dict["folate"]]["value"]


    @property
    def histidine(self):
        return self.__nutrients[usda_nutrient_name_dict["histidine"]]["value"]


    @property
    def campesterol(self):
        return self.__nutrients[usda_nutrient_name_dict["campesterol"]]["value"]


    @property
    def riboflavin(self):
        return self.__nutrients[usda_nutrient_name_dict["riboflavin"]]["value"]


    @property
    def theobromine(self):
        return self.__nutrients[usda_nutrient_name_dict["theobromine"]]["value"]


    @property
    def fat_20_1(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_1"]]["value"]


    @property
    def dihydrophylloquinone(self):
        return self.__nutrients[usda_nutrient_name_dict["dihydrophylloquinone"]]["value"]


    @property
    def fat_18_4(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_4"]]["value"]


    @property
    def methionine(self):
        return self.__nutrients[usda_nutrient_name_dict["methionine"]]["value"]


    @property
    def sodium(self):
        return self.__nutrients[usda_nutrient_name_dict["sodium"]]["value"]


    @property
    def vitamin_c(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_c"]]["value"]


    @property
    def fat_18_2_i(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_i"]]["value"]


    @property
    def arginine(self):
        return self.__nutrients[usda_nutrient_name_dict["arginine"]]["value"]


    @property
    def vitamin_d(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_d"]]["value"]


    @property
    def fat_20_3_n_3(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_3_n_3"]]["value"]


    @property
    def betaine(self):
        return self.__nutrients[usda_nutrient_name_dict["betaine"]]["value"]


    @property
    def fluoride(self):
        return self.__nutrients[usda_nutrient_name_dict["fluoride"]]["value"]


    @property
    def fat_15_1(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_15_1"]]["value"]


    @property
    def thiamin(self):
        return self.__nutrients[usda_nutrient_name_dict["thiamin"]]["value"]


    @property
    def fat_monounsaturated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_monounsaturated"]]["value"]


    @property
    def vitamin_e_alpha_tocopherol(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_e_alpha_tocopherol"]]["value"]


    @property
    def ash(self):
        return self.__nutrients[usda_nutrient_name_dict["ash"]]["value"]


    @property
    def cryptoxanthin_beta(self):
        return self.__nutrients[usda_nutrient_name_dict["cryptoxanthin_beta"]]["value"]


    @property
    def proline(self):
        return self.__nutrients[usda_nutrient_name_dict["proline"]]["value"]


    @property
    def folate_dfe(self):
        return self.__nutrients[usda_nutrient_name_dict["folate_dfe"]]["value"]


    @property
    def fat_6_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_6_0"]]["value"]


    @property
    def fat(self):
        return self.__nutrients[usda_nutrient_name_dict["fat"]]["value"]


    @property
    def fat_22_5_n_3(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_5_n_3"]]["value"]


    @property
    def tocotrienol_beta(self):
        return self.__nutrients[usda_nutrient_name_dict["tocotrienol_beta"]]["value"]


    @property
    def fat_20_3_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_3_undifferentiated"]]["value"]


    @property
    def fat_22_1_t(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_1_t"]]["value"]


    @property
    def selenium(self):
        return self.__nutrients[usda_nutrient_name_dict["selenium"]]["value"]


    @property
    def starch(self):
        return self.__nutrients[usda_nutrient_name_dict["starch"]]["value"]


    @property
    def menaquinone_4(self):
        return self.__nutrients[usda_nutrient_name_dict["menaquinone_4"]]["value"]


    @property
    def folic_acid(self):
        return self.__nutrients[usda_nutrient_name_dict["folic_acid"]]["value"]


    @property
    def fat_18_2_t_not_further_defined(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_t_not_further_defined"]]["value"]


    @property
    def tocopherol_beta(self):
        return self.__nutrients[usda_nutrient_name_dict["tocopherol_beta"]]["value"]


    @property
    def sugar(self):
        return self.__nutrients[usda_nutrient_name_dict["sugar"]]["value"]


    @property
    def fat_16_1_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_16_1_c"]]["value"]


    @property
    def fat_18_2_n_6_c_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_n_6_c_c"]]["value"]


    @property
    def fat_20_2_n_6_c_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_2_n_6_c_c"]]["value"]


    @property
    def lactose(self):
        return self.__nutrients[usda_nutrient_name_dict["lactose"]]["value"]


    @property
    def vitamin_e_added(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_e_added"]]["value"]


    @property
    def fat_12_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_12_0"]]["value"]


    @property
    def iron(self):
        return self.__nutrients[usda_nutrient_name_dict["iron"]]["value"]


    @property
    def fat_18_3_i(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_3_i"]]["value"]


    @property
    def zinc(self):
        return self.__nutrients[usda_nutrient_name_dict["zinc"]]["value"]


    @property
    def fat_18_3_n_6_c_c_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_3_n_6_c_c_c"]]["value"]


    @property
    def galactose(self):
        return self.__nutrients[usda_nutrient_name_dict["galactose"]]["value"]


    @property
    def aspartic_acid(self):
        return self.__nutrients[usda_nutrient_name_dict["aspartic_acid"]]["value"]


    @property
    def fat_8_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_8_0"]]["value"]


    @property
    def phenylalanine(self):
        return self.__nutrients[usda_nutrient_name_dict["phenylalanine"]]["value"]


    @property
    def maltose(self):
        return self.__nutrients[usda_nutrient_name_dict["maltose"]]["value"]


    @property
    def cystine(self):
        return self.__nutrients[usda_nutrient_name_dict["cystine"]]["value"]


    @property
    def lysine(self):
        return self.__nutrients[usda_nutrient_name_dict["lysine"]]["value"]


    @property
    def fat_22_6_n_3(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_6_n_3"]]["value"]


    @property
    def lutein_zeaxanthin(self):
        return self.__nutrients[usda_nutrient_name_dict["lutein_zeaxanthin"]]["value"]


    @property
    def valine(self):
        return self.__nutrients[usda_nutrient_name_dict["valine"]]["value"]


    @property
    def vitamin_b12_added(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_b12_added"]]["value"]


    @property
    def threonine(self):
        return self.__nutrients[usda_nutrient_name_dict["threonine"]]["value"]


    @property
    def tocotrienol_gamma(self):
        return self.__nutrients[usda_nutrient_name_dict["tocotrienol_gamma"]]["value"]


    @property
    def fat_24_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_24_0"]]["value"]


    @property
    def folate_food(self):
        return self.__nutrients[usda_nutrient_name_dict["folate_food"]]["value"]


    @property
    def fat_saturated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_saturated"]]["value"]


    @property
    def fat_16_1_t(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_16_1_t"]]["value"]


    @property
    def fat_14_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_14_0"]]["value"]


    @property
    def alanine(self):
        return self.__nutrients[usda_nutrient_name_dict["alanine"]]["value"]


    @property
    def fructose(self):
        return self.__nutrients[usda_nutrient_name_dict["fructose"]]["value"]


    @property
    def tocopherol_delta(self):
        return self.__nutrients[usda_nutrient_name_dict["tocopherol_delta"]]["value"]


    @property
    def alcohol_ethyl(self):
        return self.__nutrients[usda_nutrient_name_dict["alcohol_ethyl"]]["value"]


    @property
    def fat_24_1_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_24_1_c"]]["value"]


    @property
    def fat_22_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_0"]]["value"]


    @property
    def fat_trans(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_trans"]]["value"]


    @property
    def fat_10_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_10_0"]]["value"]


    @property
    def fat_16_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_16_0"]]["value"]


    @property
    def fat_18_3_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_3_undifferentiated"]]["value"]


    @property
    def fat_18_1_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_1_c"]]["value"]


    @property
    def glutamic_acid(self):
        return self.__nutrients[usda_nutrient_name_dict["glutamic_acid"]]["value"]


    @property
    def magnesium(self):
        return self.__nutrients[usda_nutrient_name_dict["magnesium"]]["value"]


    @property
    def choline(self):
        return self.__nutrients[usda_nutrient_name_dict["choline"]]["value"]


    @property
    def fat_20_3_n_6(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_3_n_6"]]["value"]


    @property
    def vitamin_a_rae(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_a_rae"]]["value"]


    @property
    def vitamin_d2(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_d2"]]["value"]


    @property
    def fat_18_2_t_t(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_t_t"]]["value"]


    @property
    def protein(self):
        return self.__nutrients[usda_nutrient_name_dict["protein"]]["value"]


    @property
    def manganese(self):
        return self.__nutrients[usda_nutrient_name_dict["manganese"]]["value"]


    @property
    def fat_13_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_13_0"]]["value"]


    @property
    def sucrose(self):
        return self.__nutrients[usda_nutrient_name_dict["sucrose"]]["value"]


    @property
    def fat_17_1(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_17_1"]]["value"]


    @property
    def tryptophan(self):
        return self.__nutrients[usda_nutrient_name_dict["tryptophan"]]["value"]


    @property
    def carb(self):
        return self.__nutrients[usda_nutrient_name_dict["carb"]]["value"]


    @property
    def fat_18_3_n_3_c_c_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_3_n_3_c_c_c"]]["value"]


    @property
    def fat_trans_polyenoic(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_trans_polyenoic"]]["value"]


    @property
    def fat_18_2_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_undifferentiated"]]["value"]


    @property
    def fat_16_1_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_16_1_undifferentiated"]]["value"]


    @property
    def glucose(self):
        return self.__nutrients[usda_nutrient_name_dict["glucose"]]["value"]


    @property
    def fat_17_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_17_0"]]["value"]


    @property
    def fiber(self):
        return self.__nutrients[usda_nutrient_name_dict["fiber"]]["value"]


    @property
    def phosphorus(self):
        return self.__nutrients[usda_nutrient_name_dict["phosphorus"]]["value"]


    @property
    def serine(self):
        return self.__nutrients[usda_nutrient_name_dict["serine"]]["value"]


    @property
    def tyrosine(self):
        return self.__nutrients[usda_nutrient_name_dict["tyrosine"]]["value"]


    @property
    def beta_sitosterol(self):
        return self.__nutrients[usda_nutrient_name_dict["beta_sitosterol"]]["value"]


    @property
    def vitamin_a_iu(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_a_iu"]]["value"]


    @property
    def niacin(self):
        return self.__nutrients[usda_nutrient_name_dict["niacin"]]["value"]


    @property
    def pantothenic_acid(self):
        return self.__nutrients[usda_nutrient_name_dict["pantothenic_acid"]]["value"]


    @property
    def fat_21_5(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_21_5"]]["value"]


    @property
    def water(self):
        return self.__nutrients[usda_nutrient_name_dict["water"]]["value"]


    @property
    def leucine(self):
        return self.__nutrients[usda_nutrient_name_dict["leucine"]]["value"]


    @property
    def tocopherol_gamma(self):
        return self.__nutrients[usda_nutrient_name_dict["tocopherol_gamma"]]["value"]


    @property
    def fat_polyunsaturated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_polyunsaturated"]]["value"]


    @property
    def fat_18_2_CLAs(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_2_CLAs"]]["value"]


    @property
    def fat_4_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_4_0"]]["value"]


    @property
    def fat_14_1(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_14_1"]]["value"]


    @property
    def fat_trans_monoenoic(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_trans_monoenoic"]]["value"]


    @property
    def tocotrienol_alpha(self):
        return self.__nutrients[usda_nutrient_name_dict["tocotrienol_alpha"]]["value"]


    @property
    def tocotrienol_delta(self):
        return self.__nutrients[usda_nutrient_name_dict["tocotrienol_delta"]]["value"]


    @property
    def glycine(self):
        return self.__nutrients[usda_nutrient_name_dict["glycine"]]["value"]


    @property
    def fat_20_5_n_3(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_5_n_3"]]["value"]


    @property
    def fat_18_1_11_t(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_1_11_t"]]["value"]


    @property
    def energy_2(self):
        return self.__nutrients[usda_nutrient_name_dict["energy_2"]]["value"]


    @property
    def stigmasterol(self):
        return self.__nutrients[usda_nutrient_name_dict["stigmasterol"]]["value"]


    @property
    def energy(self):
        return self.__nutrients[usda_nutrient_name_dict["energy"]]["value"]


    @property
    def carotene_beta(self):
        return self.__nutrients[usda_nutrient_name_dict["carotene_beta"]]["value"]


    @property
    def hydroxyproline(self):
        return self.__nutrients[usda_nutrient_name_dict["hydroxyproline"]]["value"]


    @property
    def fat_22_1_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_1_undifferentiated"]]["value"]


    @property
    def copper(self):
        return self.__nutrients[usda_nutrient_name_dict["copper"]]["value"]


    @property
    def fat_18_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_0"]]["value"]


    @property
    def fat_18_1_t(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_1_t"]]["value"]


    @property
    def caffeine(self):
        return self.__nutrients[usda_nutrient_name_dict["caffeine"]]["value"]


    @property
    def vitamin_d_d2andd3(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_d_d2andd3"]]["value"]


    @property
    def fat_22_1_c(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_1_c"]]["value"]


    @property
    def vitamin_b12(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_b12"]]["value"]


    @property
    def retinol(self):
        return self.__nutrients[usda_nutrient_name_dict["retinol"]]["value"]


    @property
    def vitamin_d3(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_d3"]]["value"]


    @property
    def cholesterol(self):
        return self.__nutrients[usda_nutrient_name_dict["cholesterol"]]["value"]


    @property
    def calcium(self):
        return self.__nutrients[usda_nutrient_name_dict["calcium"]]["value"]


    @property
    def phytosterols(self):
        return self.__nutrients[usda_nutrient_name_dict["phytosterols"]]["value"]


    @property
    def fat_18_1_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_18_1_undifferentiated"]]["value"]


    @property
    def isoleucine(self):
        return self.__nutrients[usda_nutrient_name_dict["isoleucine"]]["value"]


    @property
    def fat_20_4_undifferentiated(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_4_undifferentiated"]]["value"]


    @property
    def lycopene(self):
        return self.__nutrients[usda_nutrient_name_dict["lycopene"]]["value"]


    @property
    def potassium(self):
        return self.__nutrients[usda_nutrient_name_dict["potassium"]]["value"]


    @property
    def fat_20_4_n_6(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_4_n_6"]]["value"]


    @property
    def adjusted_protein(self):
        return self.__nutrients[usda_nutrient_name_dict["adjusted_protein"]]["value"]


    @property
    def fat_15_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_15_0"]]["value"]


    @property
    def fat_22_4(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_22_4"]]["value"]


    @property
    def fat_20_0(self):
        return self.__nutrients[usda_nutrient_name_dict["fat_20_0"]]["value"]


    @property
    def carotene_alpha(self):
        return self.__nutrients[usda_nutrient_name_dict["carotene_alpha"]]["value"]


    @property
    def vitamin_k(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_k"]]["value"]


    @property
    def vitamin_b6(self):
        return self.__nutrients[usda_nutrient_name_dict["vitamin_b6"]]["value"]

         
    def re_gram(self, gram_amt):
        gram_ratio = gram_amt / self.__gram
        self.__gram = gram_amt
        
        for nutrient in self.__nutrients.keys():
            self.__nutrients[nutrient]["value"] *= gram_ratio       


    def __str__(self):
        return self.ndbno + ":  " + self.name
    
    
def main():
    pass
    
    
if __name__ == "__main__":
    main()