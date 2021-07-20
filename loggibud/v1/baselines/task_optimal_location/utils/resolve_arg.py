from loggibud.v1.baselines.task_optimal_location.utils.OLDistances import (
  OLDDistanceMatrix,
  OLDRouteDistance,
  OLDDistanceMatrixGC,
  OLDRouteDistanceGC
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

  if not size % 2 == 0:
    raise ValueError("The number of coordinates must be even.")

  candidates = []

  for i in range(0, size, 2):
    candidates.append(Point(lat=args[i], lng=args[i+1]))
  
  return (candidates, size/2)

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

def resolve_response(message, content_name=False, content=False):
  response = {}
  response["message"] = message

  if(content_name and content):
    response["content_name"] = content

  return response

def resolve_algorithm(param):
  if(param == "minmax"):
    from loggibud.v1.baselines.task_optimal_location.minmax import solve
    return solve
  elif(param == "minsum"):
    from loggibud.v1.baselines.task_optimal_location.minsum import solve
    return solve

  raise ValueError("Invalid algoritm. Please provide a valid algoritm.")
  

def resolve_solver_response(solution):
  current = solution["currentSolution"]
  for key, value in current.items():
    if isinstance(value, Point):
      solution["currentSolution"][key] = [value.lng, value.lat]

  kSol = solution["kSolution"]
  for i, val in enumerate(kSol):
    for j, value in val.items():
      if isinstance(value, Point):
        solution["kSolution"][i][j] = [value.lng, value.lat]
        
  return solution

  