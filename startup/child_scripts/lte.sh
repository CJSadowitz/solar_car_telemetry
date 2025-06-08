echo "LTE.sh::starting"
while true; do
	OUTPUT=$(/usr/local/bin/atcom AT#ECM=1,0)
	if [[ "$OUTPUT" == *"OK"* ]]; then
		echo "LTE.sh::successfully connected to lte"
		break
	fi
	echo "LTE.sh::failed to init lte hat; $OUTPUT"
	sleep 5
done
echo "LTE.sh::success"
