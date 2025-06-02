function set_up_can() {
	while true; do
		sudo ip link set can0 up type can bitrate 500000
		if [ $? -eq 0 ]; then
			echo "Successfully initialized CAN network"
			break
		fi
		sleep 5
	done
}
