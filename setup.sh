# Create a new virtual environment
python3 -m venv venv
# Switch to virtual environment
. venv/bin/activate

# Install Python requirements
pip3 install -r requirements.txt

# Leave virtual environment
deactivate

sudo sed -e "s/{username}/${1}/g" bjucovid.service.template > /etc/systemd/system/bjucovid.service

sudo systemctl start bjucovid
sudo systemctl enable bjucovid

sudo systemctl status bjucovid