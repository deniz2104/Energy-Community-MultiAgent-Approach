from HelperFiles.base_class_for_adding_attributes_to_house_objects import AddingAttributesToObject
from SelfConsumptionModel.determine_self_consumption import SelfConsumption
from HouseModel.house import House

class SelfConsumptionAttributeAdder(AddingAttributesToObject):

    def get_object_id(self, data_object: SelfConsumption) -> int:
        return data_object.house_id

    def get_attribute_from_source(self, source_object: SelfConsumption) -> float:
        return source_object.self_consumption

    def define_object_dictionary(self, data_objects: list[SelfConsumption]) -> dict[int, SelfConsumption]:
        if isinstance(data_objects, list):
            return {obj.house_id: obj for obj in data_objects}
        return {}

    def add_self_consumption_to_houses(self, houses: list[House], self_consumption_objects: list[SelfConsumption]) -> None:
        self.add_attribute(houses, self_consumption_objects, "self_consumption")
