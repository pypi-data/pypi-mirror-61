# EM client

# Install
    Install using `pip`...
    
        pip install eventmonitoring-client
        
# Usage
```python
# setting.py
from event_monitoring import EMConfig
EMConfig(
    SYSTEM_EVENT_TOKEN='<token>',
    SYSTEM_EVENT_URL='<url>',
    SYSTEM_EVENT_NAME='<name>',
    em_notify=True, # if wanna telegram notification else False
    debug=True # True or False
)   

# your logic
from event_monitoring import event, run, log_exception, list_value_event

# decoration you function
@list_value_event(keys=['integration_id', 'cred_login'], list_value="task_list", iter_key='key') # in new version
def test(task_list: list, key: int):
    ...

@event(keys='cred_id') # for not list value function
def check_data(cred_id: int):
    ...

# if u wanna log exceptions to server
try:
    ...
except Exception as e:
    name = create_event_name(['integration_id', 'cred_login'], task_list, key)
    log_exception(name, str(e))
```

### Changes
in new version base event split for two decorators event and list_value_event