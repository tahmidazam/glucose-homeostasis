from dataclasses import dataclass
from typing import List, Any, TypeVar, Callable, Type, cast

T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    if not isinstance(x, list):
        return []
    return [f(y) for y in x]


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class IDGroup:
    rxnorm_id: List[int]

    @staticmethod
    def from_dict(obj: Any) -> "IDGroup":
        assert isinstance(obj, dict)
        rxnorm_id = from_list(lambda x: int(from_str(x)), obj.get("rxnormId"))
        return IDGroup(rxnorm_id)

    def to_dict(self) -> dict:
        result: dict = {
            "rxnormId": from_list(lambda x: from_str((lambda x: str(x))(x)), self.rxnorm_id)
        }
        return result


@dataclass
class FindRxCUIByIDResponse:
    id_group: IDGroup

    @staticmethod
    def from_dict(obj: Any) -> "FindRxCUIByIDResponse":
        assert isinstance(obj, dict)
        id_group = IDGroup.from_dict(obj.get("idGroup"))
        return FindRxCUIByIDResponse(id_group)

    def to_dict(self) -> dict:
        result: dict = {
            "idGroup": to_class(IDGroup, self.id_group)
        }

        return result


def find_rxcui_by_id_response_from_dict(s: Any) -> FindRxCUIByIDResponse:
    return FindRxCUIByIDResponse.from_dict(s)


def find_rxcui_by_id_response_to_dict(x: FindRxCUIByIDResponse) -> Any:
    return to_class(FindRxCUIByIDResponse, x)
