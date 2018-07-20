<p align="center"><img src="https://user-images.githubusercontent.com/14370340/42978617-5260c1b2-8ba4-11e8-932b-89fe566cd730.png" width="350px"></p>

# Pingout

App to count pings(POST) on a defined url, identified by an uuid, and export the count and days of those pings as a csv file. I created to use it as a counter of continuous deploys per day.

## Set up

### Using docker
```
docker-compose up
```
Access the root url [http://localhost:5000](http://localhost:5000)

### Using virtual env
```
python3 -m venv path/to/your/env

source path/to/your/env/bin/activate

pip install -r requirements.txt
```
When you run with venv you have to initate a instance of MongoDB, which is needed for the app usage, by yourself. I recommend running the [docker image of mongo](https://hub.docker.com/_/mongo/).

After that run the server with:
```
./run.sh
```

## Running the tests

### Using docker

```
docker-compose up -d 

docker-compose exec web pytest tests
```

### Using virtual env
After the set up steps run:
```
pytest tests
```

## Usage
### 1. Create a Pingout
First you have to create a Pingout, which will be the identifier of your pings, each Pingout receives an unique UUID, you can create performing a **POST** on the url `/create-pingout`:  
```
curl -X POST http://localhost:5000/create-pingout 
```
The response of the post request will be your Pingout UUID, **SAVE IT**.
```json
{
  "uuid": "YOURUNIQUEUUID"
}
```
### 2. PING!
Once you have a created pingout you can ping on it whenever you want by performing a POST on the url `UUID/ping`:
```
curl -X POST http://localhost:5000/YOURUNIQUEUUID/ping 
```
When you ping, Pingout will save the date of that ping and increment the pings counter.

### 3. Export it
To export a CSV with your pings amount by date, first you have to query it using the date range you want by the params `initial_date` and `final_date` on the format **YYYY-MM-DD**:

1. Access the url:  
[http://localhost:5000/YOURUNIQUEUUID/?initial_date=2018-01-01&final_date=2018-02-02]()
  
2. After that you'll be redirect to a page to download the CSV file with the query result.

