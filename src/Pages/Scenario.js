import AliceCarousel from 'react-alice-carousel';
import 'react-alice-carousel/lib/alice-carousel.css';
import PopupCard from '../Component/PopupCard';
import React, { Component } from 'react';
import { Grid } from '@material-ui/core';
import ToolBar from "../Component/NavBar/Toolbar"
import Leaflet from './Leaflet';
import axios from 'axios';
import HomePage from "./HomePage";
import MyPie from '../Component/MyPie';
import MyWordcloud from '../Component/WordCloud';



class Scenario extends Component{
    constructor(props) {
        super(props);

        this.state = {
            text : null,
            responsive: {
                500: { items: 2 },
                800: { items: 3 },
                1024: { items: 4 }
            },
            topic: null,
        };
        this.getTwt(this.props.attributes.position);
        this.getTopic(this.props.attributes.position);
    }  

    componentWillReceiveProps (nextProps){
        // console.log(nextProps)
        this.getTwt(nextProps.attributes.position)
        this.getTopic(nextProps.attributes.position)
      }


    twitterCard(list){
        return (
            list.map((text)=>(
                <PopupCard text={text} />
            ))            
        )
    };


    getTwt(position){
        const city = position == "mel"?"melbourne": position == "syd"?"sydney":"brisbane";
        const startkey = "startkey=%5B%22"+city+"%22%5D&";
        const endkey ="endkey=%5B%22"+city+"%22%2C%7B%7D%5D";
        var url = "http://admin:admin@"+this.props.attributes.ip+":5984/twitter-property/_design/twitterProperty/_view/twitterText?" + startkey+endkey;
        // console.log('http://admin:admin@172.26.131.149:5984/aurin-geo/' + position);
        // var url = 'http://admin:admin@172.26.131.149:5984/aurin-geo/mel';
        axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        .then(
            response => {
                const data = response.data.rows;
                // console.log(data)
                const dict = new Object();
                for(var key in data){
                    // dict.push(data[key].value.text);
                    dict[key] = data[key].value.text;
                }
                this.setState({ text: dict });
            }
        );
    }

    getTopic(position){
        const city = position == "mel"?"melbourne": position == "syd"?"sydney":"brisbane";
        const startkey = "startkey=%5B%22"+city+"%22%5D&";
        const endkey ="endkey=%5B%22"+city+"%22%2C%7B%7D%5D";
        var url = "http://admin:admin@"+this.props.attributes.ip+":5984/twitter-city-topic/_all_docs?include_docs=true";
        axios.get(url, {headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}})
        .then(
            response => {
                const data = response.data.rows;
                var key = null;
                if(position=="mel"){
                    key=1;
                }
                else if(position=="syd"){
                    key=0;
                }
                else{key=2}
                const topic = data[key].doc[position];
                this.setState({topic: topic})
            }
        );
    }

        
    


    render(){
        // this.setState({text : this.dict})
        // console.log(this.state.text);
        let list=["no twitter comment yet"];
        if(this.state.text != null){
            list = [];
            let dict = this.state.text;
            // console.log(dict);
            for(var key in dict){
                list.push(dict[key]);
            }
        }
        console.log(this.state.topic)
        return(
            <Grid container justify="center" alignItems="center" item  xs={12}>
                <MyPie data={this.props.attributes.population} topic={this.state.topic}/> 
                {/* <MyWordcloud topics={this.word}/> */}
                <AliceCarousel
                mouseTracking
                items={this.twitterCard(list)}
                style={{marginTop: "2em"}} 
                responsive={this.state.responsive}
                controlsStrategy="alternate" />      
            </Grid>
                      
        )
    }
}

export default Scenario;