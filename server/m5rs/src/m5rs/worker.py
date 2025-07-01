import os, time
import asyncio
import signal
import json
from websockets.asyncio.server import serve
from .capture import capture_window, resize_image, image_to_jpeg_bytes

WS_PORT = 8765
FPS = 30
JPG_QUALITY = 75
FRAME_WIDTH = 240
FRAME_HEIGHT = 135
window_id = int(os.environ.get("WINDOW_ID", "0"), 16)

def get_next_frame(jpg_quality, w, h):
    image = capture_window(window_id)
    resized_image = resize_image(image, w, h)
    jpeg_bytes = image_to_jpeg_bytes(resized_image, quality=jpg_quality)
    return jpeg_bytes

async def stream_images(websocket):
    async for message in websocket:
        print(f"Received message: {message} from {websocket.remote_address}")
        configs = json.loads(message)
        jpg_quality = configs.get("jpg_quality", JPG_QUALITY)
        fps = configs.get("fps", FPS)
        w = configs.get("width", FRAME_WIDTH)
        h = configs.get("height", FRAME_HEIGHT)
        while True:
            start_time = time.time()
            jpg_data = get_next_frame(jpg_quality, w, h)
            await websocket.send(jpg_data)
            elapsed_time = time.time() - start_time
            sleep_time = max(0, (1 / fps) - elapsed_time)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

async def start_websocket_server():
    print(f"Starting WebSocket server on port {WS_PORT}, window ID: {window_id:#x}")
    async with serve(stream_images, "0.0.0.0", WS_PORT) as server:
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGTERM, server.close)
        await server.wait_closed()
