pypboy_ng
======

This fork brings pypboy to the present, by migrate it to python 3.x, adds new features and fixing stuff.

Remember that one Python Pip-Boy 3000 project? Neither do we!<br>
Python/Pygame interface, emulating that of the Pipboy-3000.<br> 
Uses OSM for map data and has been partially tailored to respond to physical switches over Raspberry Pi's GPIO<br>


## Features

Work with Screen TFT 3.5" Capacitive of Adafruit<br>
Supports caching and offline loading of maps.

Start with:

git clone
cd pypboy_ng
uv init
uv add requirements.txt
uv sync

* In config.py set 'LOAD_CACHED_MAP = False'
* Run the application once
* In config.py set 'LOAD_CACHED_MAP = True'
* Pypboy will now load the cached map on starting

Additional:
* Migrated to modern python 3.x Version
* uv as packet-manager 
* systemd starup service and config for headless start directly after booting

Planed in future:
* fully working maps (I never get the old custom mapping running)
* Fixing issues with UI
* more to come

## Thanks to 
* Fixes and Updates by Goldstein
* Updates by Sabas of The Inventor's House Hackerspace
* Originally by grieve work original

## License
MIT

##Contributions

Contribuyendo a este programa se da la bienvenida con gusto.<br>

Contributing to this software is warmly welcomed. You can do this basically by [forking](https://help.github.com/articles/fork-a-repo), committing modifications and then [pulling requests](https://help.github.com/articles/using-pull-requests) (follow the links above for operating guide). Adding change log and your contact into file header is encouraged.<br>

Thanks for your contribution.

Enjoy!
