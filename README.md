git clone https://github.com/juengerj/bumble-fodder.git
cd bumble-fodder/
virtualenv venv -p $(which python3)
source venv/bin/activate
pip install -r requirements.txt
python app.py
Browse to flipx.engr.oregonstate.edu:5000/ to view (x is the flip server you run 'python app.py' from)
