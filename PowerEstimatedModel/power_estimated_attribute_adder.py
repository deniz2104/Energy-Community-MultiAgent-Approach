from HelperFiles.base_class_for_adding_attributes_to_house_objects import AddingAttributesToObject
from PowerEstimatedModel.power_estimated import PowerEstimator
from HouseModel.house import House

class PowerEstimatedAttributeAdder(AddingAttributesToObject):
    
    def get_object_id(self, data_object: PowerEstimator) -> int:
        return data_object.house_id
    
    def get_attribute_from_source(self, source_object: PowerEstimator) -> dict[str,float]:
        return source_object.power_estimated

    def define_object_dictionary(self, data_objects: list[PowerEstimator]) -> dict[int, PowerEstimator]:
        if isinstance(data_objects, list):
            return {obj.house_id: obj for obj in data_objects}
        return {}

    def add_power_estimated_to_houses(self, houses: list[House], power_estimated_objects: list[PowerEstimator]) -> None:
        self.add_attribute(houses, power_estimated_objects, "power_estimated")
