# Python Wrapper for the MClimate API

### How to use

```
pip install py-mclimate-api

```

```
python >>> from mclimate import Mclimate >>> m = Mclimate(username="email_adress", password="password") >>> m.fetch_devices() {'********': {'user_id': 1, 'serial_number': '********', 'mac': '********', 'firmware_version': 'V1SHTHF', 'name': 'Melissa ********', 'type': 'melissa', 'room_id': None, 'created': '2016-07-06 18:59:46', 'id': 1, 'online': True, 'brand_id': 1, 'controller_log': {'temp': 25.4, 'created': '2018-01-06T10:12:16.249Z', 'raw_temperature': 28188, 'humidity': 18.5, 'raw_humidity': 12862}, '_links': {'self': {'href': '/v1/controllers'}}}}

python >>> from mclimate import Mclimate >>>  m = Mclimate(username="email_adress", password="password") >>> m.send("DEVICE_ID", "DEVICE_TYPE", {"state": "on"})

```

## Built With

* [requests](http://docs.python-requests.org/en/master/)

## License

Licensed under the MIT License - see this [LICENSE.md](LICENSE.md)
