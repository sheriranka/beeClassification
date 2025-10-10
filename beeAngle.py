#USE : python beeAngle.py (t) (angle) (csvfile) (outputfile-optional)



#imports

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import sys

#function
## Look at events prior and classify based on y displacement


def beeCleanAngle(bee):

    id = bee['track_tagid'].iloc[0]
    new_event = []
    datetime = []
    vector_x = []
    vector_y = []

    
    enter_min = 180 + angle
    enter_max = 360 - angle
    exit_min = angle
    exit_max = 180 - angle
        
    
    for i in range(len(bee)-1):

            time = bee['track_endtime'].iloc[i]
            next_t = bee['track_starttime'].iloc[i+1]

            #obtain direction vector 
            #normalized to a magnitude of 1
            y1 = bee['track_starty'].iloc[i]
            y2 = bee['track_endy'].iloc[i]
            x1 = bee['track_startx'].iloc[i]
            x2 = bee['track_endx'].iloc[i]

            dx = x2-x1
            dy = y2-y1
            angle_deg = np.rad2deg(np.arctan2(dy, dx))
            unit_dx = np.cos(np.deg2rad(angle_deg))
            unit_dy = np.sin(np.deg2rad(angle_deg))

            vector_x.append(unit_dx)
            vector_y.append(unit_dy)
            
            #if next detection is further than the threshold,
            #utilize all stored angles to calculate event trajectory
            if (next_t - time).total_seconds() > t:
                #obtain average
                avg_x = sum(vector_x)/len(vector_x)
                avg_y = sum(vector_y)/len(vector_y)

                if avg_x == 0 and avg_y == 0:
                    deg = 0
                elif avg_x == 0 and avg_y != 0:
                    if avg_y > 0:
                        deg = 270
                    elif avg_y < 0:
                        deg = 90
                else:
                    # determine direction angle using arctan
                    deg = np.rad2deg(np.arctan(avg_y/avg_x))
                    
                    # since arctan limits are (-90,90), use coordinate directions to 
                    # correct the angle to be within standard [0,360) range
                    if avg_x > 0 and avg_y >= 0:
                        deg = deg
                    elif avg_x < 0 and avg_y >= 0:
                        deg = 180 + deg
                    elif avg_x < 0 and avg_y < 0:
                        deg = deg + 180
                    elif avg_x > 0 and avg_y < 0:
                        deg = 360 + deg

                #classify events based on angle threshold
                if deg >= exit_min and deg <= exit_max:
                    new_event.append('exiting')
                elif deg >= enter_min and deg <= enter_max:
                    new_event.append('entering')
                else:
                    new_event.append('unknown')
                datetime.append(time)
                vector_x = []
                vector_y = []
            
    tagID = [id] * len(new_event)
    df = pd.DataFrame.from_dict({'tagID': tagID, 'datetime':datetime, 'event':new_event})
    #print(bee)
    return df
    

#obtain parameters from prompt

t = int(sys.argv[1])
angle = int(sys.argv[2])
csvname = sys.argv[3]
if len(sys.argv) > 4:
    outputfile = sys.argv[4]
else:
    outputfile = "bee_angle.csv"
    
vdf = pd.read_csv(csvname)
vdf['track_endtime'] = vdf['track_endtime'].apply(lambda x: pd.to_datetime(x))
vdf['track_starttime'] = vdf['track_starttime'].apply(lambda x: pd.to_datetime(x))
vdf['track_tagid'] = vdf['track_tagid'].apply(lambda x: str(x))

#iterate over all bees in dataset and save to full dataframe

bees = []

beeIDs = vdf['track_tagid'].unique()
for bee in beeIDs:

    b = vdf[vdf['track_tagid'] == bee].copy().reset_index()
    events = beeCleanAngle(b)
    bees.append(events)
    
    
new = pd.concat(bees, axis = 0) 
new.to_csv(outputfile, index=False)
print(f"Saved to {outputfile}")