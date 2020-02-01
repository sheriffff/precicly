import time
import datetime
import json
from madrid.bicimad import BiciMad

bicimad = BiciMad()
state_prev = None

datas = []

for _ in range(100):
    time.sleep(10)
    data, state = bicimad.get_stations_info()

    if state != state_prev:
        print(datetime.datetime.now())
        print(data[0])
        print('\n')

        datas.append(data)
        state_prev = state

json.dump(datas, open('data.json', 'w+'))
print('DONE')
