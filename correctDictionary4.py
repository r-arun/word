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
			return strip(word)
	return False

def selectIndirect(word,sentence):
	if(sentence.find('.')>=0):
		arr=sentence.split('.')
		newstring=' '.join(arr[1:])
		if(newstring.find(':')<0 and newstring.find(' ')>=0):
			newarr=newstring.split(' ')
			rest=' '
			newword=strip(newarr[0])
			if(len(newarr)>1):
				rest=' '.join(newarr[1:])
			print word
			ilen=len(word)
			jlen=len(newword)
			mylen=min(ilen,jlen)
			cnt=0
			while(cnt<3 and mylen-cnt>=0):
				if(word[:mylen-cnt]==newword[:mylen-cnt]):
					return newword,rest
				cnt+=1
	return False

def correction():
	oppcount=0	
	relcount=0
	fd=open('dictionary','rb')
	dic=pickle.load(fd)
	newdic={}
	for i in dic.keys():
		i=strip(i)
		newdic[i]=[[],[],[],[]]
		meaning=[]
		example=[]
		related={}
		opposite=[]
		for j in dic[i]:
			spl=specialForm(j)
			if(not spl):
				meaning.append(j)
				continue
			if(spl=='CF'):
				continue
			if(spl=='v'): spl='V'
			if(spl=='Ex'):
				example.append (' '.join(j.split('.')[1:]))
				continue
			elif(spl=='OP'):
				val=(' '.join(j.split('.')[1:]))
				if(val not in opposite):
					opposite.append(val)
			if(not related.has_key(spl)):
				related[spl]=[]
			elif(spl in ['V','N','v','ADJ','ADV']):
				if(j.find(' ')>=0):
					sparr=j.split(' ')
					if(len(sparr)==2):
						related[spl].append(sparr[1])
						continue
				word=selectDirect(j)
				print word
				if(word):
					exp=j.split(':')[1]
					if(word not in related[spl]):
						related[spl]=[]
					related[spl].append(word)
					meaning.append(exp)
				else:
					word=selectIndirect(i,j)
					print word
					if(word):
						word,exp=word[0],word[1]
						word=strip(word)
						if(word not in related[spl]):
							related[spl].append(word)
						meaning.append(exp)
					else:
						related[spl].append(i)
			else:
				val=(' '.join(j.split('.')[1:]))
				if(val not in related[spl]):
					related[spl].append(val)
		newdic[i][0]=meaning
		newdic[i][1]=example
		newdic[i][2]=related
		newdic[i][3]=opposite
		#print i,newdic[i]
		print oppcount
	print newdic
	for i in newdic.keys():
		for j in  newdic[i][2].keys():
		if(newdic[i][2][j]==[]):
			print i,j
	print newdic['eclectic']

