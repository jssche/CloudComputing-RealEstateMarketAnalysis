import logo from './logo.svg';
import './App.css';
// import NavBar from './Component/NavBar/NavBar';
import { Grid } from '@material-ui/core';
import ToolBar from "./Component/NavBar/Toolbar"
// import Leaflet from './Pages/Leaflet';
// import Test from './Pages/test';
import MapPage from './Pages/MapPage';
import  {AxiosAPI}  from './Component/AxiosAPI';

function App() {
  return (
    <MapPage />
  );
}

export default App;
