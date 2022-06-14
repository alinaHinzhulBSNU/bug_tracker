# ML-based bug tracker application

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/alinaHinzhulBSNU/bug_tracker.git
$ cd bug_tracker
````

Install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
$ cd bug_tracker
$ python manage.py migrate
$ python manage.py makemigrations
$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
