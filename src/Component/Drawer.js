import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import Drawer from '@material-ui/core/Drawer';
import Button from '@material-ui/core/Button';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import MailIcon from '@material-ui/icons/Mail';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import StarBorder from '@material-ui/icons/StarBorder';
import Collapse from '@material-ui/core/Collapse';
import SettingsIcon from '@material-ui/icons/Settings';
// import Test from "../Pages/test"


const useStyles = makeStyles({
  list: {

  },
  fullList: {
    width: 'auto',
  },
});

export default function SideDrawer(props) {
  // const changeStandard = props;
  const standards = [
    'ForsaleYearAverage',
    'ForsaleYearMaximum',
    "ForsaleYearMinimum",
    "ForsaleYearTotal",
    "SoldYearAverage",
    "SoldYearMaximum",
    "SoldYearMinimum",
    "SoldYearTotal",
    "ClearanceRate"
  ];

  const para = [
    'for_sale_average_price',
    'for_sale_maximum_price',
    "for_sale_minimum_price",
    "for_sale_total_price",
    "sold_average_price",
    "sold_maximum_price",
    "sold_minimum_price",
    "sold_total_price",
  ];

  const dates =[
    "2019",
    "2020",
  ];

  const propertyType =[
    "House",
    "Unit"
];

  const classes = useStyles();
  const [state, setState] = React.useState({
    left: true,
  });
  // console.log(props.standard)

  const [coloropen, setColorOpen] = React.useState(false);
  const [dateopen, setDateOpen] = React.useState(false);
  const [propertyopen, setPropertyOpen] = React.useState(false);


  const handleColorClick = () => {
    setColorOpen(!coloropen);
  };

  const handleDateClick = () => {
    setDateOpen(!dateopen);
  };

  const handlePropertyClick = () => {
    setPropertyOpen(!propertyopen);
  };



  const toggleDrawer = (anchor, open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }

    setState({ ...state, [anchor]: open });
  };

  const pickTitle = (event) => {
    // console.log(event);
    props.functions.setStandard(event.target.innerText);
    setColorOpen(!coloropen);
  };

  const pickDate = (event) => {
    // console.log(event.target.innerText);
    props.functions.setDate(event.target.innerText);
    setDateOpen(!dateopen);
  };

  const pickProperty = (event) => {
    // console.log(event.target.innerText);
    props.functions.setPropertyType(event.target.innerText);
    setPropertyOpen(!propertyopen);
  };

  const list = (anchor) => (
    <div
      className={clsx(classes.list, {
        [classes.fullList]: anchor === 'top' || anchor === 'bottom',
      })}
      role="presentation"
      onKeyDown={toggleDrawer(anchor, false)}
    >
      <List>
        <ListItem button onClick={handleColorClick}>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary={"rank by: " + props.attributes.standard} />
          {coloropen ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={coloropen} timeout="auto" onClick={toggleDrawer(anchor, false)}>
          <List component="div" disablePadding>
            {standards.map((text) => (
              <ListItem key={text} aria-label={text} button className={classes.nested} onClick={pickTitle}>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </Collapse>
        <Divider />
        <ListItem button onClick={handleDateClick}>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary={"filter time: " + props.attributes.date} />
          {dateopen ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={dateopen} timeout="auto" onClick={toggleDrawer(anchor, false)}>
          <List component="div" disablePadding>
            {dates.map((text) => (
              <ListItem key={text} aria-label={text} button className={classes.nested} onClick={pickDate}>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </Collapse>
        <Divider />
        <ListItem button onClick={handlePropertyClick}>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary={"Property Type: " + props.attributes.propertyType} />
          {propertyopen ? <ExpandLess /> : <ExpandMore />}
        </ListItem>
        <Collapse in={propertyopen} timeout="auto" onClick={toggleDrawer(anchor, false)}>
          <List component="div" disablePadding>
            {propertyType.map((text) => (
              <ListItem key={text} aria-label={text} button className={classes.nested} onClick={pickProperty}>
                <ListItemText primary={text} />
              </ListItem>
            ))}
          </List>
        </Collapse>
      </List>
      {/* <Divider /> */}
    </div>
  );

  return (
    <div>
      {[''].map((anchor) => (
        <React.Fragment key={anchor}>
          <IconButton onClick={toggleDrawer(anchor, true)} edge="start" color="inherit" className={classes.menuButton} aria-label="menu">
            <MenuIcon />{anchor}
          </IconButton>
          <Drawer anchor={anchor} open={state[anchor]} onClose={toggleDrawer(anchor, false)}>
            {list(anchor)}
          </Drawer>
        </React.Fragment>
      ))}
    </div>
  );
}