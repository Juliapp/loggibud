from loggibud.v1.types import Point
from loggibud.v1.baselines.task_optimal_location.minmax import solve


def test_minmax_current(
    mocked_instances,
    mocked_candidates,
    mocked_OLDistance,
    mocked_K
  ):
  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  current = solution["currentSolution"]
  currentMax = current["result"]
  currentOrigin = current["detail"]["origin"]
  currentClient = current["detail"]["delivery"]

  assert currentMax == 36831.2314012329
  assert currentOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert currentClient == Point(lng=-43.69207312451086, lat=-22.966707777965688)

def test_minmax_result(
  mocked_instances,
  mocked_candidates,
  mocked_OLDistance,
  mocked_K
  ):
  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, mocked_K)
  kSolution = solution["kSolution"][0]

  solutionMax = kSolution["result"]
  solutionOrigin = kSolution["detail"]["origin"]
  solutionClient = kSolution["detail"]["delivery"]
  candidate = kSolution["candidate"]
  attraction = kSolution["attraction"]

  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.684247, lat=-22.9581481)
  assert attraction == 51

def test_minmax_k_more_than_1(
  mocked_instances,
  mocked_candidates,
  mocked_OLDistance,
):
  new_K = 2
  solution = solve(mocked_instances, mocked_candidates, mocked_OLDistance, new_K)
  Ksolutions = solution["kSolution"]
  kSolution1 = solution["kSolution"][1]

  solutionMax = kSolution1["result"]
  solutionOrigin = kSolution1["detail"]["origin"]
  solutionClient = kSolution1["detail"]["delivery"]
  candidate = kSolution1["candidate"]
  attraction = kSolution1["attraction"]

  assert attraction == 51
  assert len(Ksolutions) == new_K
  assert solutionMax == 27240.58022888479
  assert solutionOrigin == Point(lng=-43.37769374114032, lat=-22.805996173217757)
  assert solutionClient == Point(lng=-43.314351564049836, lat=-22.568088515564767)
  assert candidate == Point(lng=-43.6941723, lat=-22.9666855)