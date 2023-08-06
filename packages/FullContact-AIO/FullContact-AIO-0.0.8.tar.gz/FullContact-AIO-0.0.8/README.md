FullContact.py
==============

[![PyPI version](https://badge.fury.io/py/FullContact-AIO.svg)](https://badge.fury.io/py/FullContact-AIO)
[![Build Status](https://api.travis-ci.org/fullcontact/fullcontact.py.svg?branch=master)](https://travis-ci.org/fullcontact/fullcontact.py)

A Python interface for the [FullContact API](http://docs.fullcontact.com/).

Installation
------------

```
pip install FullContact-AIO
```

Usage
-----


```python

import asyncio

from fullcontact_aio import FullContact


async def get_person_by_email():
    fc = FullContact('xgtbJvVos2xcFMX1JvXaQvx0ZaExhSCT')

    #returns a python dictionary
    r = await fc.person(email='you@email.com')
    
    # The number of requests left in the 60-second window.
    rate_limit_remaining = r['X-Rate-Limit-Remaining']
    
    
    print(r) # {u'socialProfiles': [...], u'demographics': {...}, ... } 

    print(rate_limit_remaining) 

asyncio.get_event_loop().run_until_complete(get_person_by_email())
```


Supported Python Versions
-------------------------
* 3.6
* 3.7
* 3.8
* 3.9


Official Documentation
-------------------------
https://dashboard.fullcontact.com/api-ref