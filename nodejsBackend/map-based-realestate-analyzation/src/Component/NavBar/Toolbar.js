import React, { Component } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import useStyles from "../../styleConfig";
import ScenarioMenu from "./ScenarioMenu.js";
import MapMenu from "./MapMenu";
import HomeButton from "./HomeButton";
import FilterDrawer from "../Drawer"

const classes = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    backgroundColor: "#c49991",
  },
}));

export default function NavToolbar(props) {

  // const {changeStandard} = props;
  const classes = useStyles();

  // console.log(props);
  return (
    // <div className={classes.root}>
      <AppBar position="static" className={classes.root}>
        <Toolbar>
          <FilterDrawer attributes={props.attributes} functions={props.functions}/>
          <Typography variant="h6" className={classes.title}>
            Real estate Analyze
          </Typography>
          <ScenarioMenu />
          <MapMenu setPosition={(position) => props.functions.setPosition(position)}/>
          <HomeButton />
        </Toolbar >
      </AppBar>
    // </div>
  );
}
