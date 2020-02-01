import urllib.request
import datetime
import time
import json

# Create header of csv file with column names
# Only has to be ran once
with open("barcelona/test_scrape.csv", mode="w+") as f:
    f.write('time;id;type;latitude;longitude;streetName;streetNumber;altitude;slots;bikes;nearbyStations;status')
    f.write("\n")


# Define function to get json response
def get_response(url):
    resp = urllib.request.urlopen(url)
    data = resp.read()
    json_dt = json.loads(data)
    return json_dt


url_bcn = "http://wservice.viabicing.cat/v2/stations"
delim = ";"

# a+ for append, as the file is created with the header above
with open("barcelona/test_scrape.csv", mode="a+") as f:

    # We want to do requests every 5 seconds for a complete day.
    # 86400 seconds in a day, divided by 5 is 17280
    for i in range(17280):
        print(i)
        # Get json response
        bicycle_dict = get_response(url_bcn).get('stations')

        # Iterate over each row and append to csv file
        for j in bicycle_dict:
            j_vals = delim.join(j.values())
            # To know the specific second that we requested the data
            timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.write(timestamp + delim + j_vals)
            f.write("\n")

        time.sleep(5)
