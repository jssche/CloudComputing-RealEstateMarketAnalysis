import { Component } from "react";
// import MelGeojson from "../data/SA3Geo.json"
// import data from "../data/houseMarket_2019_Feb.json"
import { GeoJSON } from 'react-leaflet'
import axios from 'axios';
import makeRequest from"./test"



class Geojson extends Component{
    state={
        index: this.props.attributes.dict+this.props.attributes.shapeFile,
    }

    componentWillReceiveProps (nextProps){
    this.setState({
        index: Math.random(),
    })
  }



    geojson(min,max){
        const OnEachBlock = (block,layer) => {
            var suburbCode = block.properties.SA3_code;
            var suburbName = block.properties.SA3_name;
            if(this.props.attributes.dict != null){
                var number = this.props.attributes.dict[suburbCode];
                layer.options.fillOpacity= 0.2 + 0.2*(number - min)/((max - min)/4);
                layer.bindPopup(suburbName+" \n"+number);
            }
            else{
                layer.options.fillOpacity = 0.5;
                layer.bindPopup(suburbName);
            }
            // layer.on({ 
            //     click: (event) =>{
            //       event.target.setStyle({
            //         fillColor: "#ee7a6d",
            //       });
                //   event.target.popup().setContent('<p>Hello world!<br />This is a nice popup.</p>')
            //     },
            //   });
            
        }
        return(
            <GeoJSON key={this.state.index} style={{color:"#885a5a",fillColor:"#ee7a6d",weight:"1"}} data={this.props.attributes.shapeFile} onEachFeature={OnEachBlock}/>
        );
    }


    render(){
        // this.getFile();
        // console.log(this.props.attributes)
        // console.log(this.props.attributes.shapeFile)
        return (
            this.geojson(this.props.attributes.min,this.props.attributes.max)
        )
    }
}

export default Geojson;