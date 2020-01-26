# TODO for the moment it is not a loop, just testing

from madrid.bicimad import BiciMad

bicimad = BiciMad()

df = bicimad.get_stations_dataframe()

print(df.head())
