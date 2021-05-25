import React from 'react';
import axios from 'axios';

class AxiosAPI extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            totalReactPackages: null
        };
    }

    componentDidMount() {
        // Simple GET request using axios
        const url = "http://admin:admin@172.26.131.149:5984/aurin-property/_design/housePrice/_view/SoldYearMinimum?group_level=4&startkey=%5B2019%2C%22House%22%2C%22NSW%22%5D&endkey=%5B2019%2C%22House%22%2C%22NSW%22%2C%7B%7D%5D";
        axios.get(url, {
        headers: {'Authorization': 'Basic YWRtaW46YWRtaW4='}
        }).then(
            response => {
                this.setState({ totalReactPackages: response.data });
                console.log(response)
            }
        );
    }

    render() {
        const { totalReactPackages } = this.state;
        console.log(this.state.totalReactPackages)
        return (
            <div className="card text-center m-3">
                <h5 className="card-header">Simple GET Request</h5>
                <div className="card-body">
                    Total react packages: {totalReactPackages}
                </div>
            </div>
        );
    }
}

export { AxiosAPI }; 