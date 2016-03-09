cd 
git clone https://github.com/florenceloi/hackbright-project.git
cd hackbright-project
git pull
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python server.py