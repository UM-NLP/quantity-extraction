import re

string = """
Entity Definitions:
1. Entity: Any object or concept that can be identified and referred to in text.
2. Property: Any characteristic or attribute of an entity that can be measured or described.
3. Quantity: A quantity is a numeric value and, if applicable, a unit that describes the amount or extent of a property.

Output Format:
{
  "entities": [
    {
      "entity_name": "<entity_name>",
      "properties": [
        {
          "property_name": "<property_name>",
          "quantity": {
            "quantity_unit": "<quantity_unit>",
            "quantity_lower_value": "<quantity_lower_value>",
            "quantity_upper_value": "<quantity_upper_value>",
            "quantity_modifier": "<quantity_modifier>"
          }
        }
      ]
    }
  ]
}

Examples:
1. Sentence: The temperature of the water in the tank is 50 degrees Celsius.
   Output:
   {
     "entities": [
       {
         "entity_name": "water",
         "properties": [
           {
             "property_name": "temperature",
             "quantity": {
               "quantity_unit": "degrees Celsius",
               "quantity_lower_value": "50",
               "quantity_upper_value": "",
               "quantity_modifier": ""
             }
           }
         ]
       }
     ]
   }

2. Sentence: The car has four wheels and a steering wheel.
   Output: {}

3. Sentence: The experiment resulted in a catalytic activity for NOx of 120 operations.
   Output:
   {
     "entities": [
       {
         "entity_name": "NOx",
         "properties": [
           {
             "property_name": "catalytic activity",
             "quantity": {
               "quantity_unit": "operations",
               "quantity_lower_value": "120",
               "quantity_upper_value": "220",
               "quantity_modifier": "greater than or equal to"
             }
           }
         ]
       }
     ]
   }

Note: The new prompt focuses on the general concept of entity, property, and quantity, which can be applied to a wide range of relationship extraction tasks. It also provides clearer and more concise definitions and examples, making it easier for users to understand and use the system."""

start_marker = "Entity Definitions"
end_marker = r"}"

start_index = string.find(start_marker)
end_index = string.rfind(end_marker)

if start_index != -1 and end_index != -1:
    end_index += len(end_marker)
    selected_part = string[start_index:end_index]
    print(selected_part)
else:
    print("Start and/or end markers not found in the string.")
