import asyncio
import websockets
from pybot import Bot, Subscriber
import time
import jsonpickle

sleep_time=2

bot = Bot()
bot.start()
sub = Subscriber(bot)
topics = bot.get_all_topics()

async def publish_topics(websocket, path):
    while True:
        try:
            data = sub.single_subscribe(topics)
            data = jsonpickle.encode(data)
            
            await websocket.send(data)
            time.sleep(sleep_time)
        except websockets.ConnectionClosed:
            print("Connection to client closed.")
            return

start_server = websockets.serve(publish_topics, "localhost", 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()