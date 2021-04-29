import json
import requests
import geopandas as gpd

def getSA3Geo():
    districts = gpd.read_file(r'./AURIN_data/Geometry/ed02f7e0-8037-42e5-a3da-34f1795fd8c5.shp')
    districts = districts.iloc[:,-3:]
    districts = districts.rename(columns={'feature_c0': 'SA3_code', 'feature_n1': 'SA3_name'}) 
    districts = districts.to_json()
    return districts 

def getHouseData():
    

def upload(payload):
    headers = {'content-type': 'application/json'}
    r = requests.post('http://admin:admin@172.17.0.2:5984/aurin', data=payload, headers=headers)
    print(r.text)

def main():
    geoData = getSA3Geo()
    houseData = getHouseData()
    # upload(geoData)

    

if __name__ == "__main__":
    main()