const ws = require('ws');

const client = new ws('ws://localhost:3000');

client.on('message', function incoming(data) {
    console.log(JSON.parse(data));
  });
  