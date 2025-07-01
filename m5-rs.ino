#include <WiFi.h>
#include <ArduinoWebsockets.h>

// Using M5Unified library for M5Stack devices (tested with Cardputer and StickC Plus 2)
#include "M5Unified.h"

// Set your WiFi credentials and WebSocket server details in configs.h
#include "configs.h"

using namespace websockets;

WebsocketsClient ws_client;

M5Canvas canvas(&M5.Display);

void onMessageCallback(WebsocketsMessage message) {
    size_t payload_length = message.length();
    canvas.drawJpg((const uint8_t*)message.c_str(), payload_length);
    canvas.pushSprite(0, 0);
}

void onEventsCallback(WebsocketsEvent event, String data) {
    if(event == WebsocketsEvent::ConnectionOpened) {
        Serial.println("Connnection Opened");
    } else if(event == WebsocketsEvent::ConnectionClosed) {
        Serial.println("Connnection Closed");
    } else if(event == WebsocketsEvent::GotPing) {
        Serial.println("Got a Ping!");
    } else if(event == WebsocketsEvent::GotPong) {
        Serial.println("Got a Pong!");
    }
}

void setup() {
    Serial.begin(115200);
    auto cfg = M5.config();
    M5.begin(cfg);
    M5.Display.setRotation(1);
    canvas.createSprite(M5.Display.width(),
                        M5.Display.height());
    canvas.setPaletteColor(1, GREEN);
    canvas.setTextSize((float)canvas.width() / 160);
    canvas.setTextScroll(true);

    canvas.printf("Connecting WiFi: %s\n", WIFI_SSID);
    canvas.pushSprite(0, 0);

    WiFi.begin(WIFI_SSID, WIFI_PASS);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    canvas.printf("Connecting WS: %s\n", WS_HOST);
    canvas.pushSprite(0, 0);

    ws_client.onMessage(onMessageCallback);
    ws_client.onEvent(onEventsCallback);
    ws_client.connect(WS_HOST, WS_PORT, WS_PATH);
    ws_client.send("{\"quality\": " + String(JPG_QUALITY) + ", \"fps\": " + String(STREAM_FPS) +
                   ", \"width\": " + String(STREAM_WIDTH) + ", \"height\": " + String(STREAM_HEIGHT) + "}");
}

void loop() {
    ws_client.poll();
    M5.update();
    if (M5.BtnA.wasPressed()) {
        ESP.restart();
    }
}
