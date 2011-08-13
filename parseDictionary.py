import sys
import urllib2
from spaceStrip import strip
# -*- coding: iso-8859-15 -*-
def processWord(word):
	arr=word.split('\n')
	value=' '.join(arr)
	return strip(value)
def processMeaning(string):
	delim='luna-Ent">'
	pos=string.find(delim)
	#print pos
	endpos=string.find('div class="Lsentnce"')
	if(endpos>=0):
		string=string[pos+len(delim):endpos]
	else:
		string=string[pos+len(delim):]
	arr=[]
	exarr=[]
	while(string.find(delim)>=0):
		state=0
		current=''
		pos=string.find(delim)
		#print pos
		string=string[pos+len(delim):]
		meaning=''
		for i in string:
			if(state==0):
				if(i=='<'):
					if(state==1):
						print "BULLSHIT"
					if(current):
						#print current
						if not('{' in current or '}' in current or ']' in current or '}' in current):
							meaning+=(current+' ')
#					#print meaning
					current=''
					state=1
				else:
					current+=i
			elif(state==1):
				if(i=='>'):
					if(state==0):
						print "BULLSHIT"
					state=0
					#print current
					if(current=='div class="luna-Ent"' or current=='div class="Lsentnce"' or current=='a class="less"' or current=='a class="more"' or current=='style type="text/css"' or current=='script type="text/javascript"' or current=='div class="pbk"'):
						#print "break"
						if(current=='div class="Lsentnce"'):
							print "HECK \nHECK"*3
							return [arr,exarr]
						if(meaning.find(':')>=0):
							splitArr=meaning.split(':')
							#meaning=splitArr[0].split(';')
							meaning=splitArr[0]
							example=processWord(splitArr[1])
							tempArr=example.split(';')
							for ex in tempArr:
								exarr.append(ex)
						#else:
						#	meaning=meaning.split(';')
						#for words in meaning:		
						#	arr.append(processWord(words))
						arr.append(processWord(meaning))
						break
					current=''
				else:
					current+=i	
	return [arr,exarr]
def processSynonym(string):
	delimiter='<div class="hd">Synonyms'
	pos=string.find(delimiter)
	#print pos
	arr=[]
	if(pos<0):
		return []
	string=string[pos+len(delimiter):]
	state=0
	current=''
	for i in string:
		if(state==0):
			if(i=='<'):
				if(state==1):
					print "BULLSHIT"
				if(current and not current=="\n"):
#					print current
					arr.append(current)
#					print meaning
				current=''
				state=1
			else:
				current+=i
		elif(state==1):
			if(i=='>'):
				if(state==0):
					print "BULLSHIT"
				state=0
				#print current
				if(current=='/span'):
					#print "break"
					break
				current=''
			else:
				current+=i	
	return arr	

def getEntry(word):
	fd=urllib2.urlopen('http://www.dictionary.com/browse/'+word)
	string=fd.read()
	arr1=processMeaning(string)
	arr2=processSynonym(string)
	newarr=[arr1[0],arr1[1],arr2]
	print "DEBUG",newarr
	return newarr

if(__name__=='__main__'):
	fd=urllib2.urlopen('http://www.dictionary.com/browse/'+sys.argv[1])
	string=fd.read()
	arr1=processMeaning(string)
	arr2=processSynonym(string)
	newarr=[arr1[0],arr1[1],arr2]
	print newarr
print "HI"
