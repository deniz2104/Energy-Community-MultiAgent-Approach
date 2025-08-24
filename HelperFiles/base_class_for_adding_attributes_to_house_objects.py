from abc import ABC, abstractmethod
from typing import Any,Union


class AddingAttributesToObject(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_object_id(self,data_object: Any) -> int:
        pass

    @abstractmethod
    def define_object_dictionary(self,data_objects: Any)->dict[int,Any]:
        pass

    def add_attribute(self, target_objects: Any, source_objects: Any, attribute_name: str) -> None:
        object_dict = self.define_object_dictionary(source_objects)
        for target_object in target_objects:
            object_id = self.get_object_id(target_object)
            if object_dict is not None and object_id in object_dict:
                attribute_value = self.get_attribute_from_source(object_dict[object_id])
                setattr(target_object, attribute_name, attribute_value)
    
    @abstractmethod
    def get_attribute_from_source(self, source_object: Any) -> Union[dict[str, float], float]:
        pass
