const axios = require('axios');

async function makeRequest() {

    const config = {
        method: 'get',
        url: 'http://admin:admin@172.26.131.149:5984/aurin-geo/bne',
        headers: { 'Authorization': 'Basic YWRtaW46YWRtaW4=' }
    }

    let res = await axios(config)

    // console.log(res.request._header);
}

makeRequest();