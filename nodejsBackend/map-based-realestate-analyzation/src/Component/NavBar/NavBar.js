import React, { Fragment } from "react";


import { Typography, Grid, AppBar, Toolbar, IconButton } from "@material-ui/core";

import useStyles from "../../styleConfig";
import ScenarioMenu from "./ScenarioMenu.js";
import MapMenu from "./MapMenu";
import HomeButton from "./HomeButton";
import MenuIcon from '@material-ui/icons/Menu';

export default function NavBar(props) {
  const { renderSelectField } = props;
  const classes = useStyles();


  return (
    <Grid container direction="row" justify="flex-end" alignItems="center" >
      <AppBar position="static" style={{backgroundColor:"#c49991"}}>
        <Toolbar>
          <ScenarioMenu />
          <MapMenu />
          <HomeButton />
        </Toolbar>
      </AppBar>
    </Grid>
  );
}
