'''
Created on 12 Sep 2017

@author: Tor Eivind Syvertsen
'''
from numpy import ceil

if __name__ == '__main__':
    pass

import os
import Levenshtein
import pandas as pd

class parse_search_file:
    def __init__(self,filename=None,search=None,score_crit=None):        
        '''
        filename with extension
        search  can be string or list of strings
        score_crit can be integer or list of integers               
        '''
        self.search = search
        self.score_crit = score_crit
        self.filename = filename
        self.search_string = search
        self.score_crit = score_crit
        self.count=0
    
    def search_file(self):
        
        self.result_di = dict()
        '''If searching for several'''
        if type(self.search) is list:
            assert type(self.score_crit is list)
            assert len(self.score_crit)==len(self.search_string),'length of score_crit and search_string lists not equal'
            
            for search_item,crit_item in zip(self.search,self.score_crit):                
                self.inner_search(search_string=search_item,score_crit=crit_item)
                
                #add to result dict
                #self.result_di[search_item+'_'+str(crit_item)]=self.resultFrame
                self.result_di[search_item]=self.resultFrame
                print self.result_di
            
            '''if single string search'''      
        elif type(self.search) is str:              
            self._inner_search_(search_string=self.search,score_crit=self.score_crit)
            print self.resultFrame
            self.result_di[self.search] = self.resultFrame
                
    
    def frame_to_csv(self,resultfile=None,mode='w'):
        assert resultfile is not None
        for key in self.result_di:            
            dataframe = self.result_di[key]
            dataframe.to_csv(resultfile,sep=';',mode=mode)
            
    def frame_to_excel(self,resultfile=None):
        assert resultfile is not None
        writer = pd.ExcelWriter(resultfile)
        for key in self.result_di:            
            dataframe = self.result_di[key]            
            dataframe.to_excel(writer,key,encoding='utf-8')     
        writer.save() 
    
    
    def inner_search(self,search_string,score_crit):                   
        
        
        count = 0        
        line_li = list()        
        row_li = list()
        score_li = list()
        
        
        '''parse'''
        with open(self.filename,'r') as file:
            for n,line in enumerate(file):
                N = n+1
                max_words = len(search_string.split())
                words = line.split()
                N_words = len(words)
                '''Create new rows'''
                
                if N_words>0: #exept blank rows   
                    N_new_rows = max(1,N_words-max_words+1)
                    #print N_new_rows,N_words 
                    for iter_N in range(0,N_new_rows):
                        newLine = ' '.join(words[iter_N:iter_N+max_words])                         
                        '''Levenstein fuzzy search'''
                        score = Levenshtein.ratio(newLine, search_string)            
                        if score>score_crit:
                            
                            #print self.count,newLine,score,N
                            count +=1
                            self.count +=1
                            score_li.append(score)
                            row_li.append(N)
                            line_li.append(unicode(newLine, 'utf-8'))
        

        self.resultFrame= pd.DataFrame.from_items([('line', line_li), ('score', score_li),('row',row_li)])        
    


