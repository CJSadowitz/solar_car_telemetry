echo "DATABASE.sh::running"
source ../postgres_init/venv/bin/activate
python3 ../postgres_init/main.py
echo "DATABASE.sh::finished"

