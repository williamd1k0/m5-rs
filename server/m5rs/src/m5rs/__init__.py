import asyncio
from .worker import start_websocket_server

def main():
    asyncio.run(start_websocket_server())

if __name__ == "__main__":
    main()
