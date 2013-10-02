'''
This file is part of artcollector.

    Artcollector is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Artcollector is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Artcollector.  If not, see <http://www.gnu.org/licenses/>.
    
    brought to you by new deseret
'''


import urlparse
import urllib
import re
import string
import os
import easygui as eg
from bs4 import BeautifulSoup


def main():
	
	print "                        ___"
	print "                     .-'   `'."
	print "                    /         \\"
	print "                    |         ;"
	print "                    |         |           ___.--,"
	print "           _.._     |0) ~ (0) |    _.---'`__.-( (_."
	print "    __.--'`_.. '.__.\    '--. \_.-' ,.--'`     `""`"
	print "   ( ,.--'`   ',__ /./;   ;, '.__.'`    __"
	print "   _`) )  .---.__.' / |   |\   \__..--""  \"\"\"--.,_"
	print "  `---' .'.''-._.-'`_./  /\ '.  \ _.-~~~````~~~-._`-.__.'"
	print "        | |  .' _.-' |  |  \  \  '.               `~---`"
	print "         \ \/ .'     \  \   '. '-._)"
	print "          \/ /        \  \    `=.__`~-."
	print "          / /\         `) )    / / `"".`\\"
	print "    , _.-'.'\ \        / /    ( (     / /"
	print "     `--~`   ) )    .-'.'      '.'.  | ("
	print "            (/`    ( (`          ) )  '-;"
	print "             `      '-;         (-'"
	print " "
	print "                $_ ARTCOLLECTOR _$"
	print " "
	print "The following program is for saving the entire"
	print "collection of images associated with an artist"
	print "on wikipaintings.org to a diretory on your computer."
	print " "
	print "The URL you should enter is the url to the artist's page"
	print "i.e. something that looks like: "
	print "  http://www.wikipaintings.org/en/franklin-carmichael"
	print " "
	print "The highest quality images will be saved to the directory "
	print "you choose."
	print "\n"
	

	
	#url = "http://www.wikipaintings.org/en/ivan-milev"
	#save_dir = "/media/sage/Laura/Images/Wikipaintings Archive/Ivan Milev"
	
	url = raw_input("enter the artist page url:\n")
	save_dir = raw_input("enter the complete path to the save directory:\n")
	
	
	print ":::ART COLLECTION IN PROGRESS:::\n"
	
	url = url + "/mode/all-paintings/1"
	x = 1; #true while there are still more pages to save
	pg = 1; 
	
	#an image counter:
	#an array is used so that it can be mutated in savepage()
	imgcount = [0]
	
	#loop until a page is reached with no paintings
	while x:	
		url = re.sub("\d+", "", url) # delete digits from the end
		url = url + str(pg)	# add the pg number		
		print url
		
		#save all the HQ images from this page:
		x = savepage(url, save_dir, imgcount)
		pg = pg+1
		
	print ":::DOWNLOAD COMPLETE:::\n"
		

'''
'Saves each image (from url) in it's highest quality
'  to save_dir. imgcount is used to name the images.
'
'Returns 1 if at least one image was found on the page
'Returns 0 otherwise. 
'''
def savepage(url, save_dir, imgcount):
	
	#get the html as a string
	try:
		htmltext = urllib.urlopen(url).read()
	except:
		print "."
		
	validpg = 0;
	soup = BeautifulSoup(htmltext) #brew up some soup
	
	#loop through each img tag found in the html.
	for tag in soup.findAll('img',src=True):
		try:
			unparsed_img = tag['src'] # get the 'src' from this img tag.
			img = ''
			
			#check the img src for the correct format...
			if unparsed_img.startswith('http://uploads'):
				if unparsed_img.endswith('xlSmall.jpg'):						
					validpg = 1;
					img = unparsed_img[:-12] # delete the end of the url to get the link to the high quality img.
					#parse the url to create the file name:
					filename = img.replace("http://uploads", "")
					filename = filename.replace(".wikipaintings.org/images/", "")
					filename = filename[1:]
					filename = filename.replace("/", "_")
					filename = str(imgcount[0]) +" "+ filename
					
					#increment the imgcount and save the image to disk.
					imgcount[0] = imgcount[0]+1
							
					urllib.urlretrieve(img, os.path.join(save_dir, filename))	
					print filename
		except:
			#if there was a problem saving an image - just skip to the next one.
			print " "
			continue
			
	return validpg #return 1 if paintings were found on this page. 

if __name__ == "__main__":
    main()
