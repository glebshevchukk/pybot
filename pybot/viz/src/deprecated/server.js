const express = require('express');
const ws = require('ws');
const Redis = require("ioredis");
const zmq = require("zeromq")
const redis = new Redis();
const app = express();

const wss = new ws.Server({ noServer: true });

function get_topics()
{
    return redis.hgetall("bot_topics").then(function (result) {
      return result
    });      
}

async function send_sub(topic,port,w){
    const sock = new zmq.Subscriber
    sock.connect("tcp://127.0.0.1:"+port)
    sock.subscribe("")
    for await (const [msg] of sock) {
      let topic_data = {topic:topic,msg:JSON.parse(msg)}
      w.send(JSON.stringify(topic_data));
    }
}

wss.on('open', function connection(w) {
  console.log("Connection opened to a client.")
  get_topics().then(async function(topics) {
    for (const [topic, port] of Object.entries(topics)) {
      send_sub(topic,port,w)
    }
  })
});

wss.on('close', function close() {
  console.log('disconnected');
});


const server = app.listen(3000);
server.on('upgrade', (request, socket, head) => {
  wss.handleUpgrade(request, socket, head, socket => {
    wss.emit('open', socket, request);
  });
});
