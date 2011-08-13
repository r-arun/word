import pickle
from spaceStrip import strip
fd=open('dictionary','rb')
obj=pickle.load(fd)
newdict={}
for i in obj.keys():
	meaning=obj[i]
	newstruct={}
	newstruct['meaning']=[]
	newstruct['Ex']=[]
	others={}
	for j in meaning:
		if(j.find('.')>=0):
			pre=j.split('.')[0]
			if(pre.find(' ')<0):
				if(pre=='Ex'):
					newstruct['Ex'].append(j)
				elif(pre in ['N','V','ADJ','ADV','v','n']):,'PL','SG']):
					suf=j.split('.')
					if(len(suf)==1):
						appendent=i
					elif(j.split(' ')==2):
						appendent=j.split(' ')[1]
					else:
						if(suf[1].find(':')>=0):
							appendent=strip(suf[1].split(':')[0])
							j=' '.join(suf[1].split(':')[1:])
					if(others.has_key(pre)):
						if(len(suf)==1):
							others[pre].append(i)
						others[pre].append(j)
					else:
						if(len(suf)==1):
							others[pre].append(i)
						others[pre]=[j]
				else:
					newstruct['meaning'].append(j)
					
						
