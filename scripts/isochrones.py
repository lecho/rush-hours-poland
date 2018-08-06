import json
import xml.etree.ElementTree as ET
from geojson import Polygon
from catmull_rom import interpolateCatmulRomeSpline

isochrone_input_file = "input/wroclaw22.here.json"
isochrone_output_file = "output/wroclaw22.here.geo.json"

def parse_tomtom_data_json(data):
    coordinates = []
    for lat_lon in data['reachableRange']['boundary']:
        coordinates.append((lat_lon['longitude'], lat_lon['latitude']))

    interpolatedCoords = interpolateCatmulRomeSpline(coordinates)
    interpolatedCoords.append(interpolatedCoords[0])
    outerPolygon = []
    outerPolygon.append(interpolatedCoords)
    return Polygon(outerPolygon)

def parse_tomtom_data_xml(data):
    xml_namespace = {'tomtom': 'http://api.tomtom.com/routing'}
    coordinates = []
    for point in data.findall('.//tomtom:point', xml_namespace):
        longitude = point.get('longitude')
        latitude = point.get('latitude')
        coordinates.append((float(longitude), float(latitude)))

    interpolatedCoords = interpolateCatmulRomeSpline(coordinates)
    interpolatedCoords.append(interpolatedCoords[0])
    outerPolygon = []
    outerPolygon.append(interpolatedCoords)
    return Polygon(outerPolygon)

def parse_here_data(data):
    for isoline in reversed(data['data']['response']['isoline']):
        coordinates = []
        for ind in range(0, len(isoline['component'][0]['shape'])):
            if ind % 2 == 1:
                coordinates.append((isoline['component'][0]['shape'][ind], isoline['component'][0]['shape'][ind-1]))
    
    outerPolygon = []
    outerPolygon.append(coordinates)
    return Polygon(outerPolygon)

def main():
    with open(isochrone_input_file) as input:
        # data = ET.parse(input).getroot()
        data = json.load(input)

    # geo_json = parse_tomtom_data_xml(data)
    # geo_json = parse_tomtom_data_json(data)
    geo_json = parse_here_data(data)

    with open(isochrone_output_file, 'w') as output:
        output.write(str(geo_json))


if __name__ == "__main__": main()