import json
import xml.etree.ElementTree as ET
import geopy.distance

isochrone_input_file = "input/wroclaw22-30min.xml"

def parse_tomtom_data_xml(data):
    """
    Calculates maximum reachable distance in km from the center. Based on TomTom isochrones.
    """
    xml_namespace = {'tomtom': 'http://api.tomtom.com/routing'}
    center_element = data.findall('.//tomtom:center', xml_namespace)[0]
    center_lat = center_element.get('latitude')
    center_lon = center_element.get('longitude')
    center = (float(center_lat), float(center_lon))
    points = []
    for point in data.findall('.//tomtom:point', xml_namespace):
        latitude = point.get('latitude')
        longitude = point.get('longitude')
        points.append((float(latitude), float(longitude)))

    return (center, points)


def calculate_distance(center, point):
    return geopy.distance.distance(center, point).km

def main():
    with open(isochrone_input_file) as input:
        data = ET.parse(input).getroot()
        (center, points) = parse_tomtom_data_xml(data)
    
    max_distance = 0
    for point in points:
        distance = calculate_distance(center, point)
        if distance > max_distance:
            max_distance = distance

    print("max distance: " + str(max_distance))



if __name__ == "__main__": main()
