from flask import Flask, request, make_response
import json

from loggibud.v1.baselines.task_optimal_location.utils.areas import getLoggiAreas

from loggibud.v1.baselines.task_optimal_location.utils.resolve_arg import (
  resolve_location_id,
  resolve_candidates,
  resolve_calc_method,
  resolve_K,
  resolve_algorithm,
  resolve_solver_response
)
from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  instancesGeneratorFactory
)

app = Flask(__name__)

def _build_cors_prelight_response(res):
  response = make_response(res)
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add('Access-Control-Allow-Headers', "*")
  response.headers.add('Access-Control-Allow-Methods', "*")
  return response

@app.route('/run', methods=['GET'])
def run():
  body = request.get_json()
  try:
    paths = resolve_location_id('test')
    # paths = resolve_location_id(body['location_id'])

    instances = instancesGeneratorFactory(paths)

    (candidates, len_candidates) = resolve_candidates(body["candidates"])

    old = resolve_calc_method("distance_matrix_great_circle")

    k = resolve_K(body["k"], len_candidates)

    solver = resolve_algorithm(body["algorithm"])

    res = solver(instances, candidates, old, k)

    return _build_cors_prelight_response(res)

  except ValueError as e:
    return { "message": str(e) }, 422


@app.route('/get-algorithms', methods=['GET']) 
def getAlgorithms():
  return _build_cors_prelight_response(json.dumps(['minmax', 'minsum']))

@app.route('/get-areas', methods=['GET']) 
def getAreas():
  return _build_cors_prelight_response(json.dumps(getLoggiAreas()))


app.run()