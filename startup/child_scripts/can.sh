source child_scripts/can_util.sh
echo "Attempting to initialize can network"
set_up_can
source ../can/venv/bin/activate
python3 ../can/main.py
