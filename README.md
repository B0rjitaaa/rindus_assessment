Rindus Hiring Challenge
=====================================
## Set up
1. Run `docker-compose up` to create and deploy needed containers.
2. Run `docker exec -it rindus_assessment-web-1 /bin/bash` to create an interactive shell with the running container.


## Migrations
1. Run `python manage.py migrate`
2. Assumption taken: As the assessment says we are not creating any User model, I decided to use the one provided by Django. For that reason, we need to create at least one dummy user. Run `python manage.py shell` to open an interactive shell and then:
```
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='username',
    email='email@test.com',
    password='password'
)
```


## Commands
1. Run `python manage.py import_data`
2. If we want to check if everything went ok, we just need to connect to a new shell using `python manage.py shell`
```
>>> from rindus_assessment_app.models import *
>>> Post.objects.all().count()
100
>>>
```
3. Assumption taken: As the assessment says, "The user_id for the new posts created is always 99999942 since we don’t implement the user model." I decided to import the ones coming from the web using a null as a user_id. Then, when a user is creating new posts, that user_id will be 99999942.


## Tests
1. A set of tests have been provided to determine the expected behavior of this system.
Run `python manage.py test`


## Synchronization
As I have not received further clarification on some questions I had sent in an email last Thursday regarding this point, I have decided to set this item on-hold from now and discuss it during the next meeting because I don't want to make any wrong assumptions.

The reason for this is that  there is a wide array of options of how to address this problem, one option that I see possible would be the following one:

### Automated Synchronization
The synchronization process can also be automated by scheduling the synchronization command to run at regular intervals using a task scheduler such as cron, django-crontab, or django-celery.

Ensure that the scheduler is configured to execute the synchronization command (import_data) at the desired interval.


I hope to discuss any other option or further assumptions during the meeting.