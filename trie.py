import random
class Node():
	def __init__(self):
		self.dic={}
		self.value=''
		self.size=0
		
class Trie():
	def __init__(self):
		self.root=Node()

	def recursiveInsert(self,node,value,final):
		if(value==''):
			node.value=final
			return
		car=value[0]
		cdr=value[1:]
		if(not node.dic.has_key(car)): node.dic[car]=Node()
		self.recursiveInsert(node.dic[car],cdr,final)

	def insert(self,value):
		self.recursiveInsert(self.root,value,value)

	def recursiveDelete(self,node,string):
		if(string==''):
			if(node.value==''):
				return False
			node.value=''
			if(node.dic=={}):
				del node
			return True
		car=string[0]
		cdr=string[1:]
		if(not node.dic.has_key(car)):
			return False
		ret=self.recursiveDelete(node.dic[car],cdr)
		if(ret==False): return False
		if( node.dic[car].dic=={} and node.value==''):
			del node.dic[car]
		return True

	def delete(self,value):
		ret=self.recursiveDelete(self.root,value)
		if(ret==False):
			print value, "not found"
		else:
			print value,"deleted"

	def recursiveTraverse(self,node):
		if(node.value):
			print node.value
		if(node.dic=={}):
			return
		for i in node.dic.keys():
			self.recursiveTraverse(node.dic[i])

	def traverse(self):
		self.recursiveTraverse(self.root)

	def recursiveSearch(self,node,word):
		if(word==''):
			if(node.value):
				return True
			else:
				return False
		car=word[0]
		cdr=word[1:]
		if(node.dic.has_key(car)):
			return self.recursiveSearch(node.dic[car],cdr)
		else:
			return False

	def search(self,word):
		return self.recursiveSearch(self.root,word)

	def recursiveGetWord(self,node):
		if(node.value):
			return node.value
		if(node.dic=={}):
			print "Empty Dictionary"
			return None
		index=random.randint(0,len(node.dic)-1)
		return self.recursiveGetWord(node.dic[node.dic.keys()[index]])	

	def getWord(self):
		return self.recursiveGetWord(self.root)
	
	def recursiveGetSize(self,node):
		if(node.value):
			self.size+=1
		if(node.dic=={}):
			return
		for i in node.dic.keys():
			self.recursiveGetSize(node.dic[i])

	def getSize(self):
		self.size=0
		self.recursiveGetSize(self.root)
		return self.size
	
	def recursiveGetRandomWord(self,node,prob):
		if(node.value):
			if(node.dic=={}):
				return node.value
			if(random.randint(1,100)<=prob):
				return node.value
		index=random.randint(0,len(node.dic)-1)
		return self.recursiveGetRandomWord(node.dic[node.dic.keys()[index]],prob)

	def getRandomWord(self,prob):
		return self.recursiveGetRandomWord(self.root,prob)

