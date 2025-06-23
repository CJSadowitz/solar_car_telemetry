echo "Master Script"
date
echo "Calling Child Scripts"
cd "$(dirname "$0")"
bash child_scripts/database.sh
# bash child_scripts/can.sh &
bash child_scripts/lte.sh &
# bash child_scripts/gps.sh &
# bash child_scripts/pi_monitor.sh &
bash child_scripts/cloudflare.sh &
bash child_scripts/flask.sh &
# bash child_scripts/profinity.sh &
# bash child_scripts/gui.sh &
