#!/bin/bash
# Sets up one Raspberry Pi over SSH from the Mac.
# Usage: ./setup-pi.sh <set> [hostname]   <set> is lion, button or spare; hostname defaults to bs-<set>
# Needs: the Pi on the same network as the Mac, user "pi", the Mac's SSH key added in Raspberry Pi Imager.
set -e
export LC_ALL=C.UTF-8 LC_CTYPE=C.UTF-8
cd "$(dirname "$0")"
SET="$1"
case "$SET" in
  lion)   CFG=config-1-lion.json ;;
  button) CFG=config-2-button.json ;;
  spare)  CFG=config-3-spare.json ;;
  *) echo "Usage: $0 lion|button|spare [hostname]"; exit 1 ;;
esac
NAME="${2:-bs-$SET}"
HOST="pi@${NAME%.local}.local"

echo "== Copying files to $HOST"
ssh -o StrictHostKeyChecking=accept-new "$HOST" "mkdir -p ~/station"
scp station.py station.service "$HOST:~/station/"
scp "$CFG" "$HOST:~/station/config.json"
# Only the lion plays a sound
[ "$SET" = lion ] && for f in *.mp3; do [ -e "$f" ] && scp "$f" "$HOST:~/station/"; done

echo "== Installing packages and starting the service"
ssh -t "$HOST" 'set -e
sudo apt-get update -qq
sudo apt-get install -y -qq mpg123 python3-gpiozero python3-lgpio alsa-utils
sudo timedatectl set-timezone Australia/Perth
# Sound goes to the 3.5 mm jack: station.py names the device (audio_device in config.json)
sudo rm -f /etc/asound.conf
amixer -q -c Headphones sset PCM 90% 2>/dev/null || true
sudo cp ~/station/station.service /etc/systemd/system/station.service
sudo systemctl daemon-reload
sudo systemctl enable --now station
sleep 2
systemctl --no-pager --lines=5 status station'
echo "== Done. Watch it live with: ssh $HOST journalctl -u station -f"
