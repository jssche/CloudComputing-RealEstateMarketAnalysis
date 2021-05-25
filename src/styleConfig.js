import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
      backgroundColor: "#c49991",
    },
    menuButton: {
      marginRight: theme.spacing(2),
    },
    title: {
      flexGrow: 1,
    },
    dataTitle: {
      fontFamily: "PT Sans",
      fontStyle: "normal",
      fontWeight: "bold",
      fontSize: "20px",
      marginLeft: "3.5em",
      marginBottom: "1em"
    },
    pie: {
      padding: "5em"
    },
    navbarButton: {
        fontSize: "16px",
        fontSize:"bold",
        color: "white"
    },
    list: {
        width: 250,
      },
      fullList: {
        width: 'auto',
      },
  }));
export default useStyles;
