cloudflared tunnel login
echo "LOGGED ON"
cloudflared tunnel delete flask-tunnel
cloudflared tunnel create flask-tunnel
echo "Created Flask Tunnel"
cloudflared tunnel route dns flask-tunnel server.deoliveira.tech
echo "Route through pi.deoliveira.tech"
cloudflared tunnel run flask-tunnel --url http://localhost:5000
echo "Running flask-tunnel on localhost:5000"
