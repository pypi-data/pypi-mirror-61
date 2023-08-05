# Simple heartbeat library
This is designed to work with the 
[simple heartbeat app](https://github.com/joshcoales/simple-heartbeat-app) to send heartbeat status 
notifications to the server, and ignore errors and such.

## Usage
1. Get a copy of the [simple heartbeat library from pypi](https://pypi.org/project/simple-heartbeat/).
2. Spin up a copy of the heartbeat server, and then set `heartbeat.heartbeat_app_url` to the URL of
your heartbeat server.  
3. Optional: Call `heartbeat.initialise_app(app_name, expiry_period)` to initialise your app in the heartbeat server.
   - This is mostly useful for initialising an expiry period for the app. If it fails to contact the heartbeat server, it will propogate the exception up.
4. Periodically call `heartbeat.update_heartbeat(app_name)` to confirm your application is online.
