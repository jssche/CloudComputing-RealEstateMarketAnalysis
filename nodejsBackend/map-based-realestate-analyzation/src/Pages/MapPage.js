import React, { Component } from 'react';
import { Grid } from '@material-ui/core';
import ToolBar from "../Component/NavBar/Toolbar"
// import Leaflet from './Pages/Leaflet';
import Test from './test';
import Leaflet from './Leaflet';
import axios from 'axios';
import io from 'socket.io-client'


 
class MapPage extends Component {  
    constructor(props) {
        super(props);
        this.socket = io('http://localhost:8080');
        this.state = {
            standard : "ForsaleYearAverage",
            position : "mel",
            shapeFile: null,
            date: "2019",
            propertyType: "House"
        };
        this.getFile("mel");
    }  
    // state = {
    //     standard : "for_sale_both_auction_private_treaty_averageprice",
    //     position : [-37.805, 145.00],
    //     shapeFile: null,
    // }

    convertToLocation(position){
        if(position == "mel") return [-37.805, 145.00];
        else if(position== "syd") return [-33.869, 151.209];
        else return [-27.471, 153.026];
    }


    setStandard(standard){
        this.setState({standard: standard});
    }

    setPosition(position){
        this.setState({position: position});
        this.getFile(position);
    }

    setDate(date){
        this.setState({date: date});
    }

    setPropertyType(propertyType){
        this.setState({propertyType: propertyType});
    }

    getFile(position){
        console.log('get geo')
        
        this.socket.emit('position', position);
        this.socket.on('geo-data', (data)=>{
            console.log('geodata')
            console.log(data.features)
            if(data.features != null){
                this.setState({ shapeFile: data });
            }
        })
        // var url = 'http://admin:admin@172.26.131.215:5984/aurin-geo/' + position;
        console.log('http://admin:admin@172.26.131.215:5984/aurin-geo/' + position);
        // // var url = 'http://admin:admin@172.26.131.149:5984/aurin-geo/mel';
        // axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        // .then(
        //     response => {
        //         this.setState({ shapeFile: response.data.features });
        //     }
        // );
    }



    render() { 
        const attributes ={
            position: this.state.position,
            shapeFile: this.state.shapeFile,
            standard: this.state.standard,
            date: this.state.date,
            propertyType: this.state.propertyType,
        }
        const functions ={
            setStandard: (name) =>this.setStandard(name),
            setPosition: (position) =>this.setPosition(position),
            setDate: (date) =>this.setDate(date),
            setPropertyType: (propertyType) =>this.setPropertyType(propertyType),
        }
        return (
            <Grid container>
                {/* <ToolBar attributes={attributes} setStandard={(name) =>this.setStandard(name)} setPosition={(position) =>this.setPosition(position)}/> */}
                <ToolBar attributes={attributes} functions={functions}/>
                <Leaflet attributes={attributes} setStandard={(name) =>this.setStandard(name)} onChange={this.stateChange}/>
            </Grid>
            
        );
    }
}
 
export default MapPage;