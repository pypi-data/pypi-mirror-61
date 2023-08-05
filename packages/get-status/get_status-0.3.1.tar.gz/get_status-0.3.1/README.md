# Get_Status

## How to use ?

it's very easy:

```python
import get_status as get

url = "https://www.google.com"

brave = "Brave/1.0 (Windows NT x.y; rv:10.0)"

status = get.status(url, user_agent=brave)

print(status)

>>> 200
```

``get_status`` has 2 arguments :

#### - url :

  Basic url (with http(s)://)

  Ex : ~~google.com~~ / http://www.google.com / https://google.com / ~~http://www.ThisIsA404.error~~

#### - user_agent (optional, default: Auto):

  could be:

    None : No user-agent

    auto (default): Send automaticaly a Firefox user-agent)

    custom : Send directly you'r custom user agent:

  Ex: ~~None~~ / "None" / "auto" / ~~"firefox"~~ / "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
