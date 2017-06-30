cd ~/Desktop/nord/OVPN
rm *.ovpn
rm zip*
wget https://nordvpn.com/api/files/zip
unzip zip
cd ..
#echo "auth-user-pass pass.txt" >> us580.nordvpn.com.tcp443.ovpn
#sudo openvpn --config us580.nordvpn.com.tcp443.ovpn
