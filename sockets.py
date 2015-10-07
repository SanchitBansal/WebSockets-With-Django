import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import time
import threading
'''
This is a simple Websocket server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin purposes. 
Along with it functionality to read logs and return to connection is there.
''' 

SOCKET = {}

class FileLogRunner:
	def __init__(self):
		self._running = True

	def terminate(self):
		self._running = False

	def run(self, path, socket):
		index = 0
		while self._running:
			print "location of log file ", path
			fh = open(path, "r")
			dd = fh.readlines()
			data = dd[index:]
			index = len(dd)
			if index == 0:
				socket.write_message("--BLANK--")
				fh.close()
				break
			if len(data) != 0:
			  try:
			    while len(data[:5000]) >0:
			      socket.write_message("".join(data[:5000]))
			      data = data[5000:]
			      if 'END OF LOGS' in data[-1]:
			        break
			      else:
			        time.sleep(1)
			  except:
			    pass
			fh.close()
			
 
class WSHandler(tornado.websocket.WebSocketHandler):
  '''
  argument id is identity of each request could be any random value
  path is location of logfile from where it would read logs
  '''
  def open(self):
	try:
		self.id = self.get_argument("id")
		self.ccr = self.get_argument("path")
		globals()['SOCKET'][self.id] = self
		
		print 'new connection'
		print globals()['SOCKET']
		
		l = FileLogRunner()
		self.logrunner = l
		t = threading.Thread(target = l.run, args = (self.path, self))
		t.start()
		self.thread = t

	except Exception as e:
		print e
      
  def on_message(self, message):
        print 'message received:  %s' % message
        # Reverse Message and send it back
        print 'sending back message: %s' % message[::-1]
        self.write_message(message[::-1])
 
  def on_close(self):
        print 'connection closed'
	
	l = self.logrunner
	print "Terminating Thread"
	l.terminate()
	t = self.thread
	t.join()	
	print "Thread finished"
  
  del globals()['SOCKET'][self.id]
	print globals()['SOCKET']
	
 
  def check_origin(self, origin):
        return True

application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    try:
	    http_server = tornado.httpserver.HTTPServer(application)
	    http_server.listen(8008)
	    myIP = socket.gethostbyname(socket.gethostname())
	    print '*** Websocket Server Started at %s***' % myIP
	    tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
	    print e
