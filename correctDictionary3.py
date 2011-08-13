from spaceStrip import strip
import pickle
def specialForm(sentence):
	if(sentence.find('.')>=0):
		arr=sentence.split('.')[0]
		if(arr.find(' ')<0):
			return arr
	return False

def selectDirect(sentence):
	if(sentence.find('.')>=0):
		arr=sentence.split('.')
		newstring=' '.join(arr[1:])
		if(newstring.find(':')>=0):
			word=newstring.split(':')[0]
			return word
	return False

def selectIndirect(word,sentence):
	if(sentence.find('.')>=0):
		arr=sentence.split('.')
		newstring=' '.join(arr[1:])
		if(newstring.find(':')<0 and newstring.find(' ')>=0):
			newarr=newstring.split(' ')
			rest=' '
			newword=newarr[0]
			if(len(newarr)>1):
				rest=' '.join(newarr[1:])
			ilen=len(word)
			jlen=len(newword)
			mylen=min(ilen,jlen)
			cnt=0
			while(cnt<3 and mylen-cnt>=0):
				if(word[:mylen-cnt]==newword[:mylen-cnt]):
					return newword,rest
				cnt+=1
	return False
oppcount=0	
relcount=0
fd=open('dictionary','rb')
dic=pickle.load(fd)
newdic={}
for i in dic.keys():
	i=strip(i)
	newdic[i]={}
	meaning=[]
	example=[]
	related=[]
	otherword={}
	opposite=[]
	part=[]
	for j in dic[i]:
		spl=specialForm(j)
		if(not spl):
			meaning.append(j)
		elif(spl=='Ex'):
			example.append(' '.join(j.split('.')[1:]))
		elif(spl in ['V','N','v','ADJ','ADV']):
			if(spl=='v'): spl='V'
			if(spl not in part):
				part.append(spl)
			word=selectDirect(j)
			if(word):
				exp=j.split(':')[1]
				if(not otherword.has_key(spl)):
					otherword[spl]=[]
				otherword[spl].append(word)
				if(not newdic.has_key(word)):
					newdic[word]={}
					newdic[word]['meaning']=[]
				newdic[word]['meaning'].append(exp)
			else:
				word=selectIndirect(i,j)
				if(word):
					word,exp=word[0],word[1]
					word=strip(word)
					if(not newdic.has_key(word)):
						newdic[word]={}
						newdic[word]['meaning']=[]
					newdic[word]['meaning'].append(exp)
		elif(spl=='OP'):
			opposite.append(' '.join(j.split('.')[1:]))
			oppcount+=1
		else:
			related.append(' '.join(j.split('.')[1:]))
			relcount+=1
	newdic[i]['meaning']=meaning
	newdic[i]['example']=example
	newdic[i]['otherword']=otherword
	newdic[i]['part']=part
	newdic[i]['opposite']=opposite
	newdic[i]['related']=related
	print i,newdic[i]
	print oppcount
print "New Words"
newarr=[]
for i in newdic.keys():
	if i not in dic.keys():
		newarr.append(i)
print newarr
print len(newarr)
print relcount 
print newdic.keys()
