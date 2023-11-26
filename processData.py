import geolocatorClass
import folium
from folium.plugins import GroupedLayerControl

#m = folium.Map([47.64, 24.43], zoom_start=4)

iconDict = {"Dori":{"icon":"fish", "color":"blue"},
            "Peti":{"icon":"tree", "color":"green"}}

geo = geolocatorClass.Geolocator()


def addMarker(fg, location, popup):
    folium.CircleMarker(
        location=location,
        radius=3,
        color="red",
        #fill_color="red",
        popup=popup
    ).add_to(fg)

def getWhos(data):
    res = list()
    for i in data:
        res.append(i["who"])
    return list(set(res))

def getYears(data, who):
    res = list()
    for i in data:
        if i["who"] == who:
            res.append(i["year"])
    return list(set(res))


def readData(filePath):
    #
    #  output:
    #    [{"year":"2022", "coordinate": ["27.23", "16.62"], "popup":"popup text", "who":"Peti"},
    #     {"year":"2023", "coordinate": ["27.23", "16.62"], "popup":"popup text", "who":"Peti"}]
    #


    with open(filePath, encoding='utf-8') as f:
        lines = f.readlines()

    data = list()
    for line in lines[1:]:
        #print(line.strip().split(';'))
        where, startDate, endDate, who, comment = line.strip().split(';')

        lat, lon = geo.geocode(where)

        if startDate == endDate:
            popupText = {"date": startDate, "dateText": startDate, "comment": comment}
        else:
            popupText = {"date": startDate, "dateText": startDate + "&nbsp;-&nbsp;" + endDate, "comment":comment}
        
        for w in who.split(','):
            data.append({"year":startDate.split('.')[0],
                         "coordinate":[lat, lon], 
                         "where":where,
                         "popup":popupText,
                         "who":w.replace(' ',''),
                         "extendedPopup":[popupText]})

    return data

def processPopup(data):
    res = ''    
    data = sorted(data, key=lambda d: d['date']) 
    for i in data:
        res += i["dateText"] + "&nbsp;-&nbsp;" + i["comment"].replace(" ", "&nbsp;") + "<br>"
    return res



data = readData('database.csv')
#print(data)
#data = ['a','b','c','d']
for i in range(len(data)+1):
    for j in range(i+1, len(data)):
        #print(i,j)
        #print('    ', data[i], data[j])
        #print(data[i]['coordinate'], data[j]['coordinate'])
        if data[i]['coordinate'] == data[j]['coordinate'] and data[i]['who'] == data[j]['who']:
            #print(data[i])
            data[j]["extendedPopup"].append(data[i]["popup"])
            data[i]["extendedPopup"].append(data[j]["popup"])
        
#print(data)    


    




#print(data)
for who in sorted(getWhos(data)):

    m = folium.Map([47.64, 24.43], zoom_start=4)

    idx = 0
    dataFG = list()
    for year in sorted(getYears(data, who)):
        fg = folium.FeatureGroup(name=year, show=True).add_to(m)
        for i in data:
            if i["who"] == who and i["year"] == year:
                if i["coordinate"][0] != None:
                    popup = processPopup(i["extendedPopup"])
                    popup = "<b>"+i["where"].replace(" ", "&nbsp;")+"</b><br>"+popup
                    addMarker(fg, i["coordinate"], popup)
        
        dataFG.append({"who":who, 
                       "year":year, 
                       "featureGroup":fg})


    folium.LayerControl().add_to(m)
    m.save(who+"_map.html")


