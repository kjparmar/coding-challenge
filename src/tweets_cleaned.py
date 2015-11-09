#!/usr/bin/env python

import sys
def main():
	#Open both files
	inputFile = open(sys.argv[1],'r')
	outputFile = open(sys.argv[2], 'w')

	#Initialize counter for number of unicode character tweets
	counter = 0

	for line in inputFile:

		#Extract time stamp and relevant tweet text
		timeStamp = line.split('"', 4)
		relevantText = line[line.find("\"text\":")+8:line.find("\",\"source")]			
			
		#Increment counter if unicode character found
		if "\u" in relevantText:
			counter = counter + 1
				
		#Remove unicode characters
		cleanText = relevantText.decode('unicode_escape').encode('ascii','ignore')
		cleanText = cleanText.replace("\/", "/")
		cleanText = cleanText.replace("\n", " ")
		cleanText = " ".join(cleanText.split())

		outputFile.write(cleanText + ' (timestamp: ' + timeStamp[3] + ')\n')
			
	outputFile.write(str(counter) + ' tweets contained unicode.')
	
	inputFile.close();
	outputFile.close();

if __name__ == '__main__':
	main()