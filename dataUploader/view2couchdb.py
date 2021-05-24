import couchdb

class viewGenerator:
    def __init__(self, server_ip,username,password,dataDB):
        serverAddress="http://%s:%s@%s:5984/" % (username, password, server_ip)
        self.server = couchdb.Server(serverAddress)
        self.dataDB = self.server[dataDB]
        if dataDB == "aurin-property":
            self.allviews={
                "ForsaleYearAverage":{
                    "reduce": "function (keys, values, rereduce) {\n  if (!rereduce) {\n    var length = values.length\n    return [sum(values)/length,length]\n  } else {\n    var length = sum(values.map(function(v){return v[1]}))\n    var avg = sum(values.map(function(v){\n      return v[0] * (v[1]/length)\n    }))\n    return [avg, length]\n  }\n}",
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.for_sale_average_price); \n}"
                },
                "ForsaleYearTotal":{
                    "reduce": "_sum",
                    "map": "function (doc) {\n  emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.for_sale_total_price); \n}"
                },
                "ForsaleYearMaximum":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.for_sale_maximum_price); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return values.reduce(function(a,b){\n      return Math.max(a,b);\n    });\n  } \n  var maxPrice=0;\n  for (var i = 0; i < values.length; i++){\n    if(values[i] > maxPrice){\n      maxPrice = values[i];\n    }\n  }\n  return maxPrice\n}"
                },
                "ForsaleYearMinimum":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.for_sale_minimum_price); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return values.reduce(function(a,b){\n      return Math.min(a,b);\n    });\n  } \n  var minPrice=values[0];\n  for (var i = 0; i < values.length; i++){\n      if(values[i]<minPrice){\n       minPrice = values[i] \n      }\n  }\n  return minPrice\n}"
                },
                "SoldYearAverage":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.sold_average_price); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (!rereduce) {\n    var length = values.length\n    return [sum(values)/length,length]\n  } else {\n    var length = sum(values.map(function(v){return v[1]}))\n    var avg = sum(values.map(function(v){\n      return v[0] * (v[1]/length)\n    }))\n    return [avg, length]\n  }\n}"
                },
                "SoldYearTotal":{
                    "reduce": "_sum",
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.sold_total_price); \n}"
                },
                "SoldYearMaximum":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.sold_maximum_price); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return values.reduce(function(a,b){\n      return Math.max(a,b);\n    });\n  } \n  var maxPrice=0;\n  for (var i = 0; i < values.length; i++){\n    if(values[i] > maxPrice){\n      maxPrice = values[i];\n    }\n  }\n  return maxPrice\n}"
                },
                "SoldYearMinimum":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.sold_minimum_price); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (rereduce) {\n    return values.reduce(function(a,b){\n      return Math.min(a,b);\n    });\n  } \n  var minPrice=values[0];\n  for (var i = 0; i < values.length; i++){\n      if(values[i]<minPrice){\n       minPrice = values[i] \n      }\n  }\n  return minPrice\n}"
                },
                "ClearanceRate":{
                    "map": "function (doc) {\n     emit([doc.year,doc.type,doc.state,doc.sa3code,doc.month], doc.auction_clearance_rate); \n}",
                    "reduce": "function (keys, values, rereduce) {\n  if (!rereduce) {\n    var length = values.length\n    return [sum(values)/length,length]\n  } else {\n    var length = sum(values.map(function(v){return v[1]}))\n    var avg = sum(values.map(function(v){\n      return v[0] * (v[1]/length)\n    }))\n    return [avg, length]\n  }\n}"
                }

            }
            self.designdoc= "_design/housePrice"
            self.generateView()
        elif dataDB == "aurin-population":
            self.allviews={
                "population":{
                    "reduce": "_sum",
                    "map": "function (doc) {\n  emit([doc.year,doc.city,doc.sa3code],{total:doc.total,\"0-19\":doc[\"0_4_years_num\"] + doc[\"5_9_years_num\"] + doc[\"10_14_years_num\"] + doc[\"15_19_years_num\"],\"20-39\":doc[\"20_24_years_num\"] + doc[\"25_29_years_num\"] + doc[\"30_34_years_num\"]+\ndoc[\"35_39_years_num\"],\"40-59\":doc[\"40_44_years_num\"] + doc[\"45_49_years_num\"] + doc[\"50_54_years_num\"]+\ndoc[\"55_59_years_num\"],\"60-84\":doc[\"60_64_years_num\"] + doc[\"65_69_years_num\"] + doc[\"70_74_years_num\"]+\ndoc[\"75_79_years_num\"]+doc[\"80_84_years_num\"],over85:doc.over_85_num,female:doc.female_num,male:doc.male});\n}"
                }
            }
            self.designdoc= "_design/population"
            self.generateView()
        elif dataDB == "aurin-building":
            self.allviews={
                "houseBuilding": {
                    "reduce": "_sum",
                    "map": "function (doc) {\n  emit([doc.year,doc.city,doc.sa3code],{newHouseNum:doc.new_houses_num,newOtherResidentialNum:doc.new_other_residential_num});\n}"
                }
            }
            self.designdoc="_design/houseNum"
            self.generateView()
        elif dataDB == "aurin-homeless":
            self.allviews={
                "clientCount": {
                    "reduce": "_sum",
                    "map": "function (doc) {\n  emit([doc.financial_year,doc.city,doc.sa3code], doc.client_count);\n}"
                }
            }
            self.designdoc="_design/homeless"
            self.generateView()
        elif dataDB == "twitter-property":
            self.allviews={
                "twitterProperty":{
                    "map": "function (doc) {\n  emit([doc.city,doc.created_at],{text:doc.text,retweet_count:doc.reweet_count,favorite_count:doc.favorite_count});\n}"
                }
            }
            self.designdoc="_design/homeless"
            self.generateView()
 

    def generateView(self):
        try:
            self.dataDB[self.designdoc] = dict(languag='javascript',views=self.allviews)
        except:
            del self.dataDB[self.designdoc]
            self.dataDB[self.designdoc] = dict(languag='javascript', views=self.allviews)










