# Quakes
## A core python data analysis project on earthquakes.
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Earthquake_-_The_Noun_Project.svg/1024px-Earthquake_-_The_Noun_Project.svg.png" width="200" height="100">

### Data
The source data is stored in **Data** folder as a .json file which contains important fields like magnitude, place, link, detail, cases, significance, type, coordinates, etc.
We will use this data to draw various conclusions and perform analysis.
The data is obtained from https://www.usgs.gov/programs/earthquake-hazards.

### Output
The results are stored in **Output** folder named *EQ_data.json*, *EQ_location.csv*, *Output.txt* each for diffrent set of analysis performed.

### Analyze.py
This is the main python file that contains various cases and code.
We have used **json**, **collections**, **string**, **csv**, **datetime**, **pprint** libraries.

**Functions:**
* *total_quake()* To find the total number of actual earthquakes after removing anomalies.
* *max_impact()* To find the place with maximum cases registered.
* *mag_range()* To find the Most and Least significant earthquake and the magnitude range.
* *not_quakes()* To find activities that were not earthquakes but got falsely registered in device.
* *reason()* To find reason for data anamolies in earthquake records and the count for each.
* *felt_quakes()* To find if there were any earthquakes based on number of people affected and if yes, how many. Takes an integer input as the minimum number of people affected.
* *top_quake()* To find top earthquakes based on magnitude. Takes an integer input as the number of records returned.
* *certain_quake()* To find vital information about earthquakes with atleast certain magnitude criteria. Takes an integer input as the minimum magnitude of earthquakes.
* *save_data()* To save vital data of earthquakes in a json file. Saves data in >Output/*EQ_data.json*
* *save_data_location()* To save most significant events based on time with location derived from google API with the help of longitude and latitude to a csv file. Sorts data first based on cases and then based on time. Takes integer input as the total number of records returned. Saves data in >Output/*EQ_location.csv*
