def strip(word):
	small=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
	big=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','(','"',"'"]
	alpha=small
	alpha.extend(big)
	ind=0
	while ind<(len(word)):
		if(word[ind]  in alpha):
			break	
		ind+=1
	word=word[ind:]
	if(word==''):return ''
	ind=len(word)-1
	alpha.extend(['.','!','?',';'])
	while ind>=0:
		if(word[ind] in alpha):
			break
		ind-=1
	word=word[:ind+1]
	return word

if(__name__=='__main__'):
	print "RESULT:"+strip('  geneila  ')+":END"
	print "RESULT:"+strip(' arun has no b reain')+":END"
