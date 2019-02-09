import platform
from http.server import BaseHTTPRequestHandler,HTTPServer
from threading import Thread
from pathlib import Path
from .settings_manager import *
from .note_manager import NoteManager
from .recent_db_manager import RecentDBManager
from .keyword_db_manager import KeywordDBManager
from urllib.parse import parse_qs
import os, sys
import tempfile
import cgi
from stat import *
import json
#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    APP_PATH = "/home/phieelementary/Dev/GitBis/QuickDoc/CarnetNextcloud/templates/CarnetElectron"
	#Handler for the GET requests
    def do_GET(self):
        try:
            index = self.path.index("?")
            spath = self.path[0:index]
            params = parse_qs(self.path[index+1:])
        except ValueError:
            spath = self.path
        if(self.path.startswith("/api/")):
            spath = spath[len("/api/"):]

            print(spath)
            if spath == "recentdb":
                try:
                    file = open(settingsManager.getNotePath()+"/quickdoc/recentdb/"+settingsManager.getUUID(), 'r')
                    text = file.read()
                    file.close()
                except FileNotFoundError:
                    text = "{\"data\":[]}"
                data = bytes(text, "utf8")
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "keywordsdb":

                try:
                    file = open(settingsManager.getNotePath()+"/quickdoc/keywords/"+settingsManager.getUUID(), 'r')
                    text = file.read()
                    file.close()
                except FileNotFoundError:
                    text = "{\"data\":[]}"
                data = bytes(text, "utf8")
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "note/open/prepare":
                data = bytes("/reader/reader.html", "utf8")
                self.send_response(200)
            elif spath == "browser/list":
                files = os.listdir(settingsManager.getNotePath()+"/"+params['path'][0])
                ret = []
                for name in files:
                    print(name)
                    s = os.stat(settingsManager.getNotePath()+"/"+params['path'][0]+"/"+name)
                    file = {}
                    file["name"] = name
                    file["path"] = params['path'][0]+"/"+name
                    file["isDir"] = S_ISDIR(s.st_mode)
                    file["mtime"] = s.st_mtime
                    ret.append(file)
                print(json.dumps(ret))
                data = str.encode(json.dumps(ret))
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "recentdb/merge":
                recentDBManager = RecentDBManager()
                recentDBManager.merge()
                data = bytes(recentDBManager.getMyRecentDBString(), "utf8")
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "keywordsdb/merge":
                keyword_db_manager = KeywordDBManager()
                keyword_db_manager.merge()
                data = bytes(keyword_db_manager.getMyKeywordDBString(), "utf8")
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "note/open":
                tmpNoteDir = self.getTmpNoteDir()
                currentManager = NoteManager(settingsManager.getNotePath()+"/"+params['path'][0])
                ret = currentManager.extractNote(tmpNoteDir)
                ret['id'] = 0
                data = str.encode(json.dumps(ret))
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "settings/editor_css":
                data = str.encode("[\"/editor.css\"]")
                self.send_response(200)
                self.send_header('Content-type','application/json')
            elif spath == "metadata":
                ret = {}
                for notePath in params['paths'][0].split(','):
                    if(notePath == ""):
                        continue
                    try:
                        manager = NoteManager(settingsManager.getNotePath()+"/"+notePath)
                        ret[notePath] = manager.getMetadata()
                    except FileNotFoundError:
                        print("not found")
                print(json.dumps(ret))
                data = str.encode(json.dumps(ret))
                self.send_response(200)
                self.send_header('Content-type','application/json')
            else:
                data = str.encode("notyetimplemented")
                self.send_response(404)

        else:
            if(spath == "/"):
                file = open(self.APP_PATH+'/index.html', 'r')
                text = file.read()
                file.close()
                data = str.encode(text.replace("!API_URL","api/"))
            elif(spath == "/reader/reader.html"):
                file = open(self.APP_PATH+"/reader/reader.html", 'r')
                text = file.read()
                file.close()
                data = str.encode(text.replace("<!ROOTPATH>","/").replace("<!APIURL>","/api/"))
            elif(spath == "/editor.css"):
                data = str.encode(".toolbar {\
	                background: #"+settingsManager.getHeaderBarBG()+";\
                }")
            else:
                data = Path(self.APP_PATH+spath).read_bytes()
            self.send_response(200)
        self.send_header('','')
        self.end_headers()
        # Send the html message
        self.wfile.write(data)
        return

    def do_POST(self):
        try:
            index = self.path.index("?")
            spath = self.path[0:index]
            params = parse_qs(self.path[index+1:])
        except ValueError:
            spath = self.path
        if(self.path.startswith("/api/")):
            spath = spath[len("/api/"):]
            if spath == "note/saveText":
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                manager = NoteManager(settingsManager.getNotePath()+"/"+form.getvalue("path"))
                print(form.getvalue("metadata"))
                manager.saveTextAndMetadataToOpenedNote(form.getvalue("html"), form.getvalue("metadata"), self.getTmpNoteDir())

                data = str.encode("")
                self.send_response(200)
        self.send_header('','')
        self.end_headers()
        # Send the html message
        self.wfile.write(data)




    def getTmpNoteDir(self):
        return  tempfile.gettempdir()+"/CarnetGTK/Note";
class Server():
    PORT_NUMBER = 8087
    def server_thread(z):
        try:
	        #Create a web server and define the handler to manage the
	        #incoming request
	        server = HTTPServer(('', z.PORT_NUMBER), myHandler)


	        #Wait forever for incoming htto requests
	        server.serve_forever()

        except KeyboardInterrupt:
	        print ('^C received, shutting down the web server')
	        server.socket.close()

    def start(self):
        thread = Thread(target = self.server_thread)
        thread.start()