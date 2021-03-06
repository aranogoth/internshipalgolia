from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import time
import simplejson
from algoliasearch import algoliasearch
import urllib

client = algoliasearch.Client("CE9TG6T1FN", 'APIKey')
index = client.init_index('internship test')
PORT = 7575

class AlgoliaRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path=self.path
        if path[0:19] == "/api/1/apps/?query=":
            query_request=self.path
            query_request=query_request[19:]
            query_request=urllib.unquote(query_request)
            answer=index.search(query_request,{'hitsPerPage': 10,'ignorePlurals': True})
            answer=simplejson.dumps(answer)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            return(self.wfile.write((answer)))
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error=dict()
            error["error"]="wrong path"
            error=simplejson.dumps(error)
            return (self.wfile.write(error))  

       

    def do_POST(self):
        if self.path=="/api/1/apps":
            self.send_response(200)
            self.end_headers()
            data = self.rfile.read(int(self.headers['Content-Length']))
            
            data = simplejson.loads(data) 
         
            key_words=["category","name","image_ok","image","rank","link","image_updated","objectID"]
            for i in range(len(key_words)):
                if (key_words[i] not in data):
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write("missing ")
                    error=dict()
                    error["missing"]=str(key_words[i])
                    error=simplejson.dumps(error)
                    return (self.wfile.write(error)) 
            stock_data_keys=data.keys()
            for j in range(len(stock_data_keys)):
                if (stock_data_keys[j] not in key_words):
                    self.send_response(404)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    error=dict()
                    error["you gave too much information"]=str(stock_data_keys[j])+" is not a category in your index"
                    error=simplejson.dumps(error)
                    return(self.wfile.write(error))
            if ("objectID" in data.keys()):
                del data["objectID"]
            res = index.add_object(data)
            print(res)
            print(type(res))
            res=simplejson.dumps(res)
            return(self.wfile.write(res))
        else :
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error=dict()
            error["error"]="wrong path"
            error=simplejson.dumps(error)
            return (self.wfile.write(error)) 


    def do_DELETE(self):
         
        def path_end_id(self):
            user_path=self.path
            user_path=str(user_path)
            default_path='/api/1/apps/'
            if (len(user_path)<12):
                return (False)
            for i in range (12):
                if (user_path[i]!=default_path[i]):
                    return(False)
            return(True)


    
        def object_id(self):
            path=self.path
            id=path[12:]
            id=str (id)
            return(id)
    
        if (path_end_id(self)):
            id=object_id(self)
            index.delete_object("id")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            completed=dict()
            completed["delete"]="object "+str(id)+" deleted"
            completed=simplejson.dumps(completed)
            self.wfile.write(completed)
            return()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            error=dict()
            error["error"]="wrong path"
            error=simplejson.dumps(error)
            return (self.wfile.write(error)) 

    
if __name__ == '__main__':
    # with socketserver.TCPServer(("", PORT), AlgoliaRequestHandler) as httpd:  
    #     print("serving at port", PORT)
    #     httpd.serve_forever()


    httpd = SocketServer.TCPServer(("", PORT), AlgoliaRequestHandler)
    print(time.asctime(), "Server Starts - %s:%s" % ("", PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % ("", PORT))
