from loggibud.v1.baselines.task_optimal_location.utils.OLDistances import (
  OLDDistanceMatrix,
  OLDRouteDistance,
  OLDDistanceMatrixGC,
  OLDRouteDistanceGC
)

from loggibud.v1.baselines.task_optimal_location.utils.regions import (
  regionDeliveries,
  regionOrigins,
)
from loggibud.v1.types import Point
import os

def resolve_location_id(id: str):
  if id == 'test':
    return [os.path.join("tests/test_instances")]

  instances_dir = "./data/cvrp-instances-1.0/dev"

  paths = [
    os.path.join(instances_dir, path)
    for path in os.listdir(instances_dir) if path.startswith(id)
  ]

  if len(paths) == 0:
    raise ValueError("Location ID not found. Please provide a valid ID.")

  return paths


def resolve_candidates(args):
  size = len(args)
  if size == 0:
    raise ValueError("Candidates not provided. Please insert a list of candidates.")

  candidates = [Point(lat=candidate["lat"], lng=candidate["lng"]) for candidate in args]
  
  return (candidates, len(args))

def resolve_calc_method(calc_method):
  valid_calc_methods = ["distance_matrix", "route_distance", "distance_matrix_great_circle", "route_distance_great_circle"]

  if calc_method == None:
    calc_method = "distance_matrix_great_circle"

  if not calc_method in valid_calc_methods:
    raise ValueError(f"Invalid calc_method. The method should be one of the: {valid_calc_methods}, and if not provided distance_matrix_great_circle will be setted by default.")

  if calc_method == 'distance_matrix':
    old = OLDDistanceMatrix()
  elif calc_method == 'route_distance':
    old = OLDRouteDistance()
  elif calc_method == 'distance_matrix_great_circle':
    old = OLDDistanceMatrixGC()
  elif calc_method == "route_distance_great_circle":
    old = OLDRouteDistanceGC()
    
  return old

def resolve_K(k, len_candidates):
  if k == None:
    return 1
  if k < 0:
    raise ValueError("K must greater than 0.")
  if k > len_candidates:
    raise ValueError("K must be positive and greater than the number of candidates.")

  return k

def resolve_algorithm(param):
  if(param == "minmax"):
    from loggibud.v1.baselines.task_optimal_location.minmax import solve
    return solve
  elif(param == "minsum"):
    from loggibud.v1.baselines.task_optimal_location.minsum import solve
    return solve

  raise ValueError("Invalid algoritm. Please provide a valid algoritm.")

def resolve_point_type(param):
  if not param in ["deliveries", "hubs"]:
    raise ValueError("Invalid Point Type. Please provide a valid point type.")

  if param == "deliveries": return regionDeliveries
  if param == "hubs": return regionOrigins
  
def resolve_region_data_percentage(percentage):
  if percentage == None:
    return 1

  try:
    percentage = float(percentage)
  except ValueError:
    raise ValueError("Percentage must be a float")

  if percentage < 0 or percentage > 1:
    raise ValueError("Percentage must greater than 0 and lower than 1.")

  return percentage