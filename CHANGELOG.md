# Change Log

All notable changes to this project will be documented in this file.

# 0.1.1

* Fix payload handling in `__subs_cb` and `__subscribe_resp` (mqtt_client.py)
* Refactor how optional client methods are handled
* Fix `alive_check` method by passing client
* Add standard sensor reading topic format (Updated README)

# 0.1.2

* Update [`mqtt_as.py`](https://github.com/peterhinch/micropython-mqtt/tree/master/mqtt_as) file 
* Refactor so base wiring for LED is not required (expose events so it can be done if chosen)
* Add `debug` property for `config.json` that determines logging output
* Move `config.json` reader to `main.py` so `boot.py` is freed up for optional use
* Put non-terminating code after network connection is established in `mqtt_client.py`
* Clean up unnecessary code/files

# 0.1.3

* Remove boot.py so it can be dropped in by user