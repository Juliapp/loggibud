from json.decoder import JSONDecodeError
import os
import json
from random import random

def findOneCoordById(cvrp_path):
  
  list_dirs = os.listdir(cvrp_path)

  coords = []
  keys = []
  for dir_name in list_dirs:
    dir_id = dir_name[0:2]

    if not dir_id in keys:
      path = os.path.join(cvrp_path, dir_name)

      for root, dirs, files in os.walk(path):
        if files:
          file_name = os.path.join(path, files[0])
          cvrp = json.load(open(file_name))
          
          keys.append(dir_id)
          origin = cvrp['origin']
          coords.append({'key': dir_id, "lat": origin['lat'], "lng": origin['lng']})
          break

  return coords

def getLoggiRegions():
  """
  This function is designated to get the Loggi's working area around Brazil.
  It uses CVRPInstance files provided by Loggibud project (Available at https://github.com/loggi/loggibud)
  getting one file by region and then getting only one distribution build 
  ("Hub coordinates, where the vehicles originate." -https://github.com/loggi/loggibud/blob/master/docs/quickstart.md)
  """
  cvrp_path = "data/cvrp-instances-1.0/dev"
  modified_in = os.path.getmtime(cvrp_path)

  cache_path = 'loggibud/v1/baselines/task_optimal_location/utils/regions_cache'
  try:
    with open( cache_path , 'r') as cache_file:
        jsonFile = json.load(cache_file)
        
        if 'modified_in' in jsonFile:
          if jsonFile['modified_in'] == modified_in:
            return jsonFile['coords']
  except JSONDecodeError:
    pass
  except FileNotFoundError:
    pass

  cache_file = open( cache_path, 'w')
  jsonFile = {}
  coords = findOneCoordById(cvrp_path)
  jsonFile['modified_in'] = modified_in
  jsonFile['coords'] = coords

  cache_file.truncate(0)
  cache_file.write(json.dumps(jsonFile))

  return coords

def jsonBytesConverter(data):
  return data


def regionDeliveries(paths, percentage):
  points = {}
  for path in paths:
    for json_file in os.listdir(path): 
      if json_file.endswith('.json'):
        with open(os.path.join(path, json_file)) as f:
            data = json.load(f)
            for delivery in data['deliveries']:
              #ensure to return just a percend of the dataset
              if random() <= percentage:
                # Preventing duplicated values
                point = pointFormat(delivery['point'])
                key = delivery['id']
                points[key] = point

  return list(points.values())

def regionOrigins(paths, percentage):
  points = {}
  for path in paths:
    for json_file in os.listdir(path): 
      if json_file.endswith('.json'):
        with open(os.path.join(path, json_file)) as f:
            data = json.load(f)
            # Preventing duplicated values
            point = pointFormat(data['origin'])
            key = json.dumps(point, sort_keys=True)
            points[key] = point
  return list(points.values())


def pointFormat(point):
  DECIMAL_DIGITS_LEN = 7
  factor = 10.0 ** DECIMAL_DIGITS_LEN
  lat = int(point['lat'] * factor)/factor
  lng = int(point['lng'] * factor)/factor
  return {"lat":lat,"lng":lng}
