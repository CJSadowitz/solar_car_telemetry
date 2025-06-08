echo "CLOUDFLARE.sh::running flask-tunnel"
until nohup cloudflared tunnel run flask-tunnel; do
	echo "CLOUDFLARE.sh::failed to init cloudflare"
	sleep 10
done
echo "CLOUDFLARE.sh::success"
