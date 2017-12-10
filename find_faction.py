'''
Created on 13 Sep 2017

@author: Tor Eivind Syvertsen
'''

if __name__ == '__main__':
    pass

from Parse_and_search import parse_search_file


def insert_faction_tag(tag,dataframe,exclude_list):
    filename1 = 'all_lists.txt'        
    
        
               
    for row,line in zip(dataframe['row'],dataframe['line']):   
        if line not in exclude_list:
            with open(filename1) as f:
                contents = f.readlines()
                f.close()
                contents.insert(row, 'ROOSTER_START_FACTION '+tag+' ')
            f1 = open(filename1, "w")
            contents = "".join(contents)
            f1.write(contents)
            f1.close()         
        else:
            pass

        
        

def write_faction_list():
    
    filename = 'all_lists.txt'
    
    factions_d = {
        'BH':{'Beast Herds':0.8,'Beastherds':0.80},
        'DL':{'Daemon Legions':0.8},
        'DR':{'Dread Elves':0.95},
        'DH':{'Dwarven Holds':0.90},
        'EoS':{'Empire of Sonnstahl':0.74},
        'HE':{'Highborn Elves':0.9,'Born Elves':0.9},
        'IF':{'Infernal Dwarves':0.85},
        'KoE':{'Kingdom of Equitaine':0.9,'KOE':0.9},
        'OK':{'Ogre Khans':0.9,'Ogre Kingdoms':0.90},
        'O&G':{'Orcs and Goblins':0.85,'OaG':0.60},
        'SA':{'Saurian Ancients':0.8,'Saurian Army':0.90},  
        'SE':{'Sylvian Elves':0.9},
        'VS':{'Vermin Swarm':0.9},
        'UD':{'Undying Dynasties':0.8},
        'VC':{'Vampire Covenant':0.79},
        'WoTDG':{'Warriors of the Dark Gods':0.9,'WotDG':0.9}           
        }

    factions_d2 = {
        'Beast Herds':'BH',
        'Beastherds':'BH',
        'Daemon Legions':'DL',
        'Dread Elves':'DE',
        'Dwarven Holds':'DH',
        'Empire of Sonnstahl':'EoS',
        'Highborn Elves':'HE',
        'Born Elves':'HE',
        'Infernal Dwarves':'ID',
        'Kingdom of Equitaine':'KoE',
        'KOE': 'KoE',
        'Ogre Khans':'OK',
        'Ogre Kingdoms':'OK',
        'Orcs and Goblins':'O&G',
        'OaG':'O&G',
        'Saurian Ancients':'SA',
        'Saurian Army':'SA', 
        'Sylvian Elves':'SE',
        'Vermin Swarm':'VS',
        'Undying Dynasties':'UD',
        'Vampire Covenant':'VC',
        'Warriors of the Dark Gods':'WoTDG',
        'WotDG':'WoTDG'           
        }   

    '''STRUCTURE DATA INTO LIST'''
    search_li = list()
    crit_li = list()    
    
    for faction_code in factions_d:
        for search_string in factions_d[faction_code]:
                               
            search_li.append(search_string)
            crit_li.append(factions_d[faction_code][search_string])
    
    
    
    
    '''SEARCH AND PARSE'''
    ETC = parse_search_file(filename,search_li,crit_li)
    ETC.search_file()   
    ETC.frame_to_excel(resultfile='faction.xlsx')
    
    
    exclude_list=[
        'Vampire Count',
        'Vampire Count:',
        'Vampire Count,',
        '*Vampire Count,',
        'KEG'
            ]

    
    '''INSERT TAGS'''
    n=0
    for key in ETC.result_di:                        
        tag=factions_d2[key]
        dataframe = ETC.result_di[key]
        insert_faction_tag(tag,dataframe,exclude_list)
        n+=1
    
    
    
    
write_faction_list()
