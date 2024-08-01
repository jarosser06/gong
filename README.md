Gong SDK
--------

Small Gong SDK ... WIP as I need methods

API Docs: https://gong.app.gong.io/settings/api/documentation#overview


### Getting Started
Basic client usage example showing how to get a list of the last week worth of calls

```python
from datetime import datetime, timedelta, UTC

from gong import GongClient
from gong.calls import GongCallBaseFilter

# Initialize the client
base_url = 'https://<subdomain>.api.gong.io'

access_key = '<access key>'

access_key_secret = '<access key secret>'

gong = GongClient(
    base_url=base_url,
    access_key=access_key,
    access_key_secret=access_key_secret
)

# Get the current date
current_date = datetime.now(UTC)

# Get the start of the week
start_of_week = current_date - timedelta(days=7)

filter = GongCallBaseFilter(
    from_date_time=start_of_week,
    to_date_time=current_date,
)

print(gong.calls(filter))
```