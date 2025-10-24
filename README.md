## Classification algorithms for bees at the entrance to the hive to predict their trajectory.

### FILES

BeeClassify.ipynb -> Has all functions for user interactivity.

BeeCam-AprilTag.ipynb -> Application of the prior detection on BeeCam-AprilTag data.

beeActivity.csv -> File of all detections to be classified.

beeAngle.py -> Classify events utilizing summed vector angle function.

beePrior.py -> Classify events utilizing distance prior checking function.

beeSingleAngle.py -> Classify events utilizing only last angle of event.

cheatsheet.csv -> Manually corroborated event classification results

worker05.txt -> Data from BeeCam-AprilTag paper experiment.

month_data folder -> Same experiment with monthlong extracted data.

### USER-DEFINED VALUES

t -> User-defined seconds threshold to divide and combine detections into events.

t2 -> Distance that must be covered to classify an event.

angle -> Angle threshold (in degrees) for verifying the classification for an event.

### REQUIRED VALUES FOR INPUT CSV

beeAngle.py and beeSingleAngle.py require the following columns:

 - track_tagid
 - track_starty
 - track_endy
 - track_startx
 - track_endx
 - track_starttime
 - track_endtime

beePrior.py requires the following columns:

 - track_tagid
 - track_starty
 - track_endy
 - track_starttime
 - track_endtime

### HOW TO USE
```
python beePrior.py <t> <t2> <csvfilename> <outputfile-optional>
```

```
python beeAngle.py <t> <angle> <csvfilename> <outputfile-optional>
```

```
python beeSingleAngle.py <t> <angle> <csvfilename> <outputfile-optional>
```

### CREDITS

Summed vector angle function and worker05.txt was taken from BeeCam-AprilTag https://github.com/AERS-Lab/BeeCam-AprilTag
