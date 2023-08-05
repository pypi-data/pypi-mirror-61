**ctrl-v** is a markdown code snippet store written in Python using the Flask framework.  Store your code snippets that you always keep missing!

### Installation
Use the following command to install ctrl-v from [PyPI][1] 

    $ pip install ctrl-v

### Launch ctrl-v

After installing ctrl-v you can launch the application from your terminal / command line. 

    $ ctrl-v
    Serving onhttp://localhost:5000

You can also launch ctrl-v using `$ python -m ctrl-v`.

By default, the app runs on port  5000 on 127.0.0.1. 

You can however choose to run it on a different port or host using the `--port` and `--host` options.

    $ ctrl-v --host 0.0.0.0 --port 5500
    Serving on http://0.0.0.0:5500

### Password protection

To add a username and password to protect you site, use the `protect` command.

    $ ctrl-v protect
    Username: bitto
    Password: 
    Repeat for confirmation: 
    Your site is now protected.

To remove password protection use the `removeprotect` command.

    $ ctrl-v removeprotect
    Protection is removed

### Uninstall ctrl-v

    $ pip uninstall ctrl-v

  [1]: https://pypi.org/

