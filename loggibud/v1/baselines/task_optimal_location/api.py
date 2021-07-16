from flask import Flask, request

from loggibud.v1.baselines.task_optimal_location.utils.resolve_arg import (
  resolve_location_id,
  resolve_candidates,
  resolve_calc_method,
  resolve_K,
  resolve_response,
  resolve_algorithm,
  resolve_solver_response
)
from loggibud.v1.baselines.task_optimal_location.utils.generator_factories import (
  instancesGeneratorFactory
)

app = Flask(__name__)

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

    response = solver(instances, candidates, old, k)
  except ValueError as e:
    return { "message": str(e) }, 422

  return resolve_solver_response(response)

app.run()