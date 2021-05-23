import os
import json
import requests
import geopandas as gpd
from view2couchdb import viewGenerator


def upload(db_name, payload, doc_id):
    headers = {'content-type': 'application/json'}
    url = 'http://admin:admin@couchdbnode:5984/' + db_name + '/' + doc_id
    r = requests.put(url, data=payload, headers=headers)
    print(r.text)

def bulk_upload(db_name, payload):
    docs = {'docs': payload}
    docs = json.dumps(docs)
    headers = {'content-type': 'application/json'}
    url = 'http://admin:admin@couchdbnode:5984/' + db_name + '/_bulk_docs'
    r = requests.post(url, data=docs, headers=headers)
    print(r.text)

def create_db(name):
    url = 'http://admin:admin@couchdbnode:5984/' + name
    r = requests.put(url)
    print(r.text)

def uploadGeoData(db_name, geofile_dir, cities):
    for i in range (len(geofile_dir)):
        districts = gpd.read_file(geofile_dir[i])
        districts = districts.iloc[:,-3:]
        districts = districts.rename(columns={'feature_c0': 'SA3_code', 'feature_n1': 'SA3_name'})
        districts = districts.to_json()
        upload(db_name, districts, cities[i])

def uploadData(db_name, cols, new_cols, top_root):
    for root, _, files in os.walk(top_root):
        for file in files:
            if file.endswith('.json') and file.startswith('data'):
                file_path = root + '/' + file
                with open(file_path) as f:
                    raw_data = json.load(f)
                    if db_name == 'aurin-building':
                        city = file_path[22:25]
                        year = file_path[57:66] + 'FY'
                        data = prepare_data(raw_data, cols, new_cols, year, city)
                    elif db_name == 'aurin-population':
                        city = file_path[77:80]
                        data = prepare_data(raw_data, cols, new_cols, None, city)
                    elif db_name == 'aurin-homeless':
                        city = file_path[63:66]
                        data = prepare_data(raw_data, cols, new_cols, None, city)
                    else:
                        data = prepare_data(raw_data, cols, new_cols)
                    bulk_upload(db_name,data)

def prepare_data(raw_data, cols, new_cols, year=None, city=None):
    output = []
    raw_data = raw_data['features']
    for district in raw_data:
        data = {}
        if year != None:
            data['year'] = year
        if city != None:
            data['city'] = city
        for i in range(len(cols)):
            if district['properties'][cols[i]] != None:
                data[new_cols[i]] = district['properties'][cols[i]]              
            else:
                data[new_cols[i]] = 0
        output.append(data)
    return output

