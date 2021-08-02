from flask import Flask, request
from flask_cors import CORS
import json

from loggibud.v1.baselines.task_optimal_location.utils.areas import getLoggiAreas

from loggibud.v1.baselines.task_optimal_location.utils.resolve_arg import (
  resolve_location_id,
  resolve_candidates,
  resolve_calc_method,
  resolve_K,
  resolve_algorithm,
)
from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  instancesGeneratorFactory
)

app = Flask(__name__)
CORS(app)

@app.route('/run', methods=['POST'])
def run():
  body = request.get_json()["params"]
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

@app.route('/get-areas', methods=['GET']) 
def getAreas():
  return json.dumps(getLoggiAreas())


app.run()