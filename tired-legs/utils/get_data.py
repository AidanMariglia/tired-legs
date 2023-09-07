from io import StringIO
import requests
import csv

BASE_URL = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

def get_benches() -> csv.reader:
    url = BASE_URL + "/api/3/action/package_show"
    params = {"id": "street-furniture-bench"}
    package = requests.get(url, params=params).json()

    url = BASE_URL + "/datastore/dump/" + package["result"]["resources"][0]["id"]
    resource_data_dump = requests.get(url).text

    f = StringIO(resource_data_dump)
    return csv.reader(f, delimiter=',')

def main():
    reader = get_benches()
    i = 0
    for row in reader:
        if i > 2:
            break
        print('\t'.join(row))
        i += 1

# id (we will generate on insert) UUID
# addressnumber text
# address street text
# fronting street text
#SIDE text

if __name__=="__main__":
    main()