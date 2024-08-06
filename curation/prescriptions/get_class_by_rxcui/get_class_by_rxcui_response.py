from dataclasses import dataclass
from typing import Any, List, TypeVar, Type, cast, Callable

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class MinConcept:
    rxcui: int
    name: str
    tty: str

    @staticmethod
    def from_dict(obj: Any) -> 'MinConcept':
        assert isinstance(obj, dict)
        rxcui = int(from_str(obj.get("rxcui")))
        name = from_str(obj.get("name"))
        tty = from_str(obj.get("tty"))
        return MinConcept(rxcui, name, tty)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rxcui"] = from_str(str(self.rxcui))
        result["name"] = from_str(self.name)
        result["tty"] = from_str(self.tty)
        return result


@dataclass
class RxclassMinConceptItem:
    class_id: str
    class_name: str
    class_type: str

    @staticmethod
    def from_dict(obj: Any) -> 'RxclassMinConceptItem':
        assert isinstance(obj, dict)
        class_id = from_str(obj.get("classId"))
        class_name = from_str(obj.get("className"))
        class_type = from_str(obj.get("classType"))
        return RxclassMinConceptItem(class_id, class_name, class_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["classId"] = from_str(self.class_id)
        result["className"] = from_str(self.class_name)
        result["classType"] = from_str(self.class_type)
        return result


@dataclass
class RxclassDrugInfo:
    min_concept: MinConcept
    rxclass_min_concept_item: RxclassMinConceptItem
    rela: str
    rela_source: str

    @staticmethod
    def from_dict(obj: Any) -> 'RxclassDrugInfo':
        assert isinstance(obj, dict)
        min_concept = MinConcept.from_dict(obj.get("minConcept"))
        rxclass_min_concept_item = RxclassMinConceptItem.from_dict(obj.get("rxclassMinConceptItem"))
        rela = from_str(obj.get("rela"))
        rela_source = from_str(obj.get("relaSource"))
        return RxclassDrugInfo(min_concept, rxclass_min_concept_item, rela, rela_source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["minConcept"] = to_class(MinConcept, self.min_concept)
        result["rxclassMinConceptItem"] = to_class(RxclassMinConceptItem, self.rxclass_min_concept_item)
        result["rela"] = from_str(self.rela)
        result["relaSource"] = from_str(self.rela_source)
        return result


@dataclass
class RxclassDrugInfoList:
    rxclass_drug_info: List[RxclassDrugInfo]

    @staticmethod
    def from_dict(obj: Any) -> 'RxclassDrugInfoList':
        assert isinstance(obj, dict)
        rxclass_drug_info = from_list(RxclassDrugInfo.from_dict, obj.get("rxclassDrugInfo"))
        return RxclassDrugInfoList(rxclass_drug_info)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rxclassDrugInfo"] = from_list(lambda x: to_class(RxclassDrugInfo, x), self.rxclass_drug_info)
        return result


@dataclass
class GetClassByRxCUIResponse:
    rxclass_drug_info_list: RxclassDrugInfoList

    @staticmethod
    def from_dict(obj: Any) -> 'GetClassByRxCUIResponse':
        assert isinstance(obj, dict)
        rxclass_drug_info_list = RxclassDrugInfoList.from_dict(obj.get("rxclassDrugInfoList"))
        return GetClassByRxCUIResponse(rxclass_drug_info_list)

    def to_dict(self) -> dict:
        result: dict = {}
        result["rxclassDrugInfoList"] = to_class(RxclassDrugInfoList, self.rxclass_drug_info_list)
        return result


def get_class_by_rx_cui_response_from_dict(s: Any) -> GetClassByRxCUIResponse:
    return GetClassByRxCUIResponse.from_dict(s)


def get_class_by_rx_cui_response_to_dict(x: GetClassByRxCUIResponse) -> Any:
    return to_class(GetClassByRxCUIResponse, x)
