from Graph import Graph
import osmium 
from collections import namedtuple

import json

Node = namedtuple('Node', ('id', 'lonlat'))
Way = namedtuple('Way', ('id', 'v1', 'v2'))

from loggibud.v1.types import Point

class CounterHandler(osmium.SimpleHandler):
  def __init__(self):
    osmium.SimpleHandler.__init__(self)
    self.nodes = []
    self.ways = []
    self.lonlat_hash = {}
    self.num_nodes = 0

  def node(self, n):
    node_id = n.id
    self.lonlat_hash[node_id] = Point(lng=n.location.lon, lat=n.location.lat)
    self.nodes.append(node_id)

  def way(self, w):
    way_id = w.id
    way = Way(way_id, w.nodes[0].ref, w.nodes[-1].ref)
    self.ways.append(way)


h = CounterHandler()
# p = "loggibud/v1/baselines/task_optimal_location/data/map.osm"
import os
p = os.path.abspath("loggibud/v1/baselines/task_optimal_location/data/rj.pbf")

from timeit import default_timer as timer
from datetime import timedelta
start = timer()

print("Applying files: ", timedelta(timer() - start))
h.apply_file(p)
print("Applying files done: ", timedelta(timer() - start))

g = Graph()
count = 0
for node in h.nodes:
  g.addVertex(node)


print("Adicionou os vertices")

from loggibud.v1.distances import calculate_distance_matrix_m, OSRMConfig
config = OSRMConfig()
# config.host = 'http://router.project-osrm.org'

# Point(lng=-38.763, lat=-12.444) Point(lng=-38.8002084, lat=-12.3693015)
count = 0
print("Creating graph: ", timedelta(timer() - start))

length_ways = len(h.ways)

for way in h.ways:
  count+=1
  v1Id = way[1]
  v2Id = way[2]
  v1 = h.lonlat_hash[v1Id]
  v2 = h.lonlat_hash[v2Id]

  print(way)
  matrix_distance = calculate_distance_matrix_m([v1, v2], config)
  g.addEdge(v1Id, v2Id, matrix_distance[0][1])

  
  # if count % 100000 == 0 or count <= 10:
  print(f"Count way {count} from {length_ways}")

print("Creating graph done: ", timedelta(timer() - start))


'''
      USANDO PICKLE
'''
import pickle
path = 'loggibud/v1/baselines/task_optimal_location/graph2.bin'

def serializePickle(data):
  with open(path, 'wb') as f:
    pickle.dump(data, f)


def deserializePickle():
  with open(path, 'rb') as f:
    return pickle.load(f)

print("Serializing graph: ", timedelta(timer() - start))
serializePickle(g)
g2 = deserializePickle()
print("Serializing graph done: ", timedelta(timer() - start))
# print(g2.vertexMap)


