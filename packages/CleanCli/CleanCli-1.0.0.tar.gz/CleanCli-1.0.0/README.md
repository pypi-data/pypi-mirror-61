## Get Started:

To make a cli Create a class Child of Cli class.

To create a comand or parameters their names must be being with "cmd_"


### Cli Exemple

```python
# MyCli.py
from Cli import Cli


class MyCli(Cli):
    def __init__(self):
        Cli.__init__(self)
        self.cmd_version = "1.0"
    
    def cmd_first(self, arg, list_args:list, **kwargs):
        print('Argument provided value', arg)
        print("List of all args: ", list_args)
        print("other parameters provided: ", kwargs)



MyCli().listen_os(another="Another parameter")

```

```
$ python3 MyCli.py -version
1.0
```

```
$ python3 MyCli.py -first
Argument provided value True
List of all args:  {'-first': True}
anothers parameterers provided:  {'another': 'Another param'}
```


NOTE: All "-" are replaced to "_" on function name:
```python
cmd_v = "-v"
cmd__version = "--version"

```