from enum import Enum

class Borough(Enum):
    BROOKLYN = 'Brooklyn'
    MANHATTAN = 'Manhattan'
    QUEENS = 'Queens'
    STATEN_ISLAND = 'Staten Island'
    THE_BRONX = 'The Bronx'

    @classmethod
    def getBoroughs(cls):
        return [(borough.value, borough.value) for borough in cls]

class Cuisine(Enum):
    AFRICAN = 'African'
    AMERICAN = 'American'
    ARAB = 'Arab'
    AUSTRALIAN = 'Australian'
    BRAZILIAN = 'Brazilian'
    CANADIAN = 'Canadian'
    CARIBBEAN = 'Caribbean'
    CHINESE = 'Chinese'
    COLOMBIAN = 'Colombian'
    CUBAN = 'Cuban'
    DOMINICAN = 'Dominican'
    ECUADORIAN = 'Ecuadorian'
    EGYPTIAN = 'Egyptian'
    FILIPINO = 'Filipino'
    FRENCH = 'French'
    GERMAN = 'German'
    GREEK = 'Greek'
    INDIAN = 'Indian'
    INDONESIAN = 'Indonesian'
    IRISH = 'Irish'
    ITALIAN = 'Italian'
    JAMAICAN = 'Jamaican'
    JAPANESE = 'Japanese'
    JEWISH = 'Jewish'
    KOREAN = 'Korean'
    LEBANESE = 'Lebanese'
    MEXICAN = 'Mexican'
    MOROCCAN = 'Moroccan'
    PAKISTANI = 'Pakistani'
    PERUVIAN = 'Peruvian'
    POLISH = 'Polish'
    PORTUGUESE = 'Portuguese'
    PUERTO_RICAN = 'Puerto Rican'
    RUSSIAN = 'Russian'
    SPANISH = 'Spanish'
    SWEDISH = 'Swedish'
    THAI = 'Thai'
    VIETNAMESE = 'Vietnamese'
    OTHER = 'Other'


    @classmethod
    def getCuisines(cls):
        return [(cuisine.value, cuisine.value) for cuisine in cls]

class Hour(Enum):
    CLOSED = 'Closed'
    H00 = '00'
    H01 = '01'
    H02 = '02'
    H03 = '03'
    H04 = '04'
    H05 = '05'
    H06 = '06'
    H07 = '07'
    H08 = '08'
    H09 = '09'
    H10 = '10'
    H11 = '11'
    H12 = '12'
    H13 = '13'
    H14 = '14'
    H15 = '15'
    H16 = '16'
    H17 = '17'
    H18 = '18'
    H19 = '19'
    H20 = '20'
    H21 = '21'
    H22 = '22'
    H23 = '23'

    @classmethod
    def getHours(cls):
        return [(hour.value, hour.value) for hour in cls]
