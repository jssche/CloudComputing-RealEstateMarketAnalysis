import React from 'react';
import {Grid,Button,Menu,MenuItem} from "@material-ui/core";
import useStyles from '../../styleConfig';

export default function ScenarioMenu(props) {
  const classes = useStyles();
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const clickedMelbourne = () => {
    props.functions.setDisplay("scenario");
    props.functions.setPosition("mel");
    setAnchorEl(null);
  };

  const clickedSydney = () => {
    props.functions.setDisplay("scenario");
    props.functions.setPosition("syd");
    setAnchorEl(null);
  };

  const clickedBrisbane = () => {
    props.functions.setDisplay("scenario");
    props.functions.setPosition("bne");
    setAnchorEl(null);
  };

  return (
    <div>
    <Grid item xs={2}>
      <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} className={classes.navbarButton}>
        Statistics
      </Button>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={clickedMelbourne}>Melbourne</MenuItem>
        <MenuItem onClick={clickedSydney}>Sydney</MenuItem>
        <MenuItem onClick={clickedBrisbane}>Brisbane</MenuItem>
      </Menu>
    </Grid>

    </div>
  );
}