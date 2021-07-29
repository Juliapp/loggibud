from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minsum import solve

def test_minsum_current(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
    mocked_K
  ):

  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  current = solution["currentSolution"]
  currentSolution = current["result"]
  
  assert currentSolution == 5123357.986335916

def test_minsum_result(
  mocked_instances,
  mocked_candidates,
  mocked_OLDistance,
  mocked_K
  ):
  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)

  [kSolution] = solution["kSolution"]
  solutionSum = kSolution["result"]
  candidate = kSolution["candidate"]
  attraction = kSolution["attraction"]

  assert attraction == 51
  assert solutionSum == 4206999.083689318
  assert candidate == Point(lng=-43.684247, lat=-22.9581481)

def test_minsum_k_more_than_1(
  mocked_instances,
  mocked_candidates,
  mocked_OLDistance,
):
  new_K = 2
  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, new_K)
  solution1 = solution["kSolution"][1]
  
  solutionSum = solution1["result"]
  candidate = solution1["candidate"]
  attraction = solution1["attraction"]
  
  assert len(solution["kSolution"]) == 2
  assert attraction == 51
  assert solutionSum == 4260323.381126462
  assert candidate == Point(lng=-43.6941723, lat=-22.9666855)