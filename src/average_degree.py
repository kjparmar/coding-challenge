#!/usr/bin/env python

import sys
from decimal import Decimal

def main():
	inputFile = open('E:\git\coding-challenge-repo\\test\\tweet_input\\tweets.txt','r')
	outputFile = open('E:\git\coding-challenge-repo\\test\\tweet_output\\ft2.txt', 'w')

	i = 0

	tweetsWithin60Seconds = {}

	for line in inputFile:

		timeStamp = line.split('"', 4)
		if timeStamp[3] == 'track':
			continue

		relevantText = line[line.find("\"text\":")+8:line.find("\",\"source")]			

		cleanText = relevantText.decode('unicode_escape').encode('ascii','ignore')
		cleanText = cleanText.replace("\/", "/")
		cleanText = cleanText.replace("\n", " ")
		cleanText = " ".join(cleanText.split())
			
		tweetsWithin60Seconds = removeTweetsAbove60Seconds(tweetsWithin60Seconds, timeStamp[3])

		tweetsWithin60Seconds[cleanText] = timeStamp[3]
			
		average = calculateAverageDegree(tweetsWithin60Seconds)
		outputFile.write(str(average)+'\n')
	
	inputFile.close();
	outputFile.close();


def removeTweetsAbove60Seconds( presentDictionary, newTimeStamp ):
	onlyTime = newTimeStamp.split(" ")
	timeStampParts = onlyTime[3].split(":")

	listOfDeletion = []
	for items in presentDictionary.values():
		onlyItemTime = items.split(" ")
		timeParts = onlyItemTime[3].split(":")

		if timeStampParts[0] != timeParts[0]:
			listOfDeletion.append(items)

		elif (int(timeStampParts[1]) - int(timeParts[1])) > 2:
			listOfDeletion.append(items)

		elif ((int(timeStampParts[1]) - int(timeParts[1])) < 2) and (int(timeStampParts[2]) < int(timeParts[2])):
			continue

	if len(listOfDeletion) > 0:
		presentDictionary = deleteFromDictionary(presentDictionary, listOfDeletion)

	if presentDictionary == None:
		presentDictionary = {}
	return presentDictionary


def deleteFromDictionary( presentDictionary, listOfDeletion):
	for key in presentDictionary.keys():  ## creates a list of all keys
		if presentDictionary[key] in listOfDeletion:
			del presentDictionary[key]
 

def calculateAverageDegree( tweetsWithin60Seconds ):
	
	average = 0.00
	relevantTags = []

	for items in tweetsWithin60Seconds.keys():
		
		hashTagsParts = items.split('#')

		if len(hashTagsParts) < 3:
			continue

		else:
			for tags in hashTagsParts[1:]:
				tagWithoutSpace = tags.split(" ")[0]
				hashTagsParts.remove(tags)
				hashTagsParts.append(tagWithoutSpace.lower())

			relevantTags.append(hashTagsParts[1:])		
			
	tagsWithDegrees = {}

	for items in relevantTags:
		for tag in set(items):
			if tag not in tagsWithDegrees: 
				tagsWithDegrees[tag] = len(items) - 1
			else:
				tagsWithDegrees[tag] = tagsWithDegrees[tag] + len(items) - 1

	if len(tagsWithDegrees) != 0:
		average = round(Decimal(sum(tagsWithDegrees.values())) / len(tagsWithDegrees), 2)
	
	return average
		
if __name__ == '__main__':
	main()																																																																																																																																																									