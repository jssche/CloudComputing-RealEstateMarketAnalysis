import { Pie } from 'react-chartjs-2';
import styled from 'styled-components';
import {Grid,Typography} from "@material-ui/core";
import useStyles from "../styleConfig";
import MyWordcloud from '../Component/WordCloud';




const MyPie = (props) => {
  const classes = useStyles();

    const data = props.data;
    console.log(props)

    const agedata = {
        labels: [
          '0-19',
          '20-39',
          '40-59',
          '60-84',
          'over85',
        ],
        datasets: [{
          label: 'age percentage',
          data: [data['0-19'],data['20-39'],data['40-59'],data['60-84'],data['over85']],// aurin_data
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)',
            'rgb(255, 155, 86)',
            'rgb(205, 155, 86)',
          ],
          hoverOffset: 4
        }]
      };

      const genderdata = {
        labels: [
          'female',
          'male',
        ],
        datasets: [{
          label: 'My Pie Dataset',
          data: [data["female"],data["total"]-data["female"]],// aurin_data
          backgroundColor: [
            '#885a5a',
            '#ee7a6d',
          ],
          hoverOffset: 4
        }]
      };


        const word = [
          [
            0,
            "0.143*\"sign\" + 0.143*\"x\" + 0.143*\"mean\""
          ],
          [
            1,
            "0.143*\"mean\" + 0.143*\"someone\" + 0.143*\"x\""
          ],
          [
            2,
            "0.143*\"sign\" + 0.143*\"x\" + 0.143*\"mean\""
          ],
          [
            3,
            "0.143*\"sign\" + 0.143*\"x\" + 0.143*\"explain\""
          ],
          [
            4,
            "0.234*\"sign\" + 0.128*\"sun\" + 0.128*\"someone\""
          ]
        ];



    return (
      <Grid container justify="center" alignItems="center" item style={{marginBottom: "3em"}}>
        <Grid item className={classes.pie}>
          <Typography className={classes.dataTitle}>age percentage:</Typography>
          <Pie data={agedata}
          options={{ maintainAspectRatio: true }}
        />
        </Grid>
        <Grid item className={classes.pie}>
          <Typography className={classes.dataTitle}>gender percentage:</Typography>
          <Pie data={genderdata}
          options={{ maintainAspectRatio: true }}
        />
        </Grid>
        <MyWordcloud topics={props.topic!=null?props.topic:word}/>
      </Grid>
    )
}


export default MyPie;