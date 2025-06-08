source child_scripts/can_util.sh
echo "CAN.sh::running"
set_up_can
source ../can/venv/bin/activate
python3 ../can/main.py
echo "CAN.sh::failed"
