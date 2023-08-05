# Discogspy
> Discogspy is a  type-safe and easy to use python wrapper around the Discogs API.


Important: This package is under substantial development. See Road Map for more information.

## Install

`pip install discogspy`


## Road Map

1. Create type save python wrapper around the Discogs API
    
    a) Wrap database calls (done - except search request cause I personally dont have any use case for it)<br>
    b) Wrap marketplace calls (done)<br>
    c) Wrap inventory export calls (done)<br>
    d) Wrap inventory upload calls (done)<br>
    e) Wrap user identity calls (maybe later - I personally dont have any use case for it)<br>
    f) Wrap user collection calls<br>
    g) Wrap user wantlist calls<br>
    h) Wrap user lists calls<br>

2. Create response wrapper

## How to use

For detailed explanation please visit the [documentation](https://cpow-89.github.io/discogspy/).

Currently, you have two options for starting requests to Discogs.

1. Create a user object without authentication. This will limit your options cause a lot of api calls require authentication.

```
from discogspy.core.discogs_user import UserWithoutAuthentication
from discogspy.core import rq_database

user = UserWithoutAuthentication()
resp = rq_database.get_release(user, 1972502)
```

2. Create a user object with user token authentication. This will allow you to send any request.

```
from discogspy.core.discogs_user import UserWithUserTokenBasedAuthentication
from discogspy.core import rq_database

user_with_authentication = UserWithUserTokenBasedAuthentication(user_token="your_user_token",
                                                                user_agent="your_user_agent")
resp = rq_database.get_release(user, 1972502)
```
