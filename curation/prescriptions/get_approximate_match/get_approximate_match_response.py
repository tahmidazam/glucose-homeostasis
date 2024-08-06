from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if not isinstance(x, list):
        return []
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Candidate:
    rxcui: int
    rxaui: int
    score: float
    rank: int
    source: str
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Candidate':
        assert isinstance(obj, dict)
        rxcui = int(from_str(obj.get("rxcui")))
        rxaui = int(from_str(obj.get("rxaui")))
        score = float(from_str(obj.get("score")))
        rank = int(from_str(obj.get("rank")))
        source = from_str(obj.get("source"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Candidate(rxcui, rxaui, score, rank, source, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rxcui"] = from_str(str(self.rxcui))
        result["rxaui"] = from_str(str(self.rxaui))
        result["score"] = from_str(self.score)
        result["rank"] = from_str(str(self.rank))
        result["source"] = from_str(self.source)
        if self.name is not None:
            result["name"] = from_union([from_str, from_none], self.name)
        return result


@dataclass
class ApproximateGroup:
    input_term: None
    candidate: List[Candidate]

    @staticmethod
    def from_dict(obj: Any) -> 'ApproximateGroup':
        assert isinstance(obj, dict)
        input_term = from_none(obj.get("inputTerm"))
        candidate = from_list(Candidate.from_dict, obj.get("candidate"))
        return ApproximateGroup(input_term, candidate)

    def to_dict(self) -> dict:
        result: dict = {}
        result["inputTerm"] = from_none(self.input_term)
        result["candidate"] = from_list(lambda x: to_class(Candidate, x), self.candidate)
        return result


@dataclass
class GetApproximateMatchResponse:
    approximate_group: ApproximateGroup

    @staticmethod
    def from_dict(obj: Any) -> 'GetApproximateMatchResponse':
        assert isinstance(obj, dict)
        approximate_group = ApproximateGroup.from_dict(obj.get("approximateGroup"))
        return GetApproximateMatchResponse(approximate_group)

    def to_dict(self) -> dict:
        result: dict = {}
        result["approximateGroup"] = to_class(ApproximateGroup, self.approximate_group)
        return result


def get_approximate_match_response_from_dict(s: Any) -> GetApproximateMatchResponse:
    return GetApproximateMatchResponse.from_dict(s)


def get_approximate_match_response_to_dict(x: GetApproximateMatchResponse) -> Any:
    return to_class(GetApproximateMatchResponse, x)
