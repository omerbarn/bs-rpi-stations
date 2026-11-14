#!/usr/bin/env python3
# Balloon Story activation station: a button or a hand sensor plays an mp3
# and/or sends a UDP message to the venue light/sound system.
import json, socket, subprocess, sys, time

cfg = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "/home/pi/station/config.json"))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def fire():
    print("Triggered", flush=True)
    if cfg["play_sound"]:
        subprocess.Popen(["mpg123", "-q", "-o", "alsa", "-a", cfg.get("audio_device", "default"), cfg["mp3_file"]])
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
    sensor = DistanceSensor(echo=cfg["echo_gpio"], trigger=cfg["trigger_gpio"], max_distance=2)
    def triggered():
        return sensor.distance * 1000 < cfg["distance_mm"]  # .distance is in metres

last_fire = 0
was_triggered = False
while True:
    now_triggered = triggered()
    # Fire only on a new press or a new hand, and not during the cooldown
    if now_triggered and not was_triggered and time.time() - last_fire > cfg["cooldown_s"]:
        last_fire = time.time()
        fire()
    was_triggered = now_triggered
    time.sleep(0.05)
