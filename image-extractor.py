# This program rips Hero Academia chapters from the tcbscans website. Note their URL naming scheme isn't uniform for all chapters.

import requests #Used to rip a photo from a URL
import os #used to create new folders; as each chapter will have its own folder of photos

# This function formats a number as a string with a certain amount of digits (it places zeroes in front when needed)
def format_num(digits,number):
	my_output = str(number)
	for count in range(2): #Add a "0" string in front of the number's string, up to twice since I know digits < 4
		if len(my_output) < digits:
			my_output = "0" + my_output
	return my_output

# Rip the photos from each chapter
for chapter in range(7,130+1): #choose your chapter range
	print("Doing chapter",str(chapter))
	os.system("mkdir "+ format_num(3,chapter))	
	for page in range(1,30+1): #just put how many max pages you think there'll be, plus one
		my_url = "https://cdn.onepiecechapters.com/file/CDN-M-A-N/bnahtcb_" + str(chapter) + "_" + format_num(2,page) + ".jpg" #I used my function for the page but not the chapter. That was just to comply with how this website does their URL system.
		img_data = requests.get(my_url).content
		my_file_location = format_num(3,chapter) + "/" + format_num(2,page) + ".jpg"
		with open(my_file_location, 'wb') as handler:
		    handler.write(img_data)
		
		# delete the photo file you just created if it is blank (so you must've had an invalid url, probably cuz that chapter didn't have the max number of pages)
		if os.path.getsize(my_file_location) < 1000: #Any real jpg file is unlikely to be smaller than 1000bytes
			os.chdir(format_num(3,chapter)) #change to the folder that contains the undesired blank photo
			os.system("del " + format_num(2,page) + ".jpg" ) #For some reason i can't get Windows terminal to delete a file that's inside a directory
			os.chdir("..")


