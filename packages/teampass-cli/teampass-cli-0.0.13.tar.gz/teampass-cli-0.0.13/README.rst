==============================================
Teampass-cli - teampass command-line interface
==============================================


What is this?
*************
It is a simple command line interface for Teampass (https://teampass.net).
``teampass-cli`` provides an executable called ``tpcli``

**IMPORTANT**: To use the teampass-cli, you need to modify the file ``api/functions.php`` on the server there Teampass was installed. The modified version of the file ``api/functions.php`` is located in the lib folder in this repository.
This moodified version of functions.php is tested with Teampass 2.1.27.35 and 2.1.27.36

Current version of functions.php is synchronized with the upstream version in Teampass repository.

As for the changes in the functions.php that have been made:

**API methods have been added to the function restGet():**

1. For CLI **list** sub-command:

- /list/folders

- /list/items

2. Get item and folder by ID:

- /get/item/{item_id}

- /get/folder/{folder_id}

3. Search item and folder by Title:

- /find/items/{item_title}

- /find/items/{folder_title}

Installation
************
*on most UNIX-like systems, you'll probably need to run the following
`install` commands as root or by using sudo*

**pip**

::

  pip install teampass-cli

**from source**

::

  pip install git+http://github.com/verdel/teampass-cli

**or**

::

  git clone git://github.com/verdel/teampass-cli.git
  cd teampass-cli
  python setup.py install

as a result, the ``tpcli`` executable will be installed into a system ``bin``
directory


Usage
-----
::


  tpcli --help
  Usage: -c [OPTIONS] COMMAND [ARGS]...
  Options:
    --api-endpoint TEXT  Teampass API endpoint.
    --api-key TEXT       Teampass API key.
    --help               Show this message and exit.

  Commands:
    add     add entry to Teampass
    delete  delete entry from Teampass
    edit    edit entry in Teampass
    list    show entry from Teampass
    search  search entry in Teampass


  tpcli add --help
  Usage: -c add [OPTIONS]

  Add entry to Teampass.

  Options:
    --item              add item
    --folder            add folder
    --title TEXT        title for new folder or label for new item  [required]
    --login TEXT        login value for new item
    --password TEXT     password value for new item
    --description TEXT  description value for new item
    --folder-id TEXT    parent folder id  [required]
    --list              format output as list
    --table             format output as table
    --help              Show this message and exit.


  tpcli delete --help
  Usage: -c delete [OPTIONS]

  Delete entry from Teampass.

  Options:
    --item     delete item
    --folder   delete folder with sub-folders and items
    --id TEXT  entry id  [required]
    --help     Show this message and exit.


  tpcli edit --help
  Usage: -c edit [OPTIONS]

  Edit entry in Teampass.

  Options:
    --item              add item
    --folder            add folder
    --id TEXT           entry id  [required]
    --title TEXT        title for entry
    --login TEXT        login value for entry
    --password TEXT     password value for entry
    --description TEXT  description value for entry
    --folder-id TEXT    parent folder id
    --list              format output as list
    --table             format output as table
    --help              Show this message and exit.


  tpcli list --help
  Usage: -c list [OPTIONS]

  List entry from Teampass.

  Options:
    --item    show items
    --folder  show folders
    --list    format output as list
    --table   format output as table
    --tree    format output as tree
    --help    Show this message and exit.


  tpcli search --help
  Usage: -c search [OPTIONS] TEXT

  Search entry in Teampass.

  Options:
    --item    search items
    --folder  search folders
    --list    format output as list
    --table   format output as table
    --help    Show this message and exit.
