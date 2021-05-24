import React, { Component, useCallback } from 'react';
import { Grid } from '@material-ui/core';
import { MapContainer, TileLayer, Map, Popup } from 'react-leaflet'
import MelGeojson from "../data/SA3Geo.json"
import data from "../data/houseMarket_2019_Feb.json"
import "leaflet/dist/leaflet.css" 
import useStyles from "./Styles"
import ToolBar from "../Component/NavBar/Toolbar"
import Geojson from "../Component/Geojson"



function getData(suburbCode) {
  const amount = data[suburbCode].auction_activity_auctionlistedcount;
  const midPriceForSale = data[suburbCode].for_sale_both_auction_private_treaty_medianprice;
  const midPriceSold = data[suburbCode].sold_both_auction_private_treaty_medianprice;
  return "total amount:" + amount + "\n mid price for sale:" + midPriceForSale + "\n mid price sold:" + midPriceSold;
}

function getNumber(suburbCode,standard) {
  return data[suburbCode][standard];
}

function getMax (standard){
  var max = 0;
  for (var key in data){
    if(data[key][standard] != undefined && max < data[key][standard]){
      max = data[key][standard];
    }
  }
  console.log("max:"+max);
  return max;
}

function getMin (standard, max){
  var min = max;
  for (var key in data){
    if(data[key][standard] != undefined && min > data[key][standard]){
      min = data[key][standard];
    }
  }
  console.log("min:"+min);
  return min;
}

export default function Test(props) {

    const position = [-37.805, 145.00];


    const max = getMax(props.standard);
    const min = getMin(props.standard,max);
    console.log(props.standard);
    
    return (
      <MapContainer center={position} zoom={12} scrollWheelZoom={true} style={{ height: '90vh', width: '100%' }}>
        <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />      
        <Geojson min={min} max={max} title={props.standard}/>
      </MapContainer>
    );
}
