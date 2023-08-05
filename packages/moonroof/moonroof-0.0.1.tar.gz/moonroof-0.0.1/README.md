# Moonroof Django Client Library

Coming soon... this is not production ready!

Visit `https://moonroof.io/get-started` to get an API Key

## Install & Setup

Download the package

```
pip install moonroof
```

and update Django settings

```
MIDDLEWARE = [
  ...,
  'moonroof.MoonroofMiddleware',
  ...
]

MOONROOF_API_KEY = '<Your API Key Here>'
```

## TODO

- Add logging
- More detailed profile information where possible (without significantly slowing down API response time!)
  - Which models are involved
  - Serializer time (DRF)
  - View time
  - Library code vs your code
- Look into `[Errno 54] Connection reset by peer`
