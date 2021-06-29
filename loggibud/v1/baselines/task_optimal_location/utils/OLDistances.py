from dataclasses import dataclass
from loggibud.v1.types import Point
from loggibud.v1.distances import (
  calculate_distance_matrix_m,
  calculate_route_distance_m,
  calculate_distance_matrix_great_circle_m,
  calculate_route_distance_great_circle_m,
  OSRMConfig
)

@dataclass
class OLDistance:
  pointsHashTable = {}

  def distance(self, origin: Point, destination: Point):
    raise NotImplementedError("Method must be implemented")


@dataclass
class OLDDistanceMatrix(OLDistance):
  def __init__(self):
    super().__init__()
    self.calc_func = calculate_distance_matrix_m

  def config_api(self, **kwargs):
    self.osrm_config = OSRMConfig()

    if kwargs.host:
      self.osrm_config.host = kwargs.host

    if kwargs.timeout:
      self.osrm_config.timeout_s = kwargs.timeout
      
    self.has_config = True

  def distance(self, origin: Point, destination: Point):
    if not (origin, destination) in self.pointsHashTable:
      if self.has_config:
        self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination], self.osrm_config)[0][1]
      else:
        self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination])[0][1]

    return self.pointsHashTable[(origin, destination)]

@dataclass
class OLDRouteDistance(OLDistance):
  def __init__(self):
    super().__init__()
    self.calc_func = calculate_route_distance_m

  def config_api(self, **kwargs):
    self.osrm_config = OSRMConfig()

    if kwargs.host:
      self.osrm_config.host = kwargs.host

    if kwargs.timeout:
      self.osrm_config.timeout_s = kwargs.timeout
      
    self.has_config = True

  def distance(self, origin: Point, destination: Point):
    if not (origin, destination) in self.pointsHashTable:
      if self.has_config:
        self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination], self.osrm_config)
      else:
        self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination])

    return self.pointsHashTable[(origin, destination)]

@dataclass
class OLDDistanceMatrixGC(OLDistance):
  def __init__(self):
    super().__init__()
    self.calc_func = calculate_distance_matrix_great_circle_m

  def distance(self, origin: Point, destination: Point):
    if not (origin, destination) in self.pointsHashTable:
      self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination])[0][1]

    return self.pointsHashTable[(origin, destination)]

@dataclass
class OLDRouteDistanceGC(OLDistance):
  def __init__(self):
    super().__init__()
    self.calc_func = calculate_route_distance_great_circle_m

  def distance(self, origin: Point, destination: Point):
    if not (origin, destination) in self.pointsHashTable:
      self.pointsHashTable[(origin, destination)] = self.calc_func([origin, destination])

    return self.pointsHashTable[(origin, destination)]




