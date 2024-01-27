# Importing all the required modules
import json
from collections import defaultdict
from string import capwords
import csv
from datetime import date
from pprint import pp

# loading our data from a .json file to perform further operations
data = json.load(open("Data\\30DayQuakes.json","r"))
dataset = data['features']
# To test if data is imported sucessfully...
# pp(dataset[:10])

# To clear output file for new input
with open("Output\\Output.txt", 'w+') as output:
    output.write("")

# A function to find the total number of actual earthquakes.
def total_quake():
    actual_eq = sum(datapoint['properties']['mag'] is not None and datapoint['properties']['type']=='earthquake' for datapoint in dataset)
    with open("Output\\Output.txt", 'a+') as output:
        output.write(f"The total number of earthquakes are: {data['metadata']['count']}. \n")
        output.write(f"The total number of actual earthquakes after removing data anomalies are: {actual_eq}. \n\n")
    return

# To find the place with maximum impact.
def max_impact():
    def if_felt(datapoint):
        felt = datapoint['properties']['felt']
        return 0 if felt is None else float(felt)
    value = max(dataset, key = if_felt)
    with open("Output\\Output.txt", 'a+') as output:
        output.write(f"The place of maximum impact based on cases is: {value['properties']['place']}; where {value['properties']['sig']} people were affected. \n\n")
    return

# To find the Most and Least significant earthquake
def mag_range():
    def get_mag(datapoint):
        mag = datapoint['properties']['mag']
        return 0 if mag is None else float(mag)
    maxmag, minmag = max(dataset, key=get_mag), min(dataset, key=get_mag)
    maxmag, maxplace, minmag, minplace = maxmag['properties']['mag'], maxmag['properties']['place'], minmag['properties']['mag'], minmag['properties']['place']
    with open("Output\\Output.txt", 'a+') as output:
        output.write("The magnitude range of earthquakes are as follows: \n")
        output.write(f"The Largest earthquake with magnitude {maxmag} took place at {maxplace}.\n")
        output.write(f"The Smallest earthquake with magnitude {minmag} took place at {minplace}.\n")
        output.write(f"Range of Magnitude - {(maxmag-abs(minmag))}.\n\n")
    return

# To find activities that were not earthquakes.
def not_quakes():
    def false_quakes(datapoint):
        return True if datapoint['properties']['type']!='earthquake' else False
    with open("Output\\Output.txt", 'a+') as output:
        output.write("The alerts that were false positive are as follows:\n")
        for case in list(filter(false_quakes, dataset)):
            output.write(f"{case['properties']['place']} (Reason - {case['properties']['type']})\n")
    return

# To find reason for data anamolies in earthquake records.
def reason():
    Data_eq, i = defaultdict(int), 1
    for datapoint in dataset:
        Data_eq[datapoint['properties']['type']] += 1
    with open("Output\\Output.txt", 'a+') as output:
        output.write("\nThe reasons for data anomalies in earthquake records are as follows:\n")
        for datapoint in Data_eq.items():
            if datapoint[0] != 'earthquake':
                output.write(f"Reason({i}): '{capwords(datapoint[0])}'  Count: {datapoint[1]}\n")
                i+=1

# To find if there were any earthquakes based on number of people affected and their count
def felt_quakes(affected):
    found = any(datapoint['properties']['felt'] is not None and datapoint['properties']['felt']>=affected for datapoint in dataset)
    with open("Output\\Output.txt", 'a+') as output:
        if not found:
            output.write("\nNo, the number of people affected were less.\n")
            return
        output.write(f"\nYes, there were earthquakes felt by more than {affected} people:\n")
        total = sum(datapoint['properties']['felt'] is not None and datapoint['properties']['felt']>affected for datapoint in dataset)
        output.write(f"Total number of these earthquakes: {total}.\n\n")

# To find top earthquakes based on magnitude
def top_quake(num):
    def get_mag(datapoint):
        mag = datapoint['properties']['mag']
        return 0 if mag is None else float(mag)
    sorted_dataset = sorted(dataset, key=get_mag, reverse=True)
    with open("Output\\Output.txt", 'a+') as output:
        output.write(f"Top {num} Places based on largest earthquakes:\n")
        for i in range(num):
            output.write(f"Place: {sorted_dataset[i]['properties']['place']} | Magnitude: {sorted_dataset[i]['properties']['mag']}\n")
    return

# To find vital information about earthquakes with certain magnitude criteria
def certain_quake(minimum_mag):
    def correctmag(datapoint):
        return datapoint['properties']['mag'] is not None and datapoint['properties']['mag']>=minimum_mag
    result = list(filter(correctmag, dataset))
    def transformag(datapoint):
        return {
            "Place":datapoint['properties']['place'],
            "Magnitude":datapoint['properties']['mag'],
            "Time":date.fromtimestamp(datapoint['properties']['time']/1000),
            "Type":datapoint['properties']['type']
        }
    final = list(map(transformag, result))
    with open("Output\\Output.txt", 'a+') as output:
        output.write(f"\nImportant information of earthquakes where magnitude is greater than {minimum_mag}:\n")
        for i in final:
            output.write(f"{i}\n")
    return

# To save vital data of earthquakes in a json file.
def save_data():
    def mag5(datapoint):
        return datapoint['properties']['mag'] is not None and datapoint['properties']['type']=='earthquake'
    def extract(datapoint):
        d = datapoint['properties']
        return {
            'Place': d['place'],
            'Magnitude': d['mag'],
            'Time': str(date.fromtimestamp(d['time']/1000)),
            'Data': d['url']
        }
    result = list(filter(mag5, dataset))
    result = list(map(extract, result))
    with open("Output\\EQ_data.json", "w", encoding='utf-8') as file:
        json.dump(result, file, indent=4)
    pp(json.load(open('Output\\EQ_data.json','r')))
    return

# To save most significant events based on time with location to a csv file.
def save_data_location(n):
    def sig(dataset):
        sig = dataset['properties']['sig']
        return 0 if sig is None else sig
    sorted_dataset = sorted(dataset, key= sig, reverse=True)
    top_n = sorted_dataset[:n]
    sorted_top_40 = sorted(top_n, key= lambda val:val['properties']['time'], reverse=True)

    rows = [['Place', 'Magnitude', 'Cases', 'Date', 'Location']]
    for row in sorted_top_40:
        s = row['properties']
        felt = str(s['sig']) if s['sig'] is not None else 0
        long = row['geometry']['coordinates'][0]
        lat = row['geometry']['coordinates'][1]
        link = f"https://maps.google.com/maps/search/?api=1&query={lat}%2C{long}"
        rows.append([
            s['place'],
            s['mag'],
            felt,
            str(date.fromtimestamp(s['time']/1000)),
            link
        ])
    with open("Output\\EQ_location_data.csv", 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(rows)
    file = csv.reader(open("Output\\EQ_location_data.csv",'r'))
    next(file)
    for row in file: pp(row)
    return

total_quake()
max_impact()
mag_range()
not_quakes()
reason()
felt_quakes(200)
top_quake(10)
certain_quake(6)
save_data()
save_data_location(20)
