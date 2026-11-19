#!/bin/bash
# Sets the grandMA2 details on a button Pi and restarts its code.
# Usage: ./set-ma.sh <pi name> <desk IP> <user> <password> "<command>"
# Example: ./set-ma.sh bs-rpi1 192.168.0.20 administrator secret "Toggle Exec 130"
set -e
[ $# -eq 5 ] || { echo 'Usage: ./set-ma.sh bs-rpi1 <desk IP> <user> <password> "<command>"'; exit 1; }
PI="pi@${1%.local}.local"
python3 - "$2" "$3" "$4" "$5" > /tmp/ma-update.json <<'PY'
import json, sys
print(json.dumps({"ma_ip": sys.argv[1], "ma_user": sys.argv[2], "ma_pass": sys.argv[3], "ma_command": sys.argv[4]}))
PY
scp -q /tmp/ma-update.json "$PI:/tmp/ma-update.json"
ssh "$PI" 'python3 - <<PY
import json
upd = json.load(open("/tmp/ma-update.json"))
for p in ["/home/pi/station/config.json"]:
    c = json.load(open(p)); c.update(upd); c["send_ma"] = True
    json.dump(c, open(p, "w"), indent=2)
print("Saved:", {k: v for k, v in upd.items() if k != "ma_pass"})
PY
rm /tmp/ma-update.json
pkill -u pi -f "[p]ython3 /home/pi/station/station.py"; sleep 4; systemctl is-active station'
rm /tmp/ma-update.json
