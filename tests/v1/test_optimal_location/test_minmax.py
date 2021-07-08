from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minmax import solve
from loggibud.v1.baselines.task_optimal_location.geojson_script import run


def test_minmax_solver(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
    mocked_K
  ):

  (current, [solution]) = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  (currentMax, currentOrigin, currentClient) = current
  
  assert currentMax == 36831.2314012329
  assert currentOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert currentClient == Point(lng=-43.69207312451086, lat=-22.966707777965688)

  (solutionMax, solutionOrigin, solutionClient, candidate) = solution
  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.684247, lat=-22.9581481)

  run(mocked_instances)


def test_minmax_solver_k(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
  ):

  (current, [solution0, solution1]) = solve(mocked_instances, mocked_candidates, mocked_OLDistance, 2)

  (solutionMax, solutionOrigin, solutionClient, candidate) = solution1
  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.6941723, lat=-22.9666855)


  