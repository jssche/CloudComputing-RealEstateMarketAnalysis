import Background from '../data/background.png';
import React, { Component } from 'react';
import { CardMedia } from '@material-ui/core';
import Card from '@material-ui/core/Card';


//定义背景样式

var sectionStyle = {
  width: "100%",
  height: "400px",
// makesure here is String确保这里是一个字符串，以下是es6写法
  backgroundImage: `url(${Background})` 
};

export default class HomePage extends Component{
//渲染页面
render(){
        return (
            <img src={Background} alt="Logo" style={{width: "100%",height:"92vh"}}/>
        )

    }

}