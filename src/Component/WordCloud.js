import React from 'react';
import ReactWordcloud from 'react-wordcloud';
import styled from 'styled-components';
import {Grid, Typography} from "@material-ui/core";
import useStyles from "../styleConfig";



 
const MyWordcloud = (topics) => {

    console.log(topics)
    const classes = useStyles();

    let words = []
    const topics2 = topics.topics
    topics2.forEach(element => {
        let value = element[1].split('+')
        value.forEach(element => {
            let topic_weight = element.split('*')[0].trim()
            let topic_text  = element.split('*')[1].replace('"', '').replace('"', '')
            let pair = {text: topic_text,
                        value: topic_weight,}
            words.push(pair)
        })
    });

    const options = {
        fontSizes: [30,50] // min & max font sizes
    };
    

    return (
        <Grid item style={{padding: "1em"}}>
            <Typography className={classes.dataTitle}>topic words cloud:</Typography>
            <ReactWordcloud words={words} options={options} fontSizes={"20px","25px"}/>
        </Grid>
    ) 
}

export default MyWordcloud;