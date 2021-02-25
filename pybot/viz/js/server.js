const express = require('express');
const ws = require('ws');
const Redis = require("ioredis");
const zmq = require("zeromq")
const redis = new Redis();
const app = express();

function get_topics()
{
    return redis.hgetall("bot_topics").then(function (result) {
        return result
      });      
}

const wss = new ws.Server({ noServer: true });

async function send_sub(topic,port){
    const sock = new zmq.Subscriber
    sock.connect("tcp://127.0.0.1:"+port)
    sock.subscribe("")
    for await (const [msg] of sock) {
      console.log(JSON.parse(msg))
    }
}

wss.on('open', function connection(wss) {
  get_topics().then(async function(topics) {

    for (const [topic, port] of Object.entries(topics)) {
      send_sub(topic,port)
    }
    //topic_data[topic] = msg
    //wss.send(JSON.stringify(topic_data));
  })

});

const server = app.listen(3000);
server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, socket => {
    wss.emit('open', socket, request);
  });
});
