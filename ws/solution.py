import asyncio
import websockets
import json
import aiohttp
import time


def find_interval(elapsed):
    intervals = [700, 1500, 2000, 2500, 3000]
    res = intervals[0]
    for interval in intervals:
        if abs(interval - elapsed) < abs(res - elapsed):
            res = interval
    return res


async def main():
    token_url = "https://hackattic.com/challenges/websocket_chit_chat/problem?access_token=9099aaae9c650db1"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(token_url) as resp:
            data = await resp.json()
            token = data['token']
    
    ws_url = f"wss://hackattic.com/_/ws/{token}"
    async with websockets.connect(ws_url) as websocket:
        start = None
        while True:
            try:
                message = await websocket.recv()
                now = time.perf_counter()
                print(f"Received:", message)
                if message == "good!":
                    continue
                if str(message).startswith("congratulations!"):
                    secret = str(message).split('"')[1]
                    print("Secret:", secret)
                    solution = { 'secret' : secret } 
                    solve_url = "https://hackattic.com/challenges/websocket_chit_chat/solve?access_token=9099aaae9c650db1"
                    async with aiohttp.ClientSession() as session:
                        async with session.post(solve_url, json=solution) as resp:
                            resp = await resp.json()
                            print("Response:", resp)
                        break
                
                if start is None:
                    start = now
                else:
                    elapsed = (now - start) * 1000 
                    print("Elapsed:", elapsed)
                    interval = find_interval(elapsed)
                    print("Interval:", interval)
                    await websocket.send(str(interval))
                    start = now

                
            except websockets.ConnectionClosed:
                print("Connection closed.")
                break


asyncio.run(main())
