# python-autoviv [![PyPi](https://img.shields.io/badge/python-2.7%20%7C%203.4%20%7C%203.5%20%7C%203.6%20%7C%203.7%20%7C%203.8-%2344CC11)](https://pypi.org/project/python-autoviv/) [![PyPiStats](https://img.shields.io/pypi/dm/python-autoviv.svg)](https://pypistats.org/packages/python-autoviv)

The Autovivification library for Python

## Installation

Add this line to your application's requirements.txt:

```python
python-autoviv
```

And then execute:

    $ pip install -r requirements.txt

Or install it yourself as:

    $ pip install python-autoviv

## Usage

Import autoviv and call parse on any list, dict, or primitive. You can also call loads on serialized JSON

```python
>>> import autoviv
>>> import requests
>>> r = requests.get('http://jsonplaceholder.typicode.com/users')
>>> users = autoviv.parse(r.json())
>>> # or
... users = autoviv.loads(r.text)
>>> for user in users:
...     print(user.name)
...
Leanne Graham
Ervin Howell
Clementine Bauch
Patricia Lebsack
Chelsey Dietrich
Mrs. Dennis Schulist
Kurtis Weissnat
Nicholas Runolfsdottir V
Glenna Reichert
Clementina DuBuque
>>> user = users[0]
>>> print(autoviv.pprint(user, indent=4))
{
    "username": "Bret",
    "website": "hildegard.org",
    "name": "Leanne Graham",
    "company": {
        "bs": "harness real-time e-markets",
        "name": "Romaguera-Crona",
        "catchPhrase": "Multi-layered client-server neural-net"
    },
    "id": 1,
    "phone": "1-770-736-8031 x56442",
    "address": {
        "suite": "Apt. 556",
        "street": "Kulas Light",
        "geo": {
            "lat": "-37.3159",
            "lng": "81.1496"
        },
        "zipcode": "92998-3874",
        "city": "Gwenborough"
    },
    "email": "Sincere@april.biz"
}
>>> user.name = 'auto-vivification'
>>> r = requests.put('http://jsonplaceholder.typicode.com/users/{0}'.format(user.id), json=user)
>>> response = autoviv.parse(r.json())
>>> print(response.name)
auto-vivification
>>> new = autoviv.parse({})
>>> new.id = 5
>>> if not new.username:
...     new.username = 'New User'
...
>>> new.address.geo.lat = "-42.3433"
>>> new.address.geo.lng = "74.3433"
>>> new.email = 'someone@somewhere.biz'
>>> print(autoviv.pprint(new))
{
    "username": "New User",
    "email": "someone@somewhere.biz",
    "id": 5,
    "address": {
        "geo": {
            "lat": "-42.3433",
            "lng": "74.3433"
        }
    }
}
```
### NoneProp
It should be noted that missing referenced properties, including nested, are gracefully falsey.

```python
>>> import autoviv
>>> data = autoviv.parse({})
>>> data.property.is_none

>>> bool(data.property.is_none)
False
>>> isinstance(data.property.is_none, autoviv.NoneProp)
True
>>> 'some data' in data.property.is_none
False
>>> [x for x in data.property.is_none]
[]
>>> data.property.is_none = None
>>> isinstance(data.property.is_none, autoviv.NoneProp)
False
>>> print(autoviv.pprint(data))
{
    "property": {
        "is_none": null
    }
}
```

## Testing
Install test dependencies with pipenv.

    $ pip install pipenv
    $ pipenv install -d
    $ ./test.sh

## Contributing

Bug reports and pull requests are welcome on GitLab at https://gitlab.com/tysonholub/python-autoviv.git. This project is
intended to be a safe, welcoming space for collaboration, and contributors are expected to adhere to the
[Contributor Covenant](http://contributor-covenant.org) code of conduct.


## License

This package is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
