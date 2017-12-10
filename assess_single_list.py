'''
Created on 18 Sep 2017

@author: Tor Eivind Syvertsen
'''

if __name__ == '__main__':
    pass

import re
import pandas as pd
from find_units import find_units_from_line
import Levenshtein

list_file = 'msg18.txt'
DB_loc = r'XL_DVH'
res_file = 'BetaResFile.xlsx'

def load_from_xl(xlname):
    pdframe = pd.read_excel(io=xlname)
    return pdframe

def frame_to_excel(pdframe,resultfile=None):
    assert pdframe is not None
    writer = pd.ExcelWriter(resultfile)
    pdframe.to_excel(writer,encoding='utf-8')     
    writer.save() 

def give_subpart_of_frame(pdframe,key,tag):
    assert pdframe is not None
    subframe= pdframe[pdframe[key]==tag]
    return subframe


def find_match(pdframe,search_key,output_col,tag):
        df_SPECIFIC = give_subpart_of_frame(pdframe,key=search_key,tag=tag)
        output = df_SPECIFIC[output_col].values.tolist()
        output = output[0]
        return output
        
     
        
'''LOAD DIMENSIONS INTO FRAMES'''
df_DIM_FACTION=load_from_xl(DB_loc + '\DIM_FACTION.xlsx')
df_DIM_UNITS =load_from_xl(DB_loc + '\DIM_UNITS.xlsx')
df_BRG_UNIT_SEARCH = load_from_xl(DB_loc + '\BRG_UNIT_SEARCH.xlsx')

'''ESTABLISH RESULT FRAME'''
columns = ['country_tag','player ID','row', 'text','search string','faction','faction_tag','unit','Organization','unit_score','cost','n_units','n_models','special_rules']
res_frame = pd.DataFrame(columns=columns)

'''Read ETC file line for line and fill result frame'''
#initialize
country_tag = None
faction_tag = None
rowN_in_file = 0
rowN_in_res = 0
player_id = 1

'''
PRINT ALL UNIT DIMENSIONS TO RES TABLE
'''
for index, row in df_DIM_UNITS.iterrows():
    rowN_in_res +=1
    unit = row['unit_name']
    org =  row['organization']
    faction_tag = row['faction_key_f']
    faction_name = find_match(df_DIM_FACTION,'FA_KEY_P','faction_name',faction_tag)          
    save_list = ['',None ,rowN_in_res,'','',faction_name,faction_tag,unit,org,1,0,0,0,'']
    res_frame.loc[rowN_in_res-1] = save_list
'''
GO THROUGH TOURNAMENT LIST
'''
 
 
with open(list_file) as f:
    for text_line in f:
        toSave = True
        rowN_in_file +=1       
        
        if 'TAG' in text_line:
            country_tag=text_line.split()[1]
            print country_tag        
            faction_tag=text_line.split()[2]     
            print faction_tag                               
            faction_name = find_match(df_DIM_FACTION,'FA_KEY_P','faction_name',faction_tag)            
            player_id +=1
            

        if country_tag is not None and faction_tag is not None:
            df_DIM_UNITS_SPECIFIC = give_subpart_of_frame(df_DIM_UNITS,key='faction_key_f',tag=faction_tag)
            df_BRG_UNITS_SPECIFIC = give_subpart_of_frame(df_BRG_UNIT_SEARCH,key='faction_key_f',tag=faction_tag)

            
            res_dict = find_units_from_line(
                                line=text_line, 
                                unit_list = df_BRG_UNITS_SPECIFIC['search_string'].values.tolist(), 
                                crit_list = df_BRG_UNITS_SPECIFIC['criteria'].values.tolist()
                                 )
            if res_dict['unit'] is not None:
                '''find the unit in BRG matching the search string'''     
                unit = find_match(df_BRG_UNITS_SPECIFIC,'search_string','unit_name',res_dict['unit'])
                '''find the unit in DIM matching the unit'''
                organization =find_match(df_DIM_UNITS_SPECIFIC,'unit_name','organization',unit)                                                             
                cost = res_dict['cost']
                n_units = res_dict['N_units']
                n_models = res_dict['N_models']
                score = res_dict['score']
                search_string = res_dict['search_string']
               
                special_rules= ''
                
                if len(re.findall('#',text_line))>0:
                    print 'OMITTED: ' + text_line
                    toSave = False
                
                '''cast to unicode'''
                save_list = [unicode(country_tag, 'utf-8'),player_id ,rowN_in_file,unicode( text_line, 'utf-8'),search_string,faction_name,faction_tag,unit,organization,score,cost,n_units,n_models,unicode( special_rules, 'utf-8')]                                                            
                '''append'''
                if toSave:
                    rowN_in_res +=1
                    res_frame.loc[rowN_in_res] = save_list               
                 

frame_to_excel(res_frame,resultfile=res_file)
print 'completed'


