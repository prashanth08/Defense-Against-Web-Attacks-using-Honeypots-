#simple web server to serve GET requests by content
# from folders mapped in _LOCATIONS list

# Configuration
#
# For configuration used ini-files with name 'path.map'
# The path.map files are looked in current folder and all parent folders
# The values in lower folder override values in parent folders
# Content of config files:
#
# [map]
# /map/path/ = /real/disk/folder/or/file
# /map/path/to/remove/ =
# /map/path/to/mapped/file = /real/disk/file
# /map/path2/ = relative/path/
#
# The order of map definitions is important!
# Lookup uses first matched path
# If value of the path is empty - this path will be undefined even if this
# mapping exists somewhere in the parent configuration files.
# If left side ends with '/' it is treated as folder,
# otherwise the path is path to file
#
# The folder from which started the script is added as last mapping entry for path '/'
#
# Opening root folder shows all html files located in the folder where
# the web server started.
#
# By default server starts with _DEFAULT_PORT = 8181
# It can be redefined by providing port number as first parameter

import os
import sys
from ConfigParser import ConfigParser
import fnmatch
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Wrapper:
    def __init__(self, locations):
        self._locations = locations
    def __call__(self, request, client_address, server):
        return Handler(request, client_address, server, self._locations)

class Handler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server, locations):
        self.locations = locations
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', self._guessResourceContentType("html"))
            self.end_headers()
            self.wfile.write(get_root_links_html())
            return
        try:
            questionPos = self.path.find('?')
            requestPath = self.path[:questionPos]  if questionPos >=0 else self.path
            print 'REQUEST_PATH: %s' % requestPath
            isMatchFound = False
            resourceExtention = self._extractResourceExtention(requestPath)
            for webPath, dirPath in self.locations:
                if requestPath.startswith(webPath):
                    if webPath.endswith('/'):
                        resourcePath = os.path.join(dirPath, requestPath[len(webPath):])
                    else:
                        resourcePath = dirPath
                    print 'resourcePath: %s' % resourcePath
                    resource = self._getResource(resourcePath, self._isTextFile(resourceExtention))
                    if resource:
                        resourceLength = len(resource)
                        self.send_response(200)
                        self.send_header('Content-type', self._guessResourceContentType(resourceExtention))
                        self.send_header('Content-Length', resourceLength)
                        self.send_header('Content-Range', 'bytes 0-%s/%s' % (resourceLength - 1, resourceLength))
                        self.end_headers()
                        self.wfile.write(resource)
                        isMatchFound = True
                        break
            if not isMatchFound:
                self._sendNotFound()
        except IOError:
            self._sendNotFound()
    def _sendNotFound(self):
        self.send_error(404,'File Not Found: %s' % self.path)
    _MIME_TYPES = dict(
        html = 'text/html',
        txt = 'text/plain',
        js = 'text/javascript',
        css = 'text/css',
        xml = 'text/xml',
        gif = 'image/gif',
        jpg = 'image/jpeg',
        jpeg = 'image/jpeg',
        png = 'image/png',
        tif = 'image/tiff',
        tiff = 'image/tiff',
        wav = 'audio/x-wav',
        mp3 = 'audio/mpeg',
        ogg = 'video/ogg',
        manifest = 'text/cache-manifest',
    )
    _TEXT_MIME_TYPES = ('html', 'txt', 'js', 'css', 'xml')
    def _isTextFile(self, fileExtenstion):
        return fileExtenstion in self._MIME_TYPES
    
    def _extractResourceExtention(self, resourcePath):
        root, ext = os.path.splitext(resourcePath)
        return ext.lower()[1:] if ext else ""
    
    def _guessResourceContentType(self, resourceExtention):
        mimeType = None
        for k, v in self._MIME_TYPES.iteritems():
            if resourceExtention == k:
                mimeType = v
                break
        return mimeType if mimeType else self._MIME_TYPES.get('txt')
    
    def _getResource(self, resourcePath, isText):
        try:
            if os.path.isfile(resourcePath):
                f = open(resourcePath, 'r' if isText else 'rb')
                data = f.read()
                f.close()
                return data
        except IOError, ex:
            print ex
        return None

def run_server(locations, port=80):
    try:
        server = HTTPServer(('', port), Wrapper(locations))
        print 'started httpserver at port %d...' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

_PATH_MAP_FILE = 'path.map'
_ABS_PATH_PREFIXES = ('/', 'http://', 'https://')

def _is_abs_path(path):
    res = False
    for prefix in _ABS_PATH_PREFIXES:
        if path[0:len(prefix)] == prefix:
            res = True
            break
    return res

def load_locations_map():
    config = list()
    cwd = os.getcwd()
    d = cwd
    while len(d) > 0:
#        print d
        fname = os.path.join(d, _PATH_MAP_FILE)
        if os.path.isfile(fname):
            cp = ConfigParser()
            cp.read(fname)
            for key, val in cp.items('map'):
                if not _is_abs_path(val): #put back removed by abspath slash if it was there
                    path = os.path.abspath(os.path.join(d, val))
                    if path[-1] != val[-1]:
                        path += val[-1]
                    val = path
                config.append((key, val))
        dnew, dummy = os.path.split(d)
        if dnew == d:
            break;
        d = dnew
    res = []
    setSettings = set()
    for i in range(0, len(config)):
        v = config[i]
        
        if not v[0] in setSettings:
            setSettings.add(v[0])
            if len(v[1].strip()) > 0:
                res.append(v)
    if cwd[-1] != '/':
        cwd = cwd + '/'
    res.append(('/', cwd))
    return res

_HTML_TEMPLATE = '''<html>
<head><title>%s</title></head>
<body>
<h3>%s</h3>
%s
</body>
</html>
'''
def get_root_links_html():
    cwd = os.getcwd()
    links = []
    for f in os.listdir(cwd):
        if fnmatch.fnmatch(f, '*.html'):
            links.append('<div><a href="%s">%s</a></div>' % (f, f));
    return _HTML_TEMPLATE % (cwd, cwd, ''.join(links))
    
_DEFAULT_PORT = 8181

def _test_config_loading():
    print load_locations_map()
        
def run(port=0):
    if port > 0:
        _PORT = port
    else:
        _PORT = int(sys.argv[1]) if len(sys.argv) > 1 else _DEFAULT_PORT
    _locations = load_locations_map()
    print 'search locations: \n%s' % _locations
    # ---- settings ---- end

    run_server(_locations, _PORT)
    
if __name__ == '__main__':
##    _test_config_loading()
    # ---- settings ---- begin
##    _LOCATIONS = [
##        ('/app/lib/', 'test-data/data-2'),
##        ('/app/', 'test-data/data-1')
##    ]
    run()

