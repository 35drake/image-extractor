# This program rips Hero Academia chapters from the tcbscans website. Note their URL naming scheme isn't uniform for all chapters.
	# The program only can pull a certain amount of pages from a chapter. So, for a very long chapter (like the pilot), you'll have to tweak the code to make sure all the pages are gotten.
	# Fallen Angel scans for MHA start on Chapter 311. We can rip these images from their image URL's just like from earlier chapters, however these URL's are non-predictable and must be found by looking through the chapter's HTML code, which we'll access with Selenium.

import requests #Used to rip a photo from a URL
import os #used to create new folders; as each chapter will have its own folder of photos

# import selenium stuff so that we can search for image URL's from the FA chapters, since those image URL's are non-predictable
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


# This function formats a number as a string with a certain amount of digits (it places zeroes in front when needed)
def format_num(digits,number):
	my_output = str(number)
	for count in range(2): #Add a "0" string in front of the number's string, up to twice since I know digits < 4
		if len(my_output) < digits:
			my_output = "0" + my_output
	return my_output


# This function finds the url for a chapter. 
def url_find(chapter):
	driver = webdriver.Chrome()
	# This is the chapter directory's URL
	driver.get("https://tcbscans.com/mangas/6/my-hero-academia?date=18-2-2024-12")
	my_html = driver.page_source
	my_index = my_html.find("academia-chapter-413")
	if my_index == -1 :
		exit("\nError: the chapter link wasn't found in the chapter directory webpage.")
	# Find where the relevant part of the desired url starts. NOTE: the url of the chapter we want looks like this: https://tcbscans.com/chapters/?/my-hero-academia-chapter-321. Where the ? is a random number that we don't know, which could be any number of digits.
	current_index = my_index
	while True:
		current_index = current_index - 1
		if my_html[current_index : current_index + 10] == "/chapters/":
			driver.close()
			break
	return("https://tcbscans.com" + my_html[current_index:my_index+20])


# This function finds all the FA url's (this is a dev tool). DONT USE THIS ANYMORE
def url_find_all():
	driver = webdriver.Chrome()
	# This is the chapter directory's URL
	driver.get("https://tcbscans.com/mangas/6/my-hero-academia?date=18-2-2024-12")
	unused_var = input()
	my_html = driver.page_source
	with open("HTML-homepage.txt", "w") as my_file:
		my_file.write(my_html)	
	
	for chapter in range(312,415):
		my_index = my_html.find("academia-chapter-"+str(chapter))
		if my_index == -1 :
			exit("\nError: the chapter link wasn't found in the chapter directory webpage.")
		# Find where the relevant part of the desired url starts. NOTE: the url of the chapter we want looks like this: https://tcbscans.com/chapters/?/my-hero-academia-chapter-321. Where the ? is a random number that we don't know, which could be any number of digits.
		current_index = my_index
		while True:
			current_index = current_index - 1
			if my_html[current_index : current_index + 10] == "/chapters/":
				driver.close()
				break
		chapter_url = "https://tcbscans.com" + my_html[current_index:my_index+20]
		print(chapter_url)



def get_chapter_url(chapter):
	with open('HTML - homepage.txt', 'r') as my_file:
	    my_html = my_file.read()
	# print(my_html)

	my_index = my_html.find("academia-chapter-"+str(chapter))
	if my_index == -1 :
		exit("\nError: the chapter link wasn't found in the chapter directory webpage.")
	# Find where the relevant part of the desired url starts. NOTE: the url of the chapter we want looks like this: https://tcbscans.com/chapters/?/my-hero-academia-chapter-321. Where the ? is a random number that we don't know, which could be any number of digits.
	current_index = my_index
	while True:
		current_index = current_index - 1
		if my_html[current_index : current_index + 10] == "/chapters/":
			break
	chapter_url = "https://tcbscans.com" + my_html[current_index:my_index+20]
	return(chapter_url)

# This function gets all the image URLs for you from some TCBScans chapter of MHA. It returns a list.
# Currently (since the url list of the chapter's webpages is pre-generated), this is the only function that uses Selenium.
def get_image_urls(chapter):
	my_return = [] # this is the list of chapter URLs


	# my_url = "https://tcbscans.com/chapters/7607/my-hero-academia-chapter-" + format_num(3,chapter)
	my_url = get_chapter_url(chapter)
	print("The url for chapter", chapter, "is", my_url)

	# Load the chapter's webpage
	driver = webdriver.Chrome()
	driver.get(my_url)	

	print("\nWebpage loading command has been executed.\n")
	
	my_html = driver.page_source
	
	print("\nHTML code has been loaded as a string of length", len(my_html) )
	# with open("HTML.txt", "w") as my_file:
	#	my_file.write(my_html)	
	# print("\nThe code has been written into a HTML.txt if you want to look at it.\n")

	# Gonna add the next page's URL to my_return[], over and over till the next page doesn't exist (aka we've done the final page)
	current_page = 0
	while True: 
		current_page = current_page + 1
		my_index = my_html.find("My Hero Academia Chapter "+ format_num(3,chapter) + " Page " + str(current_page))
	
		if my_index == -1:
			# Failure; this image doesn't exist therefore we've already done the final image and are done findings this chapter's page URLs
			print("\nPage", str(current_page), "does not exist.\n")
			break
		else: #success; the desired page we're looking for does exist (i.e. page 19)
			# Find the beginning of the desired page image url
			index_thats_checking_for_src = my_index
			while my_html[index_thats_checking_for_src : index_thats_checking_for_src + 3] != "src" :
				index_thats_checking_for_src = index_thats_checking_for_src - 1
			index_thats_checking_for_src = index_thats_checking_for_src + 5
			print(index_thats_checking_for_src)
			
			# Find the end of the desired page image url
			index_thats_checking_for_alt = my_index
			while my_html[index_thats_checking_for_alt : index_thats_checking_for_alt + 3] != "alt" :
				index_thats_checking_for_alt = index_thats_checking_for_alt - 1
			index_thats_checking_for_alt = index_thats_checking_for_alt - 2
			print(index_thats_checking_for_alt)
		
			page_url = my_html[index_thats_checking_for_src : index_thats_checking_for_alt ]
			my_return = my_return + [page_url]
	
		# driver.close() 
	return(my_return)




