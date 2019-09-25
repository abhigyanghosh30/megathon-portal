# megathon-portal
Registration and submission portal for Megathon Onsite 2019

## Features:
- Support for participant and team registration
- Support for entry submission

## Get it up and running locally

*Prerequisites: You'll need a copy of `local_settings.py`, which happens to contain sensitive information.*

1. Clone the repository and navigate to its root
```(shell)
$ git clone https://github.com/IIIT-ECell/megathon-portal.git
$ cd path/to/repository/root
```

2. Setup and activate a virtual environment
```(shell)
$ python3 -m venv venv
$ source venv/bin/activate
```
 *(Run `$ deactivate` to deactivate the virtual environment when you are done.)*

3. Install required packages
```(shell)
$ pip3 install -r requirements.txt
```

4. Copy `local_settings.py` to the directory root, that is, on the same level as `manage.py`.
```(shell)
$ mv path/to/local_settings.py path/to/directory/root
```

5. The database and migrations are committed along with the code, so there is no need to migrate. This should be all. Test by running the development server.
```(shell)
$ python3 manage.py runserver
```

## Some things to take care of

- Make sure `local_settings.py`, your virtual environment files and pycache files are not pushed to GitHub.
- Make sure the database and the migrations stay in sync.
- Keep the database file small, do not add unnecessary records.
- Make sure you update requirements.txt after installing any new packages.
```(shell)
$ pip3 freeze > requirements.txt
```
