import React, { Component } from 'react';
import { Grid } from '@material-ui/core';
import { MapContainer, TileLayer, Map, Popup, GeoJSON } from 'react-leaflet'
import MelGeojson from "../data/SA3Geo.json"
import data from "../data/houseMarket_2019_Feb.json"
import "leaflet/dist/leaflet.css" 
import PopupCard from "../Component/PopupCard"
import { makeStyles } from "@material-ui/core/styles";
import Geojson from "../Component/Geojson";
import axios from 'axios';






 
class Leaflet extends Component {
  constructor(props) {
    super(props);

    this.state = {
      data : null,
      max: 0,
      min: 0,
      dict : null,
      population: null,
    };
    this.getData(this.props.attributes.date,this.props.attributes.propertyType,this.props.attributes.position,this.props.attributes.standard);
    this.getPopulation(this.props.attributes.date,this.props.attributes.position);
  }

  componentWillReceiveProps (nextProps){
    // console.log(nextProps)
    this.getData(nextProps.attributes.date,nextProps.attributes.propertyType,nextProps.attributes.position,nextProps.attributes.standard);
    this.getPopulation(nextProps.attributes.date,nextProps.attributes.position)
  }

  cityToState(position){
    if(position == "mel") return "VIC";
    else if(position== "syd") return "NSW";
    else return "QLD";
  }

  getPopulation(date,position){
    const startkey= "startkey=%5B"+date+"%2C%22"+position+"%22%5D&";
    const endkey = "endkey=%5B"+date+"%2C%22"+position+"%22%2C%7B%7D%5D";
    const url="http://admin:admin@172.26.133.91:5984/aurin-population/_design/population/_view/population?group_level=3&"+startkey+endkey;
    axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
    .then(
        response => {
          console.log(response.data.rows);
          const pop = response.data.rows;
          const dict = new Object();
          for (var key in pop){
            var temp = pop[key].value.total;
            if(temp != null){
              dict[pop[key].key[2]] = temp;
              // console.log(temp)
            }
          }
          this.setState({population: dict});
        }
    );
  }

  getData(date,propertyType,position,title){
    // console.log(date+propertyType+position+title);
    const startkey = "startkey=%5B"+date+"%2C%22"+propertyType+"%22%2C%22"+this.cityToState(position)+"%22%5D&";
    const endkey = "endkey=%5B"+date+"%2C%22"+propertyType+"%22%2C%22"+this.cityToState(position)+"%22%2C%7B%7D%5D";
    var url = "http://admin:admin@172.26.133.91:5984/aurin-property/_design/housePrice/_view/"+title+"?group_level=4&"+startkey+endkey;
    axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
    .then(
        response => {
          // console.log(response);
          this.setState({ data: response.data.rows });
          this.getMax(response.data.rows);
        }
    );
    
}



  getMax (data){
    var max = 0;
    const dict = new Object();
    for (var key in data){
      var temp = data[key].value.length>1?data[key].value[0]:data[key].value;
      if(temp != null){
        dict[data[key].key[3]] = temp;
        // console.log(temp)
      }
      if(temp != undefined && max < temp){
        max = temp;
        // console.log(max);
      }
    }
    this.setState({dict: dict});
    this.setState({ max: max });
    this.getMin(data,max);
  };

  getMin (data,max){
    var min = max;
    for (var key in data){
      var temp = data[key].value.length>1?data[key].value[0]:data[key].value;
      if(temp != undefined && min > temp){
        min = temp;
        // console.log(min);
      }
    }
    // console.log("min:"+min);
    this.setState({ min: min });
  };

  convertToLocation(position){
    if(position == "mel") return [-37.805, 145.00];
    else if(position== "syd") return [-33.869, 151.209];
    else return [-27.471, 153.026];
}
  

 
  render() {
    // console.log(this.props.attributes);
    const max = 0;
    const min = 0;
    const attributes = {
      shapeFile : this.props.attributes.shapeFile,
      min : this.state.min,
      max: this.state.max,  
      dict: this.state.dict,
      population: this.state.population,
    }

    return (
      <MapContainer key={this.props.attributes.position} center={this.convertToLocation(this.props.attributes.position)} zoom={11} scrollWheelZoom={true} style={{ height: '90vh', width: '100%' }}>
        <TileLayer
        attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* <Geojson shapeFile={this.props.shapeFile} min={min} max={max} title={this.props.standard}/> */}
        <Geojson attributes={attributes}/>
      </MapContainer>
    );
    }
  }

 
export default Leaflet;