# TripSpark - Catalog API
-----------

(Local)


### 1. Install dependencies by running:
  pip install -r requirements.txt

### 2. Run main.py
  python3 main3.py

### 3. In the web go to /docs and try out GET catalogs to check MySQL connectivity

(GCP VM)

## This microservice has been deployed in GCP VM

**Project name** - Cloud Computing TripSpark

**VM instance** - catalog

<img width="1178" height="417" alt="image" src="https://github.com/user-attachments/assets/495fd0d6-f509-4213-a9e3-442960a5de40" />


### 1. Go to SSH and run:

    cd TripSpark-catalog
    
    git pull
    
    source venv/bin/activate
    
    python3 -m uvicorn main3:app --host 0.0.0.0 --port 8000 #run main3.py

### 2. In the web go to http://<EXTERNAL_IP of catalog VM>:8000/docs#/ and try out all the APIs to check MySQL connectivity

<img width="1468" height="893" alt="catalog" src="https://github.com/user-attachments/assets/cd8f3e78-bafc-4d19-81f9-684ecb080b1d" />

Watch Demo - https://www.youtube.com/watch?v=DaznV2TLKHs


