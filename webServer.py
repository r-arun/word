import string,cgi,time
import os
from os import curdir,sep
from showWord import showWord
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from wordSpider import Word
from RecordReplay import RecordReplay
from testServer import Test
serverStateObject=None

def printRecordListing(arr):
	return '<td width="20%"><a href="rewind?filename='+arr[0]+'">'+arr[0]+'</a></td>\n<td width="40%">'+arr[1]+'</td><td width="40%">'+arr[2]+'</td>'

def paintAdded(word):
	return '<div style="background-color:#2222ee;color:white;text-align:center">'+word+' added</div>'

def paintSpecialMsg(msg):
	return '<div style="background-color:#2222ee;color:white;text-align:center">'+msg+' </div><br />'

def constructSearchRequest(word,string):
	divstyle='<div style="width:200;float:left">'
	return divstyle+'<a href="search?word='+word+'&traverse=true">'+string+"</a>"+"</div>\n"

def backToHome(string,addendum):
	ret = '<div style="background-color:#2222ee;color:white;text-align:center">'+string+'</div>'
	if(addendum):
		ret+=addendum
	ret+='<a href="home.html"> Go back to home</a>'
	return ret

class ServerState():
	def setAddendum(self):
		self.addendum=""
		if(self.recordState==0):
			fd=open('searchaddendum','rb')
			self.addendum=fd.read()
			self.addendum+='<br /><br /><div style="margin-left:43%"><a href="home.html">Go back to Home Page</a></div>'
			fd.close()
		elif(self.recordState==1):
			fd=open('recordaddendum','rb')
			self.addendum=fd.read()
			fd.close()
		else:
			self.addendum+=constructSearchRequest(self.recordObj.onFirst(),'First')
			self.addendum+=constructSearchRequest(self.recordObj.onPrevious(),'Previous')
			self.addendum+=constructSearchRequest(self.recordObj.currentPosition(),'Current')
			self.addendum+=constructSearchRequest(self.recordObj.onNext(),'Next')
			self.addendum+=constructSearchRequest(self.recordObj.onLast(),'Last')
			self.addendum+='<div style="width:200;float:left">\n<a href="stoprewind">Stop</a>\n</div>'
			self.addendum+='<div style="float:left"><a href="resumerecord">Resume Record</a></div>'
		print "ADDENDUM"
		print self.addendum
		print "END OF ADDENDUM"

	def __init__(self):
		self.recordObj=None
		self.recordState=0
		self.addendum=""
		self.setAddendum()
		self.testObj=None
		self.testWord=-1
		self.lastOptions=[]
		self.testReport=[]

	def displayQuestion(self,obj):
		self.lastOptions=[]
		word=obj[0]
		self.testReport.append([word])
		options=obj[1]
		cnt=0
		ret='<h5>'+word+'</h5>\n<form action="midtest">'
		for i in options.keys():
			ret+='<input type="radio" name="answer" value="'+str(cnt)+'" >'+options[i]+'</a><br />\n'
			self.lastOptions.append(options[i])
			if(i==word):
				self.testWord=cnt
			cnt+=1
		ret+='<br /><br /><input type="submit" value="Submit" /></form>'	
		return ret

	def checkAnswer(self,answer):
		print self.testReport[-1]
		print self.lastOptions
		self.testReport[-1].extend([self.lastOptions[int(answer)],self.lastOptions[self.testWord]])
		if(int(answer)==self.testWord):
			return True
		return False

	def testStatistics(self):
		ret='<h3>Results</h3>\n'
		ret+='<table>'
		correct='<tr style="color:#555555;background-color:#55aa55">'
		wrong='<tr style="color:#aaaaaa;background-color:#aa5555">'
		for i in self.testReport:
			answer=wrong
			if(i[1]==i[2]):
				answer=correct
			ret+='<tr>'+answer+"\n"
			for j in i:
				ret+='<td>'+j+'</td>\n'
			ret+='</div></tr>\n'
		ret+='</table>'
		ret+='<a href="home.html">Go back to Home Page</a>'
		return ret

	def setState(self,value):
		if(0<=value<=2):
			self.recordState=value

	def getState(self):
		return self.recordState

