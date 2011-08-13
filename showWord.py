import pickle
import random
class showWord():
	def __init__(self):
		fd=open('finished.trie','rb')
		self.finished=pickle.load(fd)
		fd.close()
		fd=open('dictionary','rb')
		self.dictionary=pickle.load(fd)

	def searchWord(self,word):
		return self.finished.search(word)

	def search(self,word):
		return self.finished.search(word)
			
	def anchor(self,arr):
		ret=''
		small=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
		big=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
		alpha=small
		alpha.extend(big)
		current=''
		print arr
		for i in arr:
			if(i in alpha):
				current+=i
			else:
				if(self.finished.search(current)):
					ret+=('<a href="search?word='+current+'">'+current+'</a>')
				else:
					ret+=current
				current=''
				ret+=i
		if(self.finished.search(current)):
			ret+=('<a href="search?word='+current+'">'+current+'</a>')
		else:
			ret+=current
		return ret

	def createList(self,msg,arr):
		ret='<h6>'+msg+'</h6>\n<ul>'
		for i in arr:
			ret+=('<li>'+self.anchor(i)+'</li>')
		ret+='</ul>'
		return ret

	def showWord(self,word):
		ret=''
		if(self.finished.search(word)):
			ret='<h4>'+word+'</h4>'
			arr=self.dictionary[word]
			ret+=self.createList('Part Of Speech',arr[2])
			ret+=self.createList('Synonym',arr[0])	
			ret+=self.createList('Meaning',arr[1])
			return ret
		return ret

	def randomWord(self):
		return self.dictionary.keys()[random.randint(0,len(self.dictionary))]
