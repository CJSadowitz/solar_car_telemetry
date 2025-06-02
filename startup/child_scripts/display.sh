check_display() {
	if [[ -n "$DISPLAY" ]] && xrandr >/dev/null 2>&1; then
		echo "Display on"
		return 0
	else
		echo "Display off"
		return 1
	fi
}
is_display_on() {
	while true; do
		check_display
		if [ $? -eq 0 ]; then
			sleep 5 # Allow display to fully boot
			break
		fi
		sleep 5
	done
}
