echo "GUI Script"
echo "Check display"
source child_scripts/display.sh
is_display_on
export DISPLAY=:0
echo "Init actual driver display here"

