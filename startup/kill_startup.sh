echo "Shutting down active scripts"
for script in child_scripts/can.sh child_scripts/lte.sh child_scripts/cloudflare.sh child_scripts/profinity.sh child_scripts/gui.sh master_startup.sh child_scripts/database.sh child_scripts/gps.sh child_scripts/flask.sh child_scripts/pi_monitor.sh child_scripts/speed.sh; do
	PID=$(pgrep -f "$script")
	if [ -n "$PID" ]; then
		kill "$PID"
		echo "Killed $script (PID: $PID)"
	else
		echo "$script is not running"
	fi
done
