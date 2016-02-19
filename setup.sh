cd ~/src/florence/
git clone https://github.com/florenceloi/hackbright-project.git
cd hackbright-project
git pull
virtualenv env
source env/bin/activate
pip install -r requirements.txt
dropdb r
createdb r
python seed.py
python server.py