# USE THIS FUNCTION ONLY FOR FA CHAPTERS.
# Rips the photos from the chapter (integer) argument, and puts them in a folder
def chapter_rip_FA(chapter):
	print("Doing chapter",str(chapter))
	os.system("mkdir "+ format_num(3,chapter)) #create a self-titled folder for this chapter's photos
	
	print("\nNow attempting to get the image url's from this chapter.\n")
	# First, get a list of all the image URL's from this chapter. This length of this list will tell you how many iamges/pages there are.
	image_urls = get_image_urls(chapter)
	print("Here's a list of this chapter's image URLs:",image_urls)
	for page in range(0,len(image_urls)):
		my_url = image_urls[page] #use the current page's URL
		print("Current image url is",image_urls[page] )
		# Get the image
		img_data = requests.get(my_url).content
		# Decide what to save the image as
		my_file_location = format_num(3,chapter) + "/" + format_num(2,page) + ".jpg"
		# Save the image
		with open(my_file_location, 'wb') as handler:
		    handler.write(img_data)
		
		# delete the photo file you just created if it is blank (so you must've had an invalid url, probably cuz that chapter didn't have the max number of pages)
		if os.path.getsize(my_file_location) < 1000: #Any real jpg file is unlikely to be smaller than 1000bytes
			os.chdir(format_num(3,chapter)) #change to the folder that contains the undesired blank photo
			os.system("del " + format_num(2,page) + ".jpg" ) #For some reason i can't get Windows terminal to delete a file that's inside a directory
			os.chdir("..")




# Rips the photos from the chapter (integer) argument, and puts them in a folder
def chapter_rip(chapter):
	print("Doing chapter",str(chapter))
	os.system("mkdir "+ format_num(3,chapter)) #create a self-titled folder for this chapter's photos
	# Iterate to pull each page from the chapter; the url's should be predictable and static
	for page in range(0,30+1): #just put how many max pages you think there'll be, plus one. Note that I started the range at 0 because sometimes the TCB website has 0-based numbering for its photos
		
		# The url is slightly different on chapter 311 onwards, since the Fallen Angels fanscan is available (which I want) for those		
		if chapter < 311:
			my_url = "https://cdn.onepiecechapters.com/file/CDN-M-A-N/bnahtcb_" + str(chapter) + "_" + format_num(2,page) + ".jpg" #I used my function for the page but not the chapter. That was just to comply with how this website does their URL system.
		else:
			exit("Error: use the function chapter_rip_FA() to rip chapters 311 and beyond.")
			# my_url = "https://cdn.onepiecechapters.com/file/CDN-M-A-N/bnha_" + str(chapter) + "_" + format_num(2,page) + ".png" #I used my function for the page but not the chapter. That was just to comply with how this website does their URL system.

		# Get the image
		img_data = requests.get(my_url).content
		# Decide what to save the image as
		my_file_location = format_num(3,chapter) + "/" + format_num(2,page) + ".jpg"
		# Save the image
		with open(my_file_location, 'wb') as handler:
		    handler.write(img_data)
		
		# delete the photo file you just created if it is blank (so you must've had an invalid url, probably cuz that chapter didn't have the max number of pages)
		if os.path.getsize(my_file_location) < 1000: #Any real jpg file is unlikely to be smaller than 1000bytes
			os.chdir(format_num(3,chapter)) #change to the folder that contains the undesired blank photo
			os.system("del " + format_num(2,page) + ".jpg" ) #For some reason i can't get Windows terminal to delete a file that's inside a directory
			os.chdir("..")




# Ask the user which mode to run in
my_mode = input("Ripping Fallen Angels chapters? Note: this is recommended for chapters 311 and beyond. (Y/n) ")

# Ask the user which chapters to pull
start_chapter = int( input("Which chapter to start on? ") )
end_chapter =  int( input("Which chapter to end on? (inclusive) ") )

# Rip the pages for each chapter in the range that the user gave
for chapter in range(start_chapter, end_chapter+1):
	if my_mode == "Y" or my_mode == "y":
		print("FA chapter\n")
		chapter_rip_FA(chapter)
	else:
		chapter_rip(chapter)