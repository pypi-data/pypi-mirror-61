# Sixgill Clients

This module provides simple clients for two of Sixgill’s APIs:
- Sixgill Feed (IOC) Client
- Sixgill Alerts Client 

# Sixgill Feed Client Arguments
1. client_id        (Mandatory) - Your client id obtained by Sixgill’s portal, 
2. client_secret    (Mandatory) - Your client secret obtained by Sixgill’s portal, 
3. channel_id       (Mandatory) - Supported Sixgill channel id. If you don't have such a channel id please contact Sixgill's support (support@cybersixgill.com).
4. feed_stream      (Mandatory) - One of the feed streams supported by Sixgill. 
5. logger           (Optional)  - Logger.
6. bulk_size        (Optional)  - requests bulk size, default 1000 items. 
7. session          (Optional)  - Session object which manage and persist settings across requests (cookies, auth, proxies) default=requests.Session().

# Supported Feed Streams
1. DARKFEED
2. DARKFEED_FREEMIUM

# Supported Functions

### get_bundle(self) -> Dict[str, Any]
- Returns a Bundle - A collection of arbitrary STIX v2.0 Objects  
```
{
'id': 'bundle--bcbb94ea-2d3a-43f1-8c1a-62002594d2ba',
'objects': [{<STIX Domain Object, STIX Relationship Object, Marking Definition>}],
'spec_version': '2.0', 
'type': 'bundle'
}
```

### get_indicator(self)
- Returns a generator of STIX v2.0 items, while auto committing items that are read

### commit_indicators(self)
- Commit on bundle. 
- Ack server and notify indicators were received.
- As long as the server doesn't receive an Ack, the same items on each get_bundle() function call will be retrieved.

## Quick Example
```
from sixgill.sixgill_darkfeed_client import SixgillFeedClient
from sixgill.sixgill_constants import FeedStream

CLIENT_ID = "<Replace with your client id>"
CLIENT_SECRET = "<Replace with your client secret>"
CHANNEL_ID = "<Replace with channel id>"

sixgill_darkfeed_client = SixgillFeedClient(CLIENT_ID, CLIENT_SECRET, CHANNEL_ID, FeedStream.DARKFEED)

for indicator in sixgill_darkfeed_client.get_indicator():
    print(indicator)
    
```

# Sixgill Alert Client Arguments
1. client_id        (Mandatory) - Your client id obtained by Sixgill’s portal, 
2. client_secret    (Mandatory) - Your client secret obtained by Sixgill’s portal, 
3. channel_id       (Mandatory) - Supported Sixgill channel id. If you don't have such a channel id please contact Sixgill's support (support@cybersixgill.com). 
4. logger           (Optional)  - Logger.
5. bulk_size        (Optional)  - requests bulk size, default 1000 items. 
6. session          (Optional)  - Session object which manage and persist settings across requests (cookies, auth, proxies) default=requests.Session().


# Supported Functions

### get_alerts_bulk(self, include_delivered_items: bool = True, sort_by: str = None, sort_order: str = None, is_read: str = None, severity: str = None, threat_level: str = None, threat_type: str = None) -> List[Dict[str, Any]]
- params:
    - include_delivered_items (Optional) - Should previously-delivered items be included in the response,               Default False.
    - sort_by                 (Optional) - One of the following [date, alert_name, severity, threat_level].             Default date.
    - sort_order              (Optional) - One of the following [asc, desc].                                            Default desc.
    - is_read                 (Optional) - Filter alerts that were read \ unread. One of the following[read, unread].   Default None.
    - severity                (Optional) - Filter by alert severity. One of the following[low, med, high].              Default None.
    - threat_level            (Optional) - Filter by alert threat level. One of the following[imminent, emerging].      Default None.
    - threat_type             (Optional) - Filter by field threat type.                                                 Default None.

- Returns a list of Sixgill alerts 


### get_alert(self, sort_by: str = None, sort_order: str = None, is_read: str = None, severity: str = None, threat_level: str = None, threat_type: str = None)
- params:
    - sort_by                 (Optional) - One of the following [date, alert_name, severity, threat_level].             Default date.
    - sort_order              (Optional) - One of the following [asc, desc].                                            Default desc.
    - is_read                 (Optional) - Filter alerts that were read \ unread. One of the following[read, unread].   Default None.
    - severity                (Optional) - Filter by alert severity. One of the following[low, med, high].              Default None.
    - threat_level            (Optional) - Filter by alert threat level. One of the following[imminent, emerging].      Default None.
    - threat_type             (Optional) - Filter by field threat type.                                                 Default None.

- Returns generator of Sixgill alerts, while auto committing on every bulk of ids

### mark_digested_item(self, item)
- Mark an alert as consumed by storing alert id

### commit_digested_items(self, force: bool = False)
- Mark a bulk of ids as consumed on Sixgill's servers
- This command is called automatically when using get_alert
  
## Quick Example
```
from sixgill.sixgill_alert_client import SixgillAlertClient
 
CLIENT_ID = "<Replace with your client id>"
CLIENT_SECRET = "<Replace with your client secret>"
CHANNEL_ID = "<Replace with channel id>"

sixgill_alert_client = SixgillAlertClient(CLIENT_ID, CLIENT_SECRET, CHANNEL_ID)

for alert in sixgill_alert_client.get_alert():
    sixgill_alert_client.mark_digested_item(alert)
    print(alert)
    
```