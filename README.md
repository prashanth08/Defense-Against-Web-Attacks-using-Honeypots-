get-webserver-py
================

Simple web-server to server script GET requests for development on localhost without running full fledged web-server. 

The server serves files from current folder and subfolders, requested with GET request.
If there is a need to serve files from other locations, it can be configured with configuration files with name 'path.map'. This files are looked up through the tree to the root folder and applied one after other.

Configuration
----------
path.map files use ini-files syntax.

Content of config files:

[map]
/map/path/ = /real/disk/folder/or/file
/map/path/to/remove/ =
/map/path/to/mapped/file = /real/disk/file
/map/path2/ = relative/path/

The order of map definitions is important!
Lookup uses first matched path.
If value of the path is empty - this path will be undefined even if this
mapping exists somewhere in the parent configuration files.
If left side ends with '/' it is treated as folder, otherwise the path is path to file

The folder from which started the script is added as last mapping entry for path '/'

Opening root folder shows all html files located in the folder where the web server started.

Running web-server
-------

       python webserver.py

By default the web-server runs on port 8181. It can be changed with providing port number as parameter:

	python webserver.py <port>
