import pickle
from spaceStrip import strip
def correctDictionary():
	fd=open('wordlist','rb')
	obj=pickle.load(fd)
	fd.close()
	newdic={}
	for i in obj.keys():
		meaning=obj[i]
		newmeaning=[]
		#LOL
		newarr=meaning.split(';')
		for k in newarr:
			if(k.find('\n')>=0):
				arr=k.split('\n')
				temp=''
				for j in arr:
					temp+=strip(j)+' '
				if(temp[-1]==' '):
					temp=temp[:-1]
				if(temp[0]==' '):
					temp=temp[1:]
				newmeaning.append(temp)
			else:
				newmeaning.append(strip(k))
		newdic[strip(i)]=newmeaning
	print newdic	
	fd=open('dictionary','wb')
	pickle.dump(newdic,fd)
	fd.close()

if(__name__=='__main__'):
	correctDictionary()
