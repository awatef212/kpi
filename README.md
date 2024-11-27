# kpi-refacfto/backend

## Run Locally

Install [MySQL](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04-fr)

Install [Python 11.3](https://www.python.org/downloads/)

Clone the project

```bash
git clone git@github.com:awatefAPlusA/kpi-refacfto.git
```

Go to the project directory

```bash
cd backend
```

Create virtual environnement

```bash
virtualenv venv -p  /usr/bin/python3.11
```

Start the virtual environnement

```bash
source venv/bin/activate
```

Install the dependances
```bash
pip install -r requirements.txt
```

Set up the env file and Config the .env file 

```bash
cp ./backend/.env.example ./backend/.env
```

Start the server 

```bash
python -m gunicorn -c gunicorn_config.py app:app --reload
```

Go to the frontend Folder

```bash
cd ../frontend
```

Install the dependances

```bash
npm i
```

Start the server 

```bash
npm run serve
```

Go to [The Web site](http://localhost:8080/)


## Run with Docker
Install [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)

Install [Docker-Compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04)

Clone the project

```bash
git clone git@github.com:awatefAPlusA/kpi-refacfto.git
```

Set up the env file and Config the .env.docker file 

```bash
cp ./backend/.env.example ./backend/.env.docker
```

Run the Project 
```bash
docker-compose up --build
```
