#USE : python beePrior.py (t) (t2) (csvfile) (outputfile-optional)



#imports

import pandas as pd
from datetime import datetime, timedelta
import sys

#function
## Look at events prior and classify based on y displacement


def beeCleanPrior(bee):

    id = bee['track_tagid'].iloc[0]

    new_event = []
    datetime = []
        
    for i in range(len(bee)-1):

            time = bee['track_endtime'].iloc[i]
            next_t = bee['track_starttime'].iloc[i+1]

            init = bee['track_starty'].iloc[i]

            #if time passed is greater than the threshold,
            #classify the last detection in an event
            if (next_t - time).total_seconds() > t:
                second = bee['track_endy'].iloc[i]
                matched = False
                counter = 1
                #iterate backwards until the distance threshold
                #is met or until they reach the first detection in
                #the event
                while not matched: 
                    if abs(second-init) > t2:
                        if second > init:
                            new_event.append('exiting')
                        else:
                            new_event.append('entering')
                        matched = True
                    elif (time - bee['track_starttime'].iloc[i-counter]).total_seconds() < t:
                        init = bee['track_starty'].iloc[i-counter]
                        counter += 1
                    else:
                        if second > init:
                            new_event.append('exiting')
                        else:
                            new_event.append('entering')
                        matched = True
                datetime.append(time)
                
                
            
    tagID = [id] * len(new_event)
    df = pd.DataFrame.from_dict({'tagID': tagID, 'datetime':datetime, 'event':new_event})
    return df
    

#obtain parameters from prompt

t = int(sys.argv[1])
t2 = int(sys.argv[2])
csvname = sys.argv[3]
if len(sys.argv) > 4:
    outputfile = sys.argv[4]
else:
    outputfile = "bee_prior.csv"
    
vdf = pd.read_csv(csvname)
vdf['track_endtime'] = vdf['track_endtime'].apply(lambda x: pd.to_datetime(x))
vdf['track_starttime'] = vdf['track_starttime'].apply(lambda x: pd.to_datetime(x))
vdf['track_tagid'] = vdf['track_tagid'].apply(lambda x: str(x))

#iterate over all bees in dataset and save to full dataframe

bees = []

beeIDs = vdf['track_tagid'].unique()
for bee in beeIDs:

    b = vdf[vdf['track_tagid'] == bee].copy().reset_index()
    events = beeCleanPrior(b)
    bees.append(events)
    
    
new = pd.concat(bees, axis = 0) 
new.to_csv(outputfile, index=False)
print(f"Saved to {outputfile}")