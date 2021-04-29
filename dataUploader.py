import os
import json
import requests
import geopandas as gpd

def getSA3Geo():
    districts = gpd.read_file(r'./AURIN_data/Geometry/ed02f7e0-8037-42e5-a3da-34f1795fd8c5.shp')
    districts = districts.iloc[:,-3:]
    districts = districts.rename(columns={'feature_c0': 'SA3_code', 'feature_n1': 'SA3_name'}) 
    districts = districts.to_json()
    return districts 

def upload(payload, doc_id):
    headers = {'content-type': 'application/json'}
    url = 'http://admin:admin@172.17.0.2:5984/aurin/'+doc_id
    r = requests.put(url, data=payload, headers=headers)
    print(r.text)

def uploadData(data_type, cols, top_root):
    for root, dirs, files in os.walk(top_root):
        for file in files:
            if file.endswith('.json') and file.startswith('data'):
                file_path = root + '/' + file
                year = file_path[46:50]
                month = file_path[51:54]
                doc_id = data_type + '_' + year + '_' + month
                with open(file_path) as f:
                    raw_data = json.load(f)
                    data = clean_data(raw_data, cols)
                    upload(data, doc_id)

def clean_data(raw_data, cols):
    output = {}
    raw_data = raw_data['features']
    for district in raw_data:
        district_code = district['properties']['sa32016code']
        output[district_code] = {}
        for c in cols:
            output[district_code][c] = district['properties'][c]
    output_json = json.dumps(output)
    return output_json

def main():
    data_type = ['houseMarket']
    dir_dict = {
        'houseMarket' : './AURIN_data/TimeSeries Property Data'
    }
    col_dict = {
        'houseMarket' : ['datemonth', 
                         'dateyear', 
                         'sa32016name',
                         'sa32016code',
                         'auction_activity_auctionclearancerate',
                         'auction_activity_auctionlistedcount',
                         'for_sale_both_auction_private_treaty_averageprice',
                         'for_sale_both_auction_private_treaty_maximumprice',
                         'for_sale_both_auction_private_treaty_medianprice',
                         'for_sale_both_auction_private_treaty_minimumprice',
                         'for_sale_both_auction_private_treaty_standarddeviationprice',
                         'for_sale_both_auction_private_treaty_totalprice',
                         'sold_both_auction_private_treaty_averageprice',
                         'sold_both_auction_private_treaty_maximumprice',
                         'sold_both_auction_private_treaty_medianprice',
                         'sold_both_auction_private_treaty_minimumprice',
                         'sold_both_auction_private_treaty_standarddeviationprice',
                         'sold_both_auction_private_treaty_totalprice']
    }

    geoData = getSA3Geo()
    upload(geoData, 'SA3Geo')
    uploadData('houseMarket', col_dict['houseMarket'], dir_dict['houseMarket'])
    

    

if __name__ == "__main__":
    main()