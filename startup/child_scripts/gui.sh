echo "GUI.sh"
source child_scripts/display.sh
is_display_on
source ../gui/venv/bin/activate
python3 ../gui/main.py
