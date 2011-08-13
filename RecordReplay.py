import os
import pickle
class RecordReplay():
	def __init__(self):
		self.fname=''
		self.dic=[]
		self.pos=0

	def record(self,word):
		self.dic.append(word)

	def dumpster(self):
		fd=open(self.fname,'wb')
		pickle.dump(self.dic,fd)

	def clear(self):
		self.fname=''
		self.dic=[]

	def onFirst(self):
		return self.dic[0]

	def onLast(self):
		return self.dic[-1]

	def setCurrentPosition(self,word):
		for i in xrange(len(self.dic)):
			if(self.dic[i]==word):
				self.pos=i
				break
	def onNext(self):
		return self.dic[(self.pos+1)%len(self.dic)]

	def onPrevious(self):
		if(self.pos==0):
			return self.onLast()
		return self.dic[self.pos-1]

	def currentPosition(self):
		return self.dic[self.pos]

	def startRecording(self,fname):
		self.fname='recording/'+fname

	def isActive(self):
		if(not self.fname==''): return True
		return False

	def reloadFile(self,fname):
		self.fname='recording/'+fname
		print "DEBUG 2",self.fname
		if(os.path.exists(self.fname)):
			fd=open(self.fname,'rb')
			self.dic=pickle.load(fd)
			fd.close()
			return True
		return False

	def showRecording(self):
		dirpath='recording/'
		arr=os.listdir(dirpath)
		ret=[]
		for i in arr:
			ret.append('<a href="rewind?filename='+i+'">'+i+'</a>')
		return ret
