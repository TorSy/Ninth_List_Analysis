'''
Created on 13 Sep 2017

@author: Tor Eivind Syvertsen
'''

if __name__ == '__main__':
    pass

mypath = r'C:\Users\Tor Eivind Syvertsen\My Documents\LiClipse Workspace\Tournament_data\lists_by_land'


import os
import re

def combine_lists(mypath):
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    
    os.chdir(mypath)
    for filename in onlyfiles:
        with open(filename,'r') as f:        
            content = f.read()
            with open('all_lists.txt','a') as f1:        
                f1.write(content)
            
            
            
def find_all_max_length_rows(filename='all_lists.txt'):
    n=0
    with open(filename,'r') as f:
        contents = f.read()
        f.seek(0)
        for row in f:
            n+=1
            order = 124 #for example
            words=re.findall(r'^.{%s}' % (order), row)
            if len(words)>0:
                print n,words
                #if insert_newline is True:                
                    #NOT IMPLEMENTED: DO MANUALLY
                                            
                        
                    
                    
 
find_all_max_length_rows()