class MyHandler(BaseHTTPRequestHandler):
	def __init__(self,r1,r2,r3):
		print "INIT"
		BaseHTTPRequestHandler.__init__(self,r1,r2,r3)

	def send404(self):
		self.send_response(404)
		self.send_header('Content-type','text/html')
		self.end_headers()
		self.wfile.write("404 - Object not found")

	def paintHome(self,msg):
		ret=''
		if(msg):
			ret=paintSpecialMsg(msg)
		fd=open('html/home.html','rb')
		return ret+fd.read()

	def searchWord(self,word,args):
		s=showWord()		
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		if(s.search(word)):
			if(serverStateObject.recordState==2):
				if(args.has_key('traverse')):
					serverStateObject.recordObj.setCurrentPosition(word)
					serverStateObject.setAddendum()
			add=serverStateObject.addendum
			finalwrite=s.showWord(word)
		#	print finalwrite
			finalwrite='<html><body>\n'+finalwrite+'\n'+add+'\n</body></html>'
			self.wfile.write(finalwrite)
		#	print "END"
			if(serverStateObject.recordState==1):
				serverStateObject.recordObj.record(word)	
		else:
			self.wfile.write(self.paintHome(word+' not found in the word list.'))

	def getRecordObject(self):
		if(serverStateObject.recordObj==None):
			print "Creating a new record object"
			return RecordReplay()
		else:
			return serverStateObject.recordObj

	def do_GET(self):
		try:
			print self.path
			self.path=self.path[1:]
			funcname=''
			args=[]
			arr=self.path.split('?')
			funcname=arr[0]
			argsdic={}
			if(self.path==''):
				self.path='home.html'
			if(len(arr)>1):
				args=arr[1].split('&')
			for i in args:
				inarr=i.split('=')	
				argsdic[inarr[0]]=inarr[1]
			print funcname
			print argsdic
			if self.path.endswith(".html"):
				fname=self.path
				print "LOADING HTML"
				print fname
				if(os.path.exists('html/'+fname)):
					fd=open('html/'+fname,'rb')
					self.send_response(200)
					self.send_header('Content-type','text/html')
					self.end_headers()
					self.wfile.write(fd.read())
				else:
					self.send404()
			else:
				if(funcname=='starttest'):
					serverStateObject.testObj=Test()
					serverStateObject.testCount=int(argsdic['count'])
					print 'test'
					self.wfile.write(serverStateObject.displayQuestion(serverStateObject.testObj.test(4)))
					serverStateObject.testCount-=1
				elif(funcname=='midtest'):
					print serverStateObject.checkAnswer(argsdic['answer'])
					if(serverStateObject.testCount):
						self.wfile.write(serverStateObject.displayQuestion(serverStateObject.testObj.test(4)))
						serverStateObject.testCount-=1
					else:
						self.wfile.write(serverStateObject.testStatistics())
					#TODO END of test
				else:
					if(funcname=='startrecord'):
						serverStateObject.setState(1)	
						serverStateObject.recordObj=RecordReplay()
						serverStateObject.recordObj.startRecording(argsdic['filename'])
						serverStateObject.setAddendum()
						self.wfile.write(self.paintHome('Recording Started'))
					elif(funcname=='resumerecord'):
						if(serverStateObject.recordObj.isActive()):
							print "Resuming"
							serverStateObject.setState(1)
							serverStateObject.setAddendum()
						self.wfile.write(self.paintHome('Resuming session '))
					elif(funcname=='pauserecord'):
						serverStateObject.setState(0)
						self.wfile.write(backToHome('Recording Paused',serverStateObject.addendum))
						self.wfile.write(self.paintHome('Recording Paused'))
					elif(funcname=='stoprecord'):
						serverStateObject.setState(0)
						serverStateObject.recordObj.dumpster()
						serverStateObject.recordObj.clear()
						serverStateObject.setAddendum()
						self.wfile.write(self.paintHome('Recording Stopped and Stored'))
					elif(funcname=='listrecord'):
						serverStateObject.recordObj=self.getRecordObject()
						listing=serverStateObject.recordObj.showRecording()	
						htmlRet='<table cellpadding="2" cellspacing="5">'
						for arr in listing:
							htmlRet+='<tr>\n'
							htmlRet+=printRecordListing(arr)
							htmlRet+='\n</tr>\n'
						htmlRet+='</table>'	
						self.send_response(200)
						self.send_header('Content-type','text/html')
						self.end_headers()
						self.wfile.write(htmlRet)
					elif(funcname=='rewind'):
						print "REWIND MACHI"
						serverStateObject.recordObj=self.getRecordObject()
						if(serverStateObject.recordObj.reloadFile(argsdic['filename'])):
							serverStateObject.setState(2)
							serverStateObject.setAddendum()
							self.searchWord(serverStateObject.recordObj.onFirst(),argsdic)
							print serverStateObject.addendum
						else:
							self.send404()
						print "END OF REWIND MACHI"
					elif(funcname=='stoprewind'):
						serverStateObject.setState(0)
						serverStateObject.setAddendum()
						self.wfile.write(self.paintHome('Rewind Stopped'))
					elif(funcname=='search'):
						print "HERE SEARCH"
						self.searchWord(argsdic['word'],argsdic)
						return
					elif(funcname=='randomword'):
						self.searchWord(showWord().randomWord(),{})
					elif(funcname=='add'):
						s=Word()
						self.send_response(200)
						self.send_header('Content-type','text/html')
						self.end_headers()
						if(s.addWord(argsdic['word'])):
							self.wfile.write(paintAdded(argsdic['word'])+showWord().showWord(argsdic['word'])+serverStateObject.addendum)
							if(serverStateObject.recordState==1):
								serverStateObject.recordObj.record(argsdic['word'])	
						else:
							self.wfile.write(argsdic['word']+" does not exist"+serverStateObject.addendum)
					else:
						self.send404()
			return	
		except IOError:
			self.send_response(404)
			self.send_error(404,'File Not found')
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write("404, Object not found")
			return

def main():
	global serverStateObject
	serverStateObject=ServerState()
	try:
		server=HTTPServer(('',8080),MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print 'Received an interrupt'
		server.socket.close()

if __name__=='__main__':
	main()

