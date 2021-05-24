const app = require('express')()
const http = require('http').createServer(app)
const io = require('socket.io')(http, {cors: {origin:'*'}})
const NodeCouchDb = require('node-couchdb')

const couch = new NodeCouchDb({
    host: 'couchdbnode',
    protocol: 'http',
    port: 5984,
    auth: {
        user: 'admin',
        password: 'admin'
    }
});

io.on('connection', socket => {
    console.log('getting new connect ' + socket.id)
    socket.on('position', (position) => {
        console.log(position)
        db_name = 'aurin-geo'
        couch.get(db_name, position).then(({data, headers, status}) => {
            console.log(status)
            socket.emit('geo-data', data)
        }, err => {
            // either request error occured
            // ...or err.code=EDOCMISSING if document is missing
            // ...or err.code=EUNKNOWN if statusCode is unexpected
        });

    }) 
});


http.listen(8080, function() { 
    console.log('listening on port 8080');
})
