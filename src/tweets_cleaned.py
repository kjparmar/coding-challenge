#!/usr/bin/env python

import sys

def main():
	inputFile = open('E:\git\coding-challenge-repo\\test\\tweet_input\\tweets.txt','r')
	outputFile = open('E:\git\coding-challenge-repo\\test\\tweet_output\\ft1.txt', 'w')

	counter = 0

	for line in inputFile:

		timeStamp = line.split('"', 4)
		relevantText = line[line.find("\"text\":")+8:line.find("\",\"source")]			
			
		if "\u" in relevantText:
			counter = counter + 1
				
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