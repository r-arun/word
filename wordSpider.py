import time
import os
import parseDictionary as pd
import pickle
from trie import Trie
class Word():
	def __init__(self):
		fd=open('dictionary','rb')
		self.dic=pickle.load(fd)
		fd.close()
		if(not os.path.exists('finished.trie')):
			self.finished=Trie()
		else:
			fd=open('finished.trie','rb')
			self.finished=pickle.load(fd)
#		fd=open('finished.trie','rb')
#		self.finished=pickle.load(fd)
#		fd.close()
#		fd=open('remaining.trie','rb')
#		self.finished=pickle.load(fd)
#		fd.close()

	def dumpster(self,fname,obj):
		fd=open(fname,'wb')
		pickle.dump(obj,fd)
		fd.close()

	def addWordFromDictionary(self,word):
		meaning,example,synonym=pd.getEntry(word)
		#print meaning
		#print synonym
		if(synonym ==[] and meaning==[]):
			return False
		return synonym,meaning,example

	def addWord(self,word):
		arr=self.addWordFromDictionary(word)
		if(arr==False):
			return arr
		self.dic[word]=[[],[],[],[],[]]
		synonym,meaning,example=arr
		self.dic[word][0].extend(synonym)
		self.dic[word][1].extend(meaning)
		self.dic[word][2].extend(example)
		self.finished.insert(word)
		self.dumpster('dictionary',self.dic)
		self.dumpster('finished.trie',self.finished)
		return True

	def mineWords(self,count):
		if(not os.path.exists('dictionary')):
			self.dic={}
		else:
			fd=open('dictionary','rb')
			self.dic=pickle.load(fd)
		if(not os.path.exists('remaining.trie')):
			fd=open('dictionary','rb')
			obj=pickle.load(fd)
			self.remaining=Trie()
			for word in obj.keys():
				self.remaining.insert(word)
		else:
			fd=open('remaining.trie','rb')
			self.remaining=pickle.load(fd)
		print self.finished.getSize()
		print self.remaining.getSize()
		for i in xrange(count):
			if(i%2):
				time.sleep(0.75)
			newword=self.remaining.getWord()
			print newword
			if(self.finished.search(newword)):
				continue
			ret=self.addWordFromDictionary(newword)
			if(ret):
				self.dic[newword]=ret
			self.finished.insert(newword)
			self.remaining.delete(newword)
		self.dumpster('dictionary',self.dic)
		self.dumpster('finished.trie',self.finished)
		self.dumpster('remaining.trie',self.remaining)
		print self.finished.getSize()
		print self.remaining.getSize()


if(__name__=='__main__'):
	w=Word()
	w.mineWords(278)
