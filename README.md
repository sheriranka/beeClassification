## Classification algorithms for bees at the entrance to the hive to predict their trajectory.

### FILES

BeeClassify.ipynb -> Has all functions for user interactivity.

beeActivity.csv -> File of all detections to be classified.

bee_angle.csv -> Classified events utilizing summed vector angle function.

bee_prior.csv -> Classified events utilizing distance prior checking function.

bee_singleangle.csv -> Classified events utilizing only last angle of event.

comparisonresults.txt -> Manually corroborated event classification result comparisons for randomly chosen differences. Was manually checked by observing numbers and not video data.

### USER-DEFINED VALUES

t -> User-defined seconds threshold to divide and combine detections into events.

t2 -> Distance that must be covered to classify an event.

angle -> Angle threshold for verifying the classification for an event.

