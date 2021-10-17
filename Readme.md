# imdb-task
RESTful API for movies, something similar to IMDB

# Stack Used
FastAPI
Sqlite3


# API Testing

Deployed at http://52.91.45.18:8000/

<br>
OpenAPI is available at 
    
    http://52.91.45.18:8000/docs#/

### Steps to test

1. Create an Admin user
    `http://52.91.45.18:8000/docs#/default/create_admin_admin__post`

    SUPERUSER_PASSWORD for `52.91.45.18` is `my_passw0rd`
    (change it in `config.py` if you want to)

    Should bring you a Bearer access_token on successful creation

2. Login as the admin user with the Bearer Token you received

    In `http://52.91.45.18:8000/docs#/` on right-top there is an authorize button. You may use this also for ease.

    Alternatively login at `http://52.91.45.18:8000/docs#/default/login_for_access_token_token_post` with username and password.

3. Upload your movies as a json file in

    `http://52.91.45.18:8000/docs#/default/upload_movies_in_bulk_upload__post`
    
    Given data already uploaded.
    Only Admins can access this API

4. Create, Update, Delete APIs for movies.

    You could find CRUD API's on endpoint `/movie/`.
    Access Limited to Admins only.

5. Users can signup from
    `http://52.91.45.18:8000/docs#/default/signup_signup__post`

6. Search Movies at
    `http://52.91.45.18:8000/docs#/default/search_movies__get` 
    
    (something like `http://52.91.45.18:8000/?search=oz`)

    Using the `search` query_param, we can search for movie name, genre and director name as well.

    Can be accessed by authenticated users and admins.


# Setting up

### Create virtual environment and activate it
```bash
sudo apt install python3-venv #for debian based systems
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run it using any asynchronus web server

Example using `uvicorn`

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Answer to the Scalability problem in 

[scalability.md](https://github.com/balumn/imdb-fastapi/blob/develop/scalablility.md)