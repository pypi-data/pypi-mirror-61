from cityair_api import CityAirRequest
import pprint
R = CityAirRequest('ek', 'Oracle23')
dicts = R.get_devices(format='dicts', include_children=True)
for d in dicts:
    print(d['serial_number'], d['misc']['description'])

   # pprint.pprint(d)

   # break