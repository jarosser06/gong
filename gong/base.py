from collections.abc import Callable
from dataclasses import asdict, dataclass, fields
from datetime import datetime
from typing import Dict, _GenericAlias


@dataclass
class GongHTTPObjectBase:
    def __post_init__(self):
        obj_fields = fields(self)

        # Populate all objects found in the dataclass
        for field in obj_fields:

            # If the instance is callable, it's a class
            if isinstance(field.type, Callable):
                current_value = getattr(self, field.name)

                # Value was not set ... skip
                if not current_value:
                    continue

                if isinstance(field.type, _GenericAlias):
                    if field.type.__dict__['_name'] == 'List':
                        field_type_args = field.type.__args__

                        field_type_arg = field_type_args[0]
                        if isinstance(field_type_arg, Callable):
                            new_list = []

                            for item in current_value:
                                new_list.append(field_type_arg(**item))

                            setattr(self, field.name, new_list)
                
                # Ignore if the attribute was already populated with
                # an instance of the object
                if not isinstance(current_value, Dict):
                    continue

                setattr(self, field.name, field.type(**current_value))

    def to_dict(self):
        dikt = asdict(self)

        keys_to_delete = []

        for key, value in dikt.items():
            if not value:
                keys_to_delete.append(key)

            elif isinstance(value, Callable):
                dikt[key] = value.to_dict()

            elif isinstance(value, datetime):
                dikt[key] = value.isoformat()
            else:
                dikt[key] = value

        for key in keys_to_delete:
            del dikt[key]

        return dikt


@dataclass
class GongRecords(GongHTTPObjectBase):
    current_page_size: int
    current_page_number: int
    total_records: int
    cursor: str = None