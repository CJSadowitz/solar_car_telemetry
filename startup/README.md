# Startup Script
The following code is intended to run on a raspberry pi for fpu's solar car team
## Hardware Setup
- LTE Hat (some brand)
- PCAN adapter (some brand)
- Any Screen
## Installation
```bash
git clone  https://github.com/CJSadowitz/solar_car_startup.git
```
## Run on startup
Some funny commands that I need to find
## Other util
All relevant scripts git ran automatically throug the line:
```bash
bash master_startup.sh
```
If there are errors or something has gotten disconnected run
```bash
bash kill_startup.sh
```
to ensure shutdown of all running scripts for setup
## Notes
These scripts will call other code from other repositories to set up the GUI for example <br>
## TODO
- Prohelion Script
- GPS Script
- Cloudflare Script
