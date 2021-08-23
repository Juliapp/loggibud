from flask import Flask, request, Response
from flask_cors import CORS
import json

from loggibud.v1.baselines.task_optimal_location.utils.regions import (
  getLoggiRegions, 
)

from loggibud.v1.baselines.task_optimal_location.utils.dictCompressor import (
  compress
)

from loggibud.v1.baselines.task_optimal_location.utils.resolve_arg import (
  resolve_location_id,
  resolve_candidates,
  resolve_calc_method,
  resolve_K,
  resolve_algorithm,
  resolve_point_type,
  resolve_region_data_percentage
)

from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  instancesGeneratorFactory
)

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run():
  body = request.get_json()["data"]
  try:
    paths = resolve_location_id(body['location_id'])

    instances = instancesGeneratorFactory(paths)

    (candidates, len_candidates) = resolve_candidates(body["candidates"])

    old = resolve_calc_method("distance_matrix_great_circle")

    k = resolve_K(body["k"], len_candidates)

    solver = resolve_algorithm(body["algorithm"])

    res = solver(instances, candidates, old, k)

    response = res

  except ValueError as e:
    response = ({ "message": str(e) }, 422)

  return response

@app.route('/get-algorithms', methods=['GET']) 
def getAlgorithms():
  return json.dumps(['minmax', 'minsum'])

@app.route('/get-regions', methods=['GET']) 
def getRegions():
  return json.dumps(getLoggiRegions())

@app.route('/get-region-data', methods=['GET'])
def getRegionData():
  args = request.args.get
  try:
    paths = resolve_location_id(args('location_id'))

    percentage = resolve_region_data_percentage(float(args('percentage')))

    region_generator = resolve_point_type(args('point_type'))

    data = region_generator(paths, percentage)

    compressed = compress(data)
    
    response = Response(compressed)

    response.headers['content-encoding'] = 'gzip'
    response.headers['Content-Type'] = 'application/json'
    
  except ValueError as e:
    response = ({ "message": str(e) }, 422)

  return response


app.run()