'''
Created on 13 Sep 2017

@author: Tor Eivind Syvertsen
'''

import Levenshtein
import re

if __name__ == '__main__':
    pass


def find_points(line):
    cost = None

    def _pattern_single(pattern,line):
        cost = re.findall(pattern,line)
        if len(cost)>0 and type(cost[0]) is str:
            return cost[0]            
        elif len(cost)>0 and type(cost[0]) is tuple:
            return cost[0][0]                                    
        else:
            return None


    ''' @ 100.0 pts'''
    if cost is None:
        cost=_pattern_single(r'(@ \d\d\d)(pts)',line)
    '''1000pts'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d\d)(pts)',line)
    '''1000'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d\d)',line)
    '''100pts'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d)(pts)',line)
    '''100 pts'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d )(pts)',line)
    '''80pts'''
    if cost is None:
        cost=_pattern_single(r'(\d\d)(pts)',line)
    '''1000'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d\d)',line)
    '''100'''
    if cost is None:
        cost=_pattern_single(r'(\d\d\d)',line)    
    '''80'''
    if cost is None:
        cost=_pattern_single(r'(\d\d)',line)

    return cost

def find_config(line):
    #Returns models and units
    N_models = None; N_units= None

    def _pattern_single(pattern,line):
        models = re.findall(pattern,line)
        if len(models)>0:
            return models[0][0]
        else:
            return None

    def _pattern_double(pattern,line):
        models = re.findall(pattern,line)
        if len(models)>0:
            #return units,models
            return models[0][0], models[0][2]
        else:
            return None,None

    '''2 x 20'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)( x )(\d\d)',line)
    '''2x 20'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)(x )(\d\d)',line)
    '''2 x20'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)( x)(\d\d)',line)
    '''2x20'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)(x)(\d\d)',line)
    '''2 x 2'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)( x )(\d)',line)
    '''2x 2'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)(x )(\d)',line)
    '''2x2'''
    if N_models is None:
        N_units, N_models=_pattern_double(r'(\d)(x)(\d)',line)
    '''10x'''
    if N_models is None:
        N_models=_pattern_single(r'(\d\d)(x)',line)
    '''10 x '''
    if N_models is None:
        N_models=_pattern_single(r'(\d\d )(x)',line)
    '''7*  <- UNITS''' 
    if N_models is None and N_units is None :
        N_units=_pattern_single(r'(\d)([\\*])',line)
    '''7 *  <- UNITS'''
    if N_models is None and N_units is None :
        N_units=_pattern_single(r'(\d )([\\*])',line)
    '''7 x  <- UNITS'''    
    if N_models is None:
        N_units=_pattern_single(r'(^\d )(x)',line)
    '''7x <-'''
    if N_models is None:
        N_models=_pattern_single(r'(^\d)(x)',line) #start of line to avoid spells..
    '''80 '''
    if N_models is None:
        N_models=_pattern_single(r'(^\d\d)( )',line)
    '''8 '''
    if N_models is None:
        N_models=_pattern_single(r'(^\d )',line)

    if N_units is None:
        N_units = 1
    
    if N_models is None:
        N_models = 1 
    


    return N_units, N_models

def search_line(line,search_string,score_crit):
        unit_detail_D = dict()
        unit_detail_D['unit']=None
        unit_detail_D['cost']=None
        unit_detail_D['N_models']=None
        unit_detail_D['N_units']=None
        
        unit = None; cost = None; N_models=None; N_units=None
        words = line.split()
        N_words = len(words)
        max_words = len(search_string.split())
        '''Create new rows'''

        if N_words>0: #exept blank rows
            N_new_rows = max(1,N_words-max_words+1)
            #print N_new_rows,N_words
            for iter_N in range(0,N_new_rows):
                newLine = ' '.join(words[iter_N:iter_N+max_words])
                newLine =unicode(newLine,'utf-8')
                '''Levenstein fuzzy search'''
                
                score = Levenshtein.ratio(newLine, search_string)

                if score>score_crit:
                    unit= search_string
                    score_saved = score
                    search_string_saved = newLine
                    
                    '''UPDATE TO MAKE SURE ONLY BETTER MATCH GETS SAVED'''
                    score_crit = score


            if unit is not None:
                cost = find_points(line)
                N_units, N_models = find_config(line)
                
                unit_detail_D = dict()
                unit_detail_D['unit']=unit
                unit_detail_D['cost']=cost
                unit_detail_D['N_models']=N_models
                unit_detail_D['N_units']=N_units
                unit_detail_D['score'] = score_saved
                unit_detail_D['search_string'] = search_string_saved
                
                
        return unit_detail_D 


def find_units_from_line(line,unit_list,crit_list):
    '''send inn en line og to lister, returner et dictionary med info'''
    assert len(unit_list)==len(crit_list)
    
    ''' iterer over lista'''
    for crit,unit in zip(crit_list,unit_list):
        unit_detail_D = search_line(line=line, search_string=unit, score_crit=crit )
                
        '''foer tilbake None's hvis den ikke finner noe'''
        if unit_detail_D['unit'] is not None:
            return unit_detail_D
            break
    
    return {'unit':None}
    
    
        
        
        
    
