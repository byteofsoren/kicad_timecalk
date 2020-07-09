# kicad_timecalk
This tool summarise the time spent on each KiCAD project from time stamps in one of the KiCAD files.

The `config.yaml  contains all project and points to the kicad files that contains the stamps.

The stamps in the kicad file should look like tihs:
```
Jun09:
12:30 - 14:00 Worked on the PDB.
```
This tool then looks for those specific tags and sumerice the time for each project.
Then when you have billed for a certain time you just add a marker in the file saying

```
Jun24
#Billed for 39 hours
```
The next time it is time to bill the previous time is discounted.
NOTE: this only works for whole hours right now.


