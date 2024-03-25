import asyncio
import json
import websockets


async def receive(self, uri):
    async with websockets.connect(uri) as websocket:
        while True:
            recv_text = await websocket.recv()
            recvtext = json.loads(recv_text)
            if recvtext['form'] == 'event':
                recvtext = recvtext['data']
                if recvtext['detail'] == 'fire':
                    msg = f"摄像头({recvtext['cam_name']})疑似出现火情，时间点{recvtext['time'][:19]}"
                    # print(msg)
                elif recvtext['detail'] == 'smoke':
                    msg = f"摄像头({recvtext['cam_name']})疑似出现烟雾，时间点{recvtext['time'][:19]}"
                    # print(msg)
                else:
                    msg = f"摄像头({recvtext['cam_name']})疑似有陌生人，时间点{recvtext['time'][:19]}"
                    # print(msg)

def recv(token):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(receive(f'ws://43.143.245.240:8000/ws/event/{token}/'))