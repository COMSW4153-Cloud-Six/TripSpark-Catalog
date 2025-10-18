# TripSpark - Catalog API
-----------

(Local)


### 1. Install dependencies by running:
  pip install -r requirements.txt

### 2. Run main.py
  python3 main.py

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
    
    python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 #run main.py

### 2. In the web go to http://34.139.65.200:8000/docs#/ and try out all the APIs to check MySQL connectivity

<img width="1461" height="747" alt="image" src="https://github.com/user-attachments/assets/04756de6-799f-4fd5-9a74-aeb64502947a" />

Watch Demo - https://www.youtube.com/watch?v=DaznV2TLKHs


