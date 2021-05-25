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

  return (
    <div>
    <Grid item xs={2}>
      <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} className={classes.navbarButton}>
        Scenario
      </Button>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
        <MenuItem onClick={handleClose}>Profile</MenuItem>
        <MenuItem onClick={handleClose}>My account</MenuItem>
        <MenuItem onClick={handleClose}>Logout</MenuItem>
      </Menu>
    </Grid>

    </div>
  );
}