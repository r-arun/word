import random
import pickle
from synonymList import Synonymn
from selectOption import getTestWords
class Test():
	def __init__(self):
		fd=open('finished.trie','rb')
		self.obj=pickle.load(fd)
		fd.close()
		fd=open('dictionary','rb')
		self.dic=pickle.load(fd)
		fd.close()
		self.resultSet={}
		self.arr=self.dic.keys()
		self.length=len(self.arr)-1
		self.syn=Synonymn()

	def getWord(self):
		return self.arr[random.randint(0,self.length)]

	def addToResultSet(self,word):
		meaning=self.dic[word][1]
		testMeaning=getTestWords(meaning,word)
		if(testMeaning==[]): return False
		attempt=3
		while attempt>=0:
			ind=random.randint(0,len(testMeaning)-1)
			if(testMeaning[ind]==''):
				attempt-=1
				continue
			self.resultSet[word]=testMeaning[ind]
			return True
		return False

	def test(self,numOptions):
		self.resultSet={}
		word=self.getWord()
		self.addToResultSet(word)
		print "*******",word,"*******"
		synArr=self.syn.recursiveTransitiveClosure(word)
		numOptions-=1
		while(numOptions>0):	
			newWord=self.getWord()	
			if(newWord not in synArr and newWord not in self.resultSet.keys()):
				ret=self.addToResultSet(newWord)
				if(ret):
					numOptions-=1
		return [word,self.resultSet]

