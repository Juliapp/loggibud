import math
from heapq import heappush, heappop

class Graph:
  def __init__(self):
    self.vertexMap = dict()           

  def addVertex(self, v):
    self.vertexMap[v] = dict()

  def removeVertex(self, v):  
    if v in self.vertexMap:
      for (i,j) in self.vertexMap[v].copy():
        print(f"e->{(i,j)}")
        self.removeEdge(i,j)
      del self.vertexMap[v]

  def vertices(self):    
    return list(self.vertexMap.keys())

  def adjacents(self, v):
    return [j for (i, j) in self.outgoing(v)]   

  def addEdge(self, u,v,data):
    if (u in self.vertexMap) and (v in self.vertexMap):
      self.vertexMap[u][(u,v)] = data
      self.vertexMap[v][(v,u)] = data
    else:
      raise ValueError(f"One or both of the V {u} and {v} are not present in the Graph!")  

  def removeEdge(self,u,v):
    if ((u,v) in self.vertexMap[u]) and ((v,u) in self.vertexMap[v]):
      del self.vertexMap[u][(u,v)]      
      del self.vertexMap[v][(v,u)]  

  def edges(self):
    ret = []
    for e in self.vertexMap.values():
      if len(e.keys()):
        ret.extend(list(e.keys()))
    return ret

  def getEdge(self,u,v):
    return self.vertexMap[u][(u,v)]

  def outgoing(self, v):
    return list(self.vertexMap[v].keys())  

  def outdegree(self, v):
    return len(self.vertexMap[v])

  def incoming(self, v):
    return [(j,i) for (i,j) in self.vertexMap[v]] 

  def indegree(self, v):
    return len(self.vertexMap[v])

  def path(self, v):
    ret = ""
    visited = set()
    visited.add(v)
    stack = []
    stack.append((v,None))
    while stack:
      (v, p) = stack.pop()
      if p:        
        ret+=f"{p}--{self.getEdge(p,v)}--{v}  "
              
      for u in self.adjacents(v):        
        if u not in visited:          
          visited.add(u)          
          stack.append((u,v))

    return ret.strip() 

def dfs(G,v):
  return dfsRec(G,v,set(),[])

def dfsRec(G,v,visited,dfsList):  
  visited.add(v)  
  for u in G.adjacents(v):
    if u not in visited:      
      dfsList.append(u)
      dfsRec(G,u,visited,dfsList)  
  return dfsList  
  
def bfs(G,v):
  bfsList = []
  queue = [v]
  visited = set()
  visited.add(v)  
  while len(queue):
    e = queue.pop(0)
    for u in G.adjacents(e):
      if u not in visited:
        queue.append(u)
        visited.add(u)    
        bfsList.append(u)
  return bfsList    

def dijkstra(G,v,u):
  paths = dict()
  heap = [(0, v, None)]
  while len(heap):
    (dist, c, p) = heappop(heap)
    if c == u:
      paths[c] = (p,dist)
      return shortestPath(v,u,paths)

    if c not in paths:
      paths[c] = (p,dist) 
      for a in G.adjacents(c):
        distVA = dist + G.getEdge(c,a)
        if (a not in paths) or distVA < paths[a][1]:
          heappush(heap, (distVA, a, c))

def shortestPath(v,u,paths):
  L = []
  while v != u:
    (p,dist) = paths[u]
    L.insert(0,u)
    u  = p
  L.insert(0,u)    
  return L
         

def kruskals(G):
  H = []
  
  for e in G.edges():    
    heappush(H, (g.getEdge(e[0],e[1]), e[0], e[1]))
  
  P = Graph()
  for v in G.vertices():
    P.addVertex(v)
  
  while H and len(P.edges())//2 < len(P.vertices())-1:         
    (dist, v, u) = heappop(H)    
    #If you are about to add an edge between node A and node B, 
    #then first search if there is an existing path between A and B.
    # If such a path exists, then you must not add the edge AB.     
    if str(u) not in P.path(v):      
      P.addEdge(v, u, dist)
  return P    


def prims(G):
  mv = math.inf
  me = None
  for e in G.edges():
    if G.getEdge(e[0],e[1]) < mv:
      mv = G.getEdge(e[0],e[1])
      me = e

  P = Graph()
  for v in G.vertices():
    P.addVertex(v)

  visited = set()
  while me and len(P.edges())//2 < len(P.vertices())-1:    
    P.addEdge(me[0], me[1], G.getEdge(me[0],me[1]))
    visited.add(me[0])
    visited.add(me[1])
    mv = math.inf
    me = None    
    for v in visited:
      for u in G.adjacents(v):
        if (u not in visited) and G.getEdge(v,u)< mv:
          mv = G.getEdge(v,u)
          me = (v,u)
  return P
