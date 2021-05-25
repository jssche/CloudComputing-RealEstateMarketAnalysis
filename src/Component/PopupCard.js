import React, { Fragment } from "react";


import { Typography, Card, Grid} from "@material-ui/core";

// import useStyles from "./Styles";

export default function PopupCard(props) {
//   const { renderSelectField } = props;
//   const classes = useStyles();


  return (
    <Grid item xs={4}>
      <Card >
        <Typography>{props.text}</Typography>
    </Card>
    </Grid>
  );
}
