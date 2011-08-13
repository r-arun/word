import pickle
from spaceStrip import strip
collection=[]
def findSpecial(sentence):
	if(sentence.find('.')>=0):
		init=sentence.split('.')[0]
		if(init.find(' ')<0):
			return init
	return False

def findSpecial2(sentence,delim):
	if(sentence.find(delim)>=0):
		init=sentence.split(delim)[0]
		if(init in collection):
			return init
	return False

def main_fill(dic):
	for i in dic.keys():
		for j in dic[i]:
			init=findSpecial(j)
			if(init):
				if(init not in collection):	
					collection.append(init)

def findWord(sentence,word):
	arr=sentence.split(' ')
	wlen=len(word)
	for i in arr:
		i=strip(i)
		count=0
		ilen=len(i)
		mlen=min(wlen,ilen)
		while count<3 and mlen-count>0 :
			if(word[:mlen-count]==i[:mlen-count]):
				return i
			count+=1
	return False

def main(word,dic):
	print word,dic[word]
	example=[]
	meaning=[]
	opposite=[]
	related={}
	for j in dic[word]:
		init=findSpecial(j)
		if(init=='Ex' or init=='EX'):
			example.append(j)		
			continue
		if(init=='OP' or init=='Op' or init=='op'):
			opposite.append(j)
			continue
		if(init and strip(j)==init+'.'):
			if(not related.has_key(init)):
				related[init]=[]
			if(word not in related[init]):
				related[init].append(word)
			continue
		if(init or findSpecial2(j,' ') or findSpecial2(j,':')):	
			newword=findWord(j,word)
			if(init):
				j=' '.join(j.split('.')[1:])
			else:
				init=findSpecial2(j,' ')
				if(init):
					j=' '.join(j.split(' ')[1:])
				else:
					init=(findSpecial2(j,':'))
					if(init):
						j=' '.join(j.split(':')[1:])
			j=strip(j)
			if(newword):
				exp=	' '.join(j.split(newword))
				exp=strip(exp)
				if(not exp==''):
					meaning.append(strip(exp))
				if(not related.has_key(init)):
					related[init]=[]
				if(newword not in related[init]):
					related[init].append(newword)
				continue
		if(not (init=='CF' or init=='Cf')):
			meaning.append(j)
	return [meaning,example,related,opposite]

fd=open('dictionary','rb')
dic=pickle.load(fd)
main_fill(dic)
newdic={}
for i in dic.keys():
	newdic[i]=main(i,dic)
fd.close()
fd=open('newdictionary','wb')
pickle.dump(newdic,fd)
fd.close()
	
