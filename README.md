# ansible_retry_wrapper

## Example Usage:

### Command Prompt:
```
./try_ansible.py ansible-playbook playbook.yml -f 10
```

### Call from a python script
```
from try_ansible import try_ansible
try_ansible("ansible-playbook -f 10 playbook.yml")
```
