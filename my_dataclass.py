from dataclasses import dataclass, field, asdict
from typing import Optional, List

@dataclass
class Quantity:
    quantity_unit: str
    quantity_lower_value: Optional[str] = None
    quantity_upper_value: Optional[str] = None
    quantity_modifier: str = ""

@dataclass
class MeasuredProperty:
    property_name: str
    quantity: Quantity= None

@dataclass
class MeasuredEntity:
    entity_name: str
    measured_properties: List[MeasuredProperty] = field(default_factory=list)

@dataclass
class Patent:
    patent_name: str
    claim_text: str = ""
    drawing_description: str = ""
    description: str = ""
    abstract: str = ""
    measured_entities: List[MeasuredEntity] = field(default_factory=list)
    def add_entity(self, entity_name: str, measured_properties: List[MeasuredProperty]):
        entity = MeasuredEntity(entity_name=entity_name, measured_properties=measured_properties)
        self.measured_entities.append(entity)

#Create an instance of the Patent class with quantity values and their units
# quantity_1 = Quantity(quantity_lower_value=20, quantity_upper_value=40, quantity_unit="ml", quantity_modifier="almost")
# property_1 = MeasuredProperty(property_name="Crystallite Size", quantity=quantity_1)
# entity_1 = MeasuredEntity(entity_name="Compound A", measured_properties=[property_1])
#
# # Create another instance of the Patent class
# patent = Patent(patent_name="Example Patent", text="Some patent text")
# patent.add_entity(entity_name="Compound B", measured_properties=[])
#
# # Add the first compound to the measured_entities list in the patent object
# patent.measured_entities.append(entity_1)
#
# # Serialize the dataclass instance to JSON
# json_data = json.dumps(patent, default=lambda x: asdict(x), indent=4)
# print(json_data)
