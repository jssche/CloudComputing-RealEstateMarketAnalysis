import React, { Component } from 'react';
import { Grid } from '@material-ui/core';
import ToolBar from "../Component/NavBar/Toolbar"
import Leaflet from './Leaflet';
import axios from 'axios';
import Scenario from './Scenario';
import HomePage from "./HomePage";




 
class MapPage extends Component {  
    constructor(props) {
        super(props);

        this.state = {
            standard : "ForsaleYearAverage",
            position : "mel",
            shapeFile: null,
            date: "2019",
            propertyType: "House",
            display: "home",
            population: null,
            ip: window.location.host.split(":")[0],
            // ip: "172.26.132.96"
        };
        this.getFile(this.state.position);
        this.getPopulation(this.state.position);
    }  

    convertToLocation(position){
        if(position == "mel") return [-37.805, 145.00];
        else if(position== "syd") return [-33.869, 151.209];
        else return [-27.471, 153.026];
    }

    setDisplay(name){
        this.setState({display: name});
    }

    setStandard(standard){
        this.setState({standard: standard});
    }

    setPosition(position){
        this.setState({position: position});
        this.getFile(position);
        this.getPopulation(position);
    }

    setDate(date){
        this.setState({date: date});
    }

    setPropertyType(propertyType){
        this.setState({propertyType: propertyType});
    }

    getFile(position){
        var url = "http://admin:admin@"+this.state.ip+":5984/aurin-geo/" + position;
        // console.log('http://admin:admin@172.26.131.149:5984/aurin-geo/' + position);
        // var url = 'http://admin:admin@172.26.131.149:5984/aurin-geo/mel';
        axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        .then(
            response => {
                this.setState({ shapeFile: response.data.features });
            }
        );
    }




    getPopulation(position){
        const startkey= "key=%5B2019%2C%22"+position+"%22%5D&";
        const endkey = "endkey=%5B2019%2C%22"+position+"%22%2C%7B%7D%5D";
        const url="http://admin:admin@"+this.state.ip+":5984/aurin-population/_design/population/_view/population?group_level=2&"+startkey+endkey;
        axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        .then(
            response => {
              this.setState({population: response.data.rows[0].value});
            }
        );
      }



    render() { 
        const attributes ={
            position: this.state.position,
            shapeFile: this.state.shapeFile,
            standard: this.state.standard,
            date: this.state.date,
            propertyType: this.state.propertyType,
            population : this.state.population,
            ip: this.state.ip,
        }
        const functions ={
            setStandard: (name) =>this.setStandard(name),
            setPosition: (position) =>this.setPosition(position),
            setDate: (date) =>this.setDate(date),
            setPropertyType: (propertyType) =>this.setPropertyType(propertyType),
            setDisplay: (name) => this.setDisplay(name),
        }
        return (
            <Grid container direction="column">
                {/* <ToolBar attributes={attributes} setStandard={(name) =>this.setStandard(name)} setPosition={(position) =>this.setPosition(position)}/> */}
                <Grid item xs={12}>
                    <ToolBar attributes={attributes} functions={functions}/>
                </Grid>
                {this.state.display == "map"?
                <Leaflet attributes={attributes} setStandard={(name) =>this.setStandard(name)} onChange={this.stateChange}/>
                :this.state.display == "scenario"?
                <Scenario attributes={attributes}/>
                :<HomePage />}
                
            </Grid>
        );
    }
}
 
export default MapPage;