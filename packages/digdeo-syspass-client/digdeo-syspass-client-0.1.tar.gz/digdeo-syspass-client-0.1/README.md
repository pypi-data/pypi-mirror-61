# digdeo-syspass-client

Python API Client for SysPass server (https://www.syspass.org/en)

### Implemented API
Both 100% Cover and 100% UnitTested
* 3.0: https://syspass-doc.readthedocs.io/en/3.0/
* 3.1: https://syspass-doc.readthedocs.io/en/3.1/

### Notes:

The API Client require settings like the server and token ;)

It have 2 ways. by ENV Vars , or by a config.yml file.

````
$HOME/.config/digdeo-syspass-client/config.yml
````
or
````
$DD_SYSPASS_CLIENT_CONFIG_DIR/config.yml
````
### Config file

```
syspassclient:
  api_url: 'https://you.server.exemple.com/api.php'
  api_version: '3.1'
  authToken: '######################################################'
  tokenPass: '######################################################'
  debug: False
  debug_level: 0
  verbose: False
  verbose_level: 0
```

### Tips

* If you would like to change token on fly, you'll have to play with **$DD_SYSPASS_CLIENT_CONFIG_DIR** and a subdirectory structure.

---
DigDeo FLOSS Team - 2020