def main():
    cities = ['mel','syd','bne']
    db_names = ['aurin-geo', 'aurin-property', 'aurin-population', 'aurin-building', 'aurin-homeless']
    dir_dict = {
        'aurin-geo': ['./AURIN_data/Geometry/mel/ed02f7e0-8037-42e5-a3da-34f1795fd8c5.shp', 
                    './AURIN_data/Geometry/syd/27c1d1eb-4661-4928-8ec0-7151bca62078.shp',
                    './AURIN_data/Geometry/bne/048898eb-25cf-4106-9ce4-d54969dab420.shp'],
        'aurin-property' : './AURIN_data/property',
        'aurin-population': './AURIN_data/population',
        'aurin-building': './AURIN_data/building',
        'aurin-homeless': './AURIN_data/homeless'
    }
    col_dict = {
        'aurin-property' : ['datemonth', 
                            'dateyear', 
                            'propertycategorisation',
                            'state',
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
                            'sold_both_auction_private_treaty_totalprice'],

        'aurin-population': ['sa3_code_2016',
                            'sa3_name_2016',
                            'yr',
                            'estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_prsns_ttl_nm',
                            'estimated_resident_population_persons_30_june_0_4_years_num',
                            'estimated_resident_population_persons_30_june_5_9_years_num',
                            'estimated_resident_population_persons_30_june_10_14_years_num',
                            'estimated_resident_population_persons_30_june_15_19_years_num',
                            'estimated_resident_population_persons_30_june_20_24_years_num',
                            'estimated_resident_population_persons_30_june_25_29_years_num',
                            'estimated_resident_population_persons_30_june_34_years_num',
                            'estimated_resident_population_persons_30_june_35_39_years_num',
                            'estimated_resident_population_persons_30_june_40_44_years_num',
                            'estimated_resident_population_persons_30_june_45_49_years_num',
                            'estimated_resident_population_persons_30_june_50_54_years_num',
                            'estimated_resident_population_persons_30_june_55_59_years_num',
                            'estimated_resident_population_persons_30_june_60_64_years_num',
                            'estimated_resident_population_persons_30_june_65_69_years_num',
                            'estimated_resident_population_persons_30_june_70_74_years_num',
                            'estimated_resident_population_persons_30_june_75_79_years_num',
                            'estimated_resident_population_persons_30_june_80_84_years_num',
                            'estimated_resident_population_persons_30_june_persons_85_num',
                            'estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_fmls_ttl_nm',
                            'estmtd_rsdnt_ppltn_smmry_sttstcs_30_jne_mls_ttl_nm'],

        'aurin-building': ['sa3_code16',
                            'sa3_name16',
                            'new_houses_num',
                            'new_oth_resial_building_num'],

        'aurin-homeless': ['fin_yr',
                            'sa3_code',
                            'client_count',
                            'sa3_name']
    }
    new_cols = {
        'aurin-property' : ['month', 
                            'year', 
                            'type',
                            'state',
                            'sa3name',
                            'sa3code',
                            'auction_clearance_rate',
                            'auction_listed_count',
                            'for_sale_average_price',
                            'for_sale_maximum_price',
                            'for_sale_median_price',
                            'for_sale_minimum_price',
                            'for_sale_std_price',
                            'for_sale_total_price',
                            'sold_average_price',
                            'sold_maximum_price',
                            'sold_median_price',
                            'sold_minimum_price',
                            'sold_std_price',
                            'sold_total_price'],

        'aurin-population' : ['sa3code',
                            'sa3name',
                            'year',
                            'total',
                            '0_4_years_num',
                            '5_9_years_num',
                            '10_14_years_num',
                            '15_19_years_num',
                            '20_24_years_num',
                            '25_29_years_num',
                            '30_34_years_num',
                            '35_39_years_num',
                            '40_44_years_num',
                            '45_49_years_num',
                            '50_54_years_num',
                            '55_59_years_num',
                            '60_64_years_num',
                            '65_69_years_num',
                            '70_74_years_num',
                            '75_79_years_num',
                            '80_84_years_num',
                            'over_85_num',
                            'female_num',
                            'male_num'],

        'aurin-building': ['sa3code',
                            'sa3name',
                            'new_houses_num',     
                            'new_other_residential_num'],

        'aurin-homeless': ['financial_year',
                            'sa3code',
                            'client_count',
                            'sa3name']
    }
    # create databases and add design document
    for name in db_names:
        create_db(name)
        viewGenerator('couchdbnode', 'admin', 'admin', name)

    # upload Polygon geo locations
    uploadGeoData(db_names[0], dir_dict[db_names[0]], cities)

    # upload property data
    uploadData(db_names[1], col_dict[db_names[1]], new_cols[db_names[1]], dir_dict[db_names[1]])

    # upload population data
    uploadData(db_names[2], col_dict[db_names[2]], new_cols[db_names[2]], dir_dict[db_names[2]])

    # upload building data
    uploadData(db_names[3], col_dict[db_names[3]], new_cols[db_names[3]], dir_dict[db_names[3]])

    # upload homeless data
    uploadData(db_names[4], col_dict[db_names[4]], new_cols[db_names[4]], dir_dict[db_names[4]])

    
if __name__ == "__main__":
    main()