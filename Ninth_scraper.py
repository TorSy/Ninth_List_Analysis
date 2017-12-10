'''
Created on 18 May 2017

@author: Tor Eivind Syvertsen
'''

if __name__ == '__main__':
    pass

from bs4 import BeautifulSoup

import requests

link = 'https://www.the-ninth-age.com/index.php?thread/5939-sa-public-playtesting-comments/&pageNo=5'

f  = requests.get(link)

soup = BeautifulSoup(f.text) #or f.content

'''TO PRINT ENTIRE SOUP'''
#for link in soup.find_all('a'):
    #print(link.get('href'))
#suppeText = soup.findAll('div', {"class":"messageText"})
all_messages = soup.find_all("div", class_="messageText")

ctr =0
for msg in all_messages:
    ctr+=1
    a = msg.get_text()
    a.replace(' ','')
    print a
    with open('msg'+str(ctr)+'.txt','w') as f:
        f.write(a)            


