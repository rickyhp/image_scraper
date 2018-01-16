import requests
from bs4 import BeautifulSoup
import os, errno
import argparse
import mimetypes

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input",
	help="path to the website to scrap images")
args = vars(ap.parse_args())

#r = requests.get("http://pythonforengineers.com/pythonforengineersbook/")
r = requests.get(args['input'])
data = r.text
soup = BeautifulSoup(data, "lxml")

folderName = args['input'].split('//')[1]

i = 1
for link in soup.find_all('img'):
        image = link.get("src")
        #question_mark = image.find("?")
        #image = image[:question_mark]
        #image_name = os.path.split(image)[1]
        #print(image_name)
        if 'http' not in image or 'https' not in image:
            image = 'http://' + folderName + '/' + image
        print('image url = ' + image)
        r2 = requests.get(image)
        content_type = r2.headers['content-type']
        extension = mimetypes.guess_extension(content_type)

        try:
            os.makedirs(folderName)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        with open(folderName+'/'+str(i)+extension, "wb") as f:
            f.write(r2.content)
            i = i + 1