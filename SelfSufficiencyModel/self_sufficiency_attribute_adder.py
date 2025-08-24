from HelperFiles.base_class_for_adding_attributes_to_house_objects import AddingAttributesToObject
from SelfSufficiencyModel.determine_self_sufficiency import SelfSufficiency
from HouseModel.house import House

class SelfSufficiencyAttributeAdder(AddingAttributesToObject):

    def get_object_id(self, data_object: SelfSufficiency) -> int:
        return data_object.house_id

    def get_attribute_from_source(self, source_object: SelfSufficiency) -> float:
        return source_object.self_sufficiency

    def define_object_dictionary(self, data_objects: list[SelfSufficiency]) -> dict[int, SelfSufficiency]:
        if isinstance(data_objects, list):
            return {obj.house_id: obj for obj in data_objects}
        return {}

    def add_self_sufficiency_to_houses(self, houses: list[House], self_sufficiency_objects: list[SelfSufficiency]) -> None:
        self.add_attribute(houses, self_sufficiency_objects, "self_sufficiency")
