import pickle
from trie import Trie
from spaceStrip import strip
class Synonymn():

	def getSynonymnFromMeaning(self,dic,word):
		arr=[]
		if(dic[word][1]==None): return arr
		for i in dic[word][1]:
			i=strip(i)
			if(i==None):
				print dic[word][1]," missing"
				continue
			if(i.find(' ')>=0 or i.find(')')>=0 or i=='Ex.' or i=='' or i=='V.' or i=='ADJ.' or i=='N.'):
				continue
			arr.append(i)	
		return arr
		
	def initializeRelation(self):
		f=open('dictionary','rb')
		dic=pickle.load(f)
		f.close()
		f=open('finished.trie','rb')
		finished=pickle.load(f)
		f.close()
		for i in dic.keys():
			if(finished.search(i)):
				if(type(dic[i][0])==(str)):
					print "HECK"
					self.graph[i]=[dic[i][0]]	
				else:
					self.graph[i]=dic[i][0]
				self.graph[i].extend(self.getSynonymnFromMeaning(dic,i))

	def __init__(self):
		self.graph={}
		self.visited=[]
		self.initializeRelation()

	def recursiveTransitiveClosure(self,word):
		arr=[word]
		if(word in self.visited): return []
		self.visited.append(word)
		for i in self.graph[word]:
			if(self.graph.has_key(i)):
				arr.extend(self.recursiveTransitiveClosure(i))
			else:
				arr.append(i)
		return arr	
			
	def transitiveClosure(self):
		cnt=0
		for i in self.graph.keys():
			if(i in self.visited):
				continue
			arr=self.recursiveTransitiveClosure(i)
			dic=Trie()
			cnt+=1
			for j in arr:
				dic.insert(j)
			for j in arr:
				if(j in self.graph):
					self.graph[j]=dic
		fd=open('synonymnRelation.trie','wb')
		pickle.dump(self.graph,fd)
		fd.close()
		print cnt
