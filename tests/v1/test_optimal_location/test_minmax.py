from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minmax import solve


def test_minmax_solver(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
    mocked_K
  ):

  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  current = solution["currentSolution"]
  currentMax = current["result"]
  currentOrigin = current["origin"]
  currentClient = current["delivery"]
  
  assert currentMax == 36831.2314012329
  assert currentOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert currentClient == Point(lng=-43.69207312451086, lat=-22.966707777965688)

  [kSolution] = solution["kSolution"]

  solutionMax = kSolution["result"]
  solutionOrigin = kSolution["origin"]
  solutionClient = kSolution["delivery"]
  candidate = kSolution["candidate"]

  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.684247, lat=-22.9581481)


def test_minmax_solver_k(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
  ):

  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, 2)
  current = solution["currentSolution"]
  currentMax = current["result"]
  currentOrigin = current["origin"]
  currentClient = current["delivery"]
  
  [kSolution0, kSolution1] = solution["kSolution"]

  solutionMax = kSolution1["result"]
  solutionOrigin = kSolution1["origin"]
  solutionClient = kSolution1["delivery"]
  candidate = kSolution1["candidate"]
  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.6941723, lat=-22.9666855)


  