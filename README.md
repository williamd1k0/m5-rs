# M5 Remote Streaming

This project is a simple remote desktop streaming application for some M5Stack devices (tested on M5Stack Cardputer and StickC Plus 2).
It allows you to stream a window from your computer using a WebSocket server.

> [!WARNING]
> As I am not a professional MCU/IoT developer, this code may not be the most efficient or optimal solution. It was created as a personal project and may not follow best practices. Use it at your own risk!

The project can be built using the Arduino IDE, and aside from the `M5Stack` library, it requires only the [ArduinoWebsockets](https://www.ardu-badge.com/ArduinoWebsockets) library, which can be installed using the Library Manager.

> [!NOTE]
> The Makefile in the root directory and the compile_flags.txt.in file are just helpers to improve my development experience with the Zed Editor, so they can be ignored.

## How it works

The python server awaits for a WebSocket connection from any client. Once a client connects and sends an initial message, it starts a loop that captures a specified window at a specified interval and sends the image as a JPEG file to the client.

An optional JSON string can be sent to the server to change the following parameters:
- `fps`: Frames per second for the screen capture.
- `quality`: JPEG quality for the captured images (0-100).
- `width`: The target width to which the captured image will be resized.
- `height`: The target height to which the captured image will be resized.

> [!NOTE]
> These parameters can be set in the `configs.h` file.

As of now, the server only supports Linux X11 windows (via python-xlib).
If you wish to use this on Windows or macOS, consider modifying the `capture.py` script to support those platforms (more specifically, the `capture_window(window_id:int)` function).

The rendering on the client side is done using the `M5Canvas.drawJpg` function from the M5Stack `M5Unified` library, which decodes the JPEG image and displays it on the screen.

### Known Issues

- Due to the current implementation, both Cardputer and StickC Plus 2 devices are limited to a maximum frame rate of 15 FPS. This limitation likely stems from the devices' constrained processing capabilities and/or inefficiencies in the code.
- Audio streaming is not supported, as the focus of this project was solely on video streaming.

## Usage

### Required Tools and Libraries

Server:
- Python 3.x (tested with Python 3.12)
- Python project manager: [uv](https://docs.astral.sh/uv/) (recommended for running the server without needing to manage dependencies manually)
- Python libraries: `python-xlib`, `pillow`, `websockets`
- xorg-xwininfo (package for Linux, used for getting the window ID)
- [ripgrep](https://github.com/BurntSushi/ripgrep) (optional, used in the helper script to get the window ID)

Client:
- [Arduino IDE](https://www.arduino.cc/en/software/) (tested with version 2.3.6)
- M5Stack library and its dependencies (see [M5Stack documentation](https://docs.m5stack.com/en/arduino/arduino_ide))
- [ArduinoWebsockets](https://www.ardu-badge.com/ArduinoWebsockets) library (installable via Library Manager)


### Running the Server

The server relies on the uv project manager to ease the management of dependencies and the execution.
You may be able to run the server without uv, but it is not recommended.

The window to be captured must be specified by its ID via the `WINDOW_ID` environment variable.
The window ID can be obtained using the `xwininfo` command in Linux.

To start the server, you can use the following commands:
```sh
cd server/m5rs
WINDOW_ID=<window_id> uv run m5rs
```

Alternatively, you can use the provided helper script to get the window ID and start the server automatically:
```sh
cd server/m5rs
./serve.sh
```

There is also a helper Makefile in the `server` directory that calls the `serve.sh` script mentioned above.

```sh
cd server
make
```

### Running the Client

No additional steps are required to run the client, since the connection to the server is established automatically when the device boots up.
Just ensure to setup the `configs.h` file with your WIFI credentials, server address and optional streaming parameters before uploading the code to the device.
