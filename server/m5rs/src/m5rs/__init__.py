import asyncio
from .worker import start_websocket_server, capture_task

async def run_tasks():
    await asyncio.gather(
        capture_task(),
        start_websocket_server()
    )

def main():
    asyncio.run(run_tasks())

if __name__ == "__main__":
    main()
