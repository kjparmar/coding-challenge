#!/usr/bin/env python

import sys
from decimal import Decimal

def main():
	#Open the files
	inputFile = open('E:\git\coding-challenge-repo\\test\\tweet_input\\tweets.txt','r')
	outputFile = open('E:\git\coding-challenge-repo\\test\\tweet_output\\ft2.txt', 'w')

	#Dictionary for storing tweets within 60 seconds
	tweetsWithin60Seconds = {}

	for line in inputFile:

		#If the entry doesn't contain a valid timestamp, ignore it
		timeStamp = line.split('"', 4)
		if timeStamp[3] == 'track':
			continue

		#Extract text of the tweet and remove unicode characters
		relevantText = line[line.find("\"text\":")+8:line.find("\",\"source")]			

		cleanText = relevantText.decode('unicode_escape').encode('ascii','ignore')
		cleanText = cleanText.replace("\/", "/")
		cleanText = cleanText.replace("\n", " ")
		cleanText = " ".join(cleanText.split())
			
		#Remove tweets from dictionary not within 60 seconds of incoming tweet
		tweetsWithin60Seconds = removeTweetsAbove60Seconds(tweetsWithin60Seconds, timeStamp[3])

		#Add incoming tweet to dictionary
		tweetsWithin60Seconds[cleanText] = timeStamp[3]
			
		#Calculate average degree of hash graph and write to file
		average = calculateAverageDegree(tweetsWithin60Seconds)
		outputFile.write(str(average)+'\n')
	
	inputFile.close();
	outputFile.close();

# This function scans the current dictionary of tweets and removes
# entries in the dictionary which are not within 60 seconds of the
# incoming tweet
def removeTweetsAbove60Seconds( presentDictionary, newTimeStamp ):
	#Extract hours,minutes and seconds for incoming tweet
	onlyTime = newTimeStamp.split(" ")
	timeStampParts = onlyTime[3].split(":")

	listOfDeletion = []
	for items in presentDictionary.values():
		#Extract hours,minutes and seconds for current entry in dictionary
		onlyItemTime = items.split(" ")
		timeParts = onlyItemTime[3].split(":")

		#If hours of both the times are not equal, add to list of deletion
		if timeStampParts[0] != timeParts[0]:
			listOfDeletion.append(items)

		#If difference of minutes of both the times is greater than 2, add to list of deletion
		elif (int(timeStampParts[1]) - int(timeParts[1])) > 2:
			listOfDeletion.append(items)

		#Otherwise, keep the entry in the dictionary as it is
		elif ((int(timeStampParts[1]) - int(timeParts[1])) < 2) and (int(timeStampParts[2]) < int(timeParts[2])):
			continue

	if len(listOfDeletion) > 0:
		presentDictionary = deleteFromDictionary(presentDictionary, listOfDeletion)

	#Handle case when dictionary becomes empty
	if presentDictionary == None:
		presentDictionary = {}

	return presentDictionary


# This function deletes the entry from the dictionary according to the 
# values obtained from list of deletion
def deleteFromDictionary( presentDictionary, listOfDeletion):
	for key in presentDictionary.keys():  
		if presentDictionary[key] in listOfDeletion:
			del presentDictionary[key]
 

# This function constructs the hash graph from the hash tags obtained from tweets 
# dictionary and calculates the average degree of the graph
def calculateAverageDegree( tweetsWithin60Seconds ):
	
	average = 0.00
	relevantTags = []

	#Obtain hash tags text from the text of the tweet
	for items in tweetsWithin60Seconds.keys():
		
		hashTagsParts = items.split('#')

		#Ignore entry if number of hash tags is less than 2
		if len(hashTagsParts) < 3:
			continue

		else:
			#Remove characters after whitespace in tag text
			#extracted
			for tags in hashTagsParts[1:]:
				tagWithoutSpace = tags.split(" ")[0]
				hashTagsParts.remove(tags)
				hashTagsParts.append(tagWithoutSpace.lower())

			relevantTags.append(hashTagsParts[1:])		
			
	#Create dictionary for hash graph
	tagsWithDegrees = {}

	#Populate the hash graph
	for items in relevantTags:
		for tag in set(items):
			if tag not in tagsWithDegrees: 
				tagsWithDegrees[tag] = len(items) - 1
			else:
				tagsWithDegrees[tag] = tagsWithDegrees[tag] + len(items) - 1

	#Calculate average degree of hash graph
	if len(tagsWithDegrees) != 0:
		average = round(Decimal(sum(tagsWithDegrees.values())) / len(tagsWithDegrees), 2)
	
	return average
		
if __name__ == '__main__':
	main()																																																																																																																																																									