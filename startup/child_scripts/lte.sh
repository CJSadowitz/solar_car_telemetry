echo "LTE Script"
echo "Setting up LTE hat"
while true; do
	OUTPUT=$(atcom AT#ECM=1,0)
	if [[ "$OUTPUT" == *"OK"* ]]; then
		echo "Successfully connected to LTE"
		break
	fi
	echo "Failed to init lte hat; $OUTPUT"
	sleep 5
done
