cd ~/Desktop/nord
echo "auth-user-pass pass.txt" >> us15.nordvpn.com.tcp443.ovpn
sudo openvpn --config us15.nordvpn.com.tcp443.ovpn
