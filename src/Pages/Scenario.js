import AliceCarousel from 'react-alice-carousel';
import 'react-alice-carousel/lib/alice-carousel.css';
import Piechart from '../Component/PieChart';
import PopupCard from '../Component/PopupCard';
import React, { Component } from 'react';
import { Grid } from '@material-ui/core';
import ToolBar from "../Component/NavBar/Toolbar"
import Leaflet from './Leaflet';
import axios from 'axios';
import HomePage from "./HomePage";



class Scenario extends Component{
    constructor(props) {
        super(props);

        this.state = {
            text : null,
        };
        this.getTwt();
    }  

    // const responsive = {
    //     0: { items: aa },
    //     568: { items: bb },
    //     1024: { items: cc },
    // };
    
    // items = [
    //     <div className="item" data-value="1">1</div>,
    //     <div className="item" data-value="2">2</div>,
    //     <div className="item" data-value="3">3</div>,
    //     <div className="item" data-value="4">4</div>,
    //     <div className="item" data-value="5">5</div>,
    // ];
    // word=[
    //     "aa",
    //     "bb",
    //     "cc",
    //     "dd"
    // ];

    // twitterCard= () =>{
    //     return word.map((text)=>(
    //         <PopupCard text={text} />
    //     ))
    // };


    getTwt = () => {
        const city = this.props.attributes.position == "mel"?"melbourne": this.props.attributes.position == "syd"?"sydney":"brisbane";
        const startkey = "startkey=%5B%22"+city+"%22%5D&";
        const endkey ="endkey=%5B%22"+city+"%22%2C%7B%7D%5D";
        var url = "http://admin:admin@172.26.133.91:5984/twitter-property/_design/twitterProperty/_view/twittertext?" + startkey+endkey;
        // console.log('http://admin:admin@172.26.131.149:5984/aurin-geo/' + position);
        // var url = 'http://admin:admin@172.26.131.149:5984/aurin-geo/mel';
        axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        .then(
            response => {
                const data = response.data.rows;
                const dict = [];
                for(var key in data){
                    dict.push(data[key].value.text);
                }
                this.setState({ text: dict });
            }
        );
    }
        
    


    render(){
        const twt = this.state.text;
        console.log(twt)
        return(
            <AliceCarousel 
            mouseTracking
            items={twt==null?"a":twt}
            controlsStrategy="alternate" />
        )
    }
}

export default Scenario;