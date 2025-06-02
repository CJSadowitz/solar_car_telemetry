echo "Master Script"
date
echo "Calling Child Scripts"
bash child_scripts/database.sh
bash child_scripts/can.sh &
bash child_scripts/lte.sh &
bash child_scripts/cloudflare.sh &
bash child_scripts/profinity.sh &
wait
bash child_scripts/gui.sh
