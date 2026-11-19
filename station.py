#!/usr/bin/env python3
# Balloon Story activation station: a button or a hand sensor plays an mp3
# and/or sends a command to the venue lighting desk (grandMA2 telnet) or a UDP message.
import json, socket, subprocess, sys, threading, time

cfg = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/home/pi/station/config.json"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

player = None

def send_ma():
    # grandMA2 telnet, same as Daniel's MA button: log in, send one command line, hang up
    try:
        with socket.create_connection((cfg["ma_ip"], cfg.get("ma_port", 30000)), timeout=3) as s:
            s.sendall(f'login "{cfg["ma_user"]}" "{cfg["ma_pass"]}"\r\n{cfg["ma_command"]}\r\n'.encode())
            time.sleep(0.1)
        print("MA2 command sent:", cfg["ma_command"], flush=True)
    except OSError as e:
        print("MA2 command failed:", e, flush=True)

def fire():
    global player
    print("Triggered", flush=True)
    if cfg["play_sound"]:
        player = subprocess.Popen(["mpg123", "-q", "-o", "alsa", "-a", cfg.get("audio_device", "default"), cfg["mp3_file"]])
    if cfg.get("send_ma"):
        threading.Thread(target=send_ma, daemon=True).start()
    if cfg["send_udp"]:
        try:
            sock.sendto(cfg["udp_message"].encode(), (cfg["udp_ip"], cfg["udp_port"]))
        except OSError as e:  # no network yet: log it and keep running
            print("UDP send failed:", e, flush=True)

if cfg["trigger"] == "button":
    from gpiozero import Button
    button = Button(cfg["button_gpio"], pull_up=True, bounce_time=0.05)
    def triggered():
        return button.is_pressed
else:  # "distance": ultrasonic sensor, fires when someone comes closer than distance_mm
    from gpiozero import DistanceSensor
    sensor = DistanceSensor(echo=cfg["echo_gpio"], trigger=cfg["trigger_gpio"], max_distance=cfg.get("max_distance_m", 3))
    def triggered():
        return sensor.distance * 1000 < cfg["distance_mm"]  # .distance is in metres

last_fire = 0
last_debug = 0
last_close = 0
last_done = 0
armed = True
while True:
    close = triggered()
    now = time.time()
    playing = player is not None and player.poll() is None
    if playing:
        last_done = now
    if cfg.get("debug") and cfg["trigger"] == "distance" and now - last_debug > 0.5:
        last_debug = now
        print("distance mm:", round(sensor.distance * 1000), flush=True)
    if close:
        # A new visit fires straight away; someone who stays gets another roar repeat_s after the last one ends
        repeat = cfg.get("repeat_s", 0) > 0 and now - last_done > cfg["repeat_s"]
        if (armed or repeat) and not playing and now - last_fire > cfg["cooldown_s"]:
            last_fire = now
            fire()
            armed = False
        last_close = now
    elif now - last_close > cfg.get("clear_s", 0.2):
        # Re-arm only after nobody/no press for clear_s seconds, so a missed sensor reading doesn't count as leaving
        armed = True
    time.sleep(0.05)
