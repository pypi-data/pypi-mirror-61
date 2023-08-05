# Discogspy
> Discogspy is a  type-safe and easy to use python wrapper around the Discogs API.


## General information

<br>

What's the use case for discogspy?

<br>
I have a small label/distro, and I sell my items via Discogs and my own website. To keep both stores in sync is tidies. That's why I want to automate this process. Therefore I need to be able to get information from my Discogs store. That can be done via the official Discogs python client. However, I also need to be able to update orders, add and remove items etc. and this doesn't seem to work via the Discogs python client. That's why I decided to wrap the Discogs API myself. 
<br><br><br>
Important information:
<br>
Requests to the Discogs API are throttled by the server by source IP to 60 per minute for authenticated requests, and 25 per minute for unauthenticated requests, with some exceptions.



## Install

`pip install discogspy`


## Road Map

1. Create type save python wrapper around the Discogs API
    
    a) Wrap database calls (done - except search request cause I personally dont have any use case for it)<br>
    b) Wrap marketplace calls (done)<br>
    c) Wrap inventory export calls (done)<br>
    d) Wrap inventory upload calls (done)<br>
    e) Wrap user identity calls (maybe later - I personally dont have any use case for it)<br>
    f) Wrap user collection calls (done)<br>
    g) Wrap user wantlist calls (done)<br>
    h) Wrap user lists calls<br>

2. Create response wrapper

## How to use

For a detailed explanation and more examples, please visit the [documentation](https://cpow-89.github.io/discogspy/).

Currently, you have two options for starting requests to Discogs.

1. Create a user object without authentication. This will limit your options cause a lot of API calls do require authentication.

```python
from discogspy.core.discogs_user import UserWithoutAuthentication
from discogspy.core import rq_database

user = UserWithoutAuthentication()
resp = rq_database.get_release(user, 1972502)
```

2. Create a user object with user token authentication. This will allow you to send any request.

```python
from discogspy.core.discogs_user import UserWithUserTokenBasedAuthentication
from discogspy.core import rq_database

user_with_authentication = UserWithUserTokenBasedAuthentication(user_token="your_user_token",
                                                                user_agent="your_user_agent")
resp = rq_database.get_release(user, 1972502)
```
