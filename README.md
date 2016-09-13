# ansible_retry_wrapper

## Example Usage:

### Command Prompt:

Whatever play you were going to run just feeds straight into try_ansible:

```
./try_ansible.py ansible-playbook playbook.yml -f 10
```

Call with whatever options you need and it should behave.

### Call from a python script

Get try_ansible into your path.

```
from try_ansible import try_ansible
try_ansible("ansible-playbook -f 10 playbook.yml")
```
