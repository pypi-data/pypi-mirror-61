from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Union, Optional

import pytz
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat,
    validator,
)


class CraftTypes(Enum):
    """String based enum because of Typer/Click parsing."""

    SCAFFOLDING = "SCAFFOLDING"
    INSULATION = "INSULATION"
    WATERBLASTING = "WATERBLASTING"
    SANDBLASTING = "SANDBLASTING"
    PAINTING = "PAINTING"
    HOISTWELLS = "HOISTWELLS"
    MOBILE_EQUIPMENT = "MOBILE_EQUIPMENT"
    HVAC = "HVAC"
    PERMITTING = "PERMITTING"
    HOUSEKEEPING = "HOUSEKEEPING"


craft_type_codes = {
    CraftTypes.SCAFFOLDING: 10,
    CraftTypes.INSULATION: 15,
    CraftTypes.WATERBLASTING: 20,
    CraftTypes.SANDBLASTING: 25,
    CraftTypes.PAINTING: 30,
    CraftTypes.HOISTWELLS: 40,
    CraftTypes.MOBILE_EQUIPMENT: 50,
    CraftTypes.HVAC: 60,
    CraftTypes.PERMITTING: 90,
    CraftTypes.HOUSEKEEPING: 99,
}

craft_type_path_strings = {
    CraftTypes.SCAFFOLDING: "scaffoldRecords",
    CraftTypes.INSULATION: "insulationRecords",
    CraftTypes.WATERBLASTING: "waterblastingRecords",
    CraftTypes.SANDBLASTING: "sandblastingRecords",
    CraftTypes.PAINTING: "paintingRecords",
    CraftTypes.HOISTWELLS: "hoistwellRecords",
    CraftTypes.MOBILE_EQUIPMENT: "mobileEquipmentRecords",
    CraftTypes.HVAC: "hvacRecords",
    CraftTypes.PERMITTING: "permittingRecords",
    CraftTypes.HOUSEKEEPING: "housekeepingRecords",
}


class TaskTypes(Enum):
    INSTALLATION = 10
    MODIFICATION = 11
    REMOVAL = 12
    INSPECTION = 13
    WATERBLASTING = 20
    SANDBLASTING = 30
    INSULATION = 40
    ABATEMENT = 50
    PAINTING = 60
    REPAIR = 70
    LOCKOUT = 90
    WALKTHROUGH = 91
    PERFORMING_WORK = 92
    HOUSEKEEPING = 99


class TaskStatus(Enum):
    AWAITING_ESTIMATE = 5
    AWAITING_APPROVAL = 8
    AWAITING_SCHEDULE = 10
    SCHEDULED = 20
    AWAITING = 30
    IN_PROGRESS = 40
    ON_HOLD = 50
    COMPLETE = 90


class EventTypes(Enum):
    NEW_USER_APPROVED = 10
    NEW_USER_APPLIED = 11
    CRAFT_RECORD_CREATED = 20
    NEW_TASK_ADDED = 30
    TASK_STATUS_UPDATED = 31
    TASK_REASSIGNED_COMPANY = 32
    TASK_DESCRIPTION_UPDATED = 33
    TASK_WORK_ORDER_UPDATED = 34
    TASK_DETAILS_UPDATED = 36
    UPDATED_TITLE = 40
    UPDATED_DESCRIPTION = 41
    ADDED_PHOTO = 42
    REMOVED_PHOTO = 43
    CHANGED_ASSET = 44
    UPDATED_CRAFT_DETAILS = 45
    CHANGED_LOCATION_ID = 46
    UPDATED_LOCATION_ON_MAP = 47


class DetailDataType(Enum):
    string = "string"
    boolean = "bool"
    number = "number"
    timestamp = "timestamp"


@dataclass
class CraftDetail:
    data_type: DetailDataType
    title: str
    default_value: Union[str, bool, int, float, datetime, None]
    required: bool
    editable: bool
    min_value: Union[int, float, None] = None
    max_value: Union[int, float, None] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None

    def to_firestore(self) -> dict:
        output = {
            "type": self.data_type.value,
            "title": self.title,
            "defaultValue": self.default_value,
            "required": self.required,
            "editable": self.editable,
        }
        if self.min_value is not None:
            output["minValue"] = self.min_value

        if self.max_value is not None:
            output["maxValue"] = self.max_value

        if self.min_length is not None:
            output["minLength"] = self.min_length

        if self.max_length is not None:
            output["maxLength"] = self.max_length

        return output


class CraftDetailValidator(BaseModel):
    data_type: DetailDataType
    title: StrictStr
    default_value: Union[StrictStr, StrictBool, StrictInt, StrictFloat, datetime, None]
    required: StrictBool
    editable: StrictBool
    min_value: Union[StrictInt, StrictFloat, None]
    max_value: Union[StrictInt, StrictFloat, None]
    min_length: Optional[StrictInt]
    max_length: Optional[StrictInt]

    @validator("default_value")
    def default_value_must_match_data_type(cls, v, values):
        if values["data_type"] == DetailDataType.boolean:
            if type(v) is not bool:
                raise ValueError("Expected default_value to be a boolean.")
        elif values["data_type"] == DetailDataType.number:
            if type(v) not in [float, int]:
                raise ValueError(
                    "Expected default_value to be a number (int or float)."
                )
        elif values["data_type"] == DetailDataType.string:
            if type(v) is not str:
                raise ValueError("Expected default_value to be a string.")
        elif values["data_type"] == DetailDataType.timestamp:
            if v is not None:
                raise ValueError("Expected default_value to be None.")
        else:
            raise ValueError("Unexpected condition for DetailDataType")

    @validator("min_value")
    def min_value_must_be_present_for_numbers(cls, v, values):
        if values["data_type"] == DetailDataType.number:
            if v is None:
                raise ValueError("Expected a value for min_value")

    @validator("max_value")
    def max_value_must_be_present_for_numbers(cls, v, values):
        if values["data_type"] == DetailDataType.number:
            if v is None:
                raise ValueError("Expected a value for max_value")

    @validator("min_length")
    def min_length_must_be_present_for_strings(cls, v, values):
        if values["data_type"] == DetailDataType.string:
            if v is None:
                raise ValueError("Expected a value for min_length")

    @validator("max_length")
    def max_length_must_be_present_for_strings(cls, v, values):
        if values["data_type"] == DetailDataType.string:
            if v is None:
                raise ValueError("Expected a value for max_length")


@dataclass
class SiteKey:
    name: str
    timezone: str
    managingCompanyID: str
    validCraftTypes: List[int]
    validTaskTypes: List[int]
    validTaskStatusCodes: List[int]
    validEventTypes: List[int]
    customizations: Dict[str, Any]


class SiteKeyValidator(BaseModel):
    name: StrictStr
    timezone: StrictStr
    managingCompanyID: StrictStr
    validCraftTypes: List[StrictInt]
    validTaskTypes: List[StrictInt]
    validTaskStatusCodes: List[StrictInt]
    validEventTypes: List[StrictInt]
    customizations: Dict[StrictStr, Any]

    @validator("timezone")
    def timezone_must_be_valid(cls, tz_string: str):
        if tz_string not in pytz.common_timezones:
            raise ValueError(f"Timezone '{tz_string}' is not valid")

    @validator("validCraftTypes")
    def craft_type_must_be_in_list(cls, type_list: List[int]):
        errors: List[str] = []
        for item in type_list:
            if item not in craft_type_codes.values():
                errors.append(f"code {item} not found in craft type codes")
        if len(errors) > 0:
            raise ValueError(f"Validation errors: {errors}")

        return type_list

    @validator("validTaskTypes")
    def task_type_must_be_in_list(cls, type_list: List[int]):
        errors: List[str] = []
        for item in type_list:
            if item not in [task_type.value for task_type in TaskTypes]:
                errors.append(f"code {item} not found in TaskTypes")
        if len(errors) > 0:
            raise ValueError(f"Validation errors: {errors}")

        return type_list

    @validator("validTaskStatusCodes")
    def status_type_must_be_in_list(cls, type_list: List[int]):
        errors: List[str] = []
        for item in type_list:
            if item not in [status_type.value for status_type in TaskStatus]:
                errors.append(f"code {item} not found in TaskStatus")
        if len(errors) > 0:
            raise ValueError(f"Validation errors: {errors}")

        return type_list

    @validator("validEventTypes")
    def event_type_must_be_in_list(cls, type_list: List[int]):
        errors: List[str] = []
        for item in type_list:
            if item not in [event_type.value for event_type in EventTypes]:
                errors.append(f"code {item} not found in EventTypes")
        if len(errors) > 0:
            raise ValueError(f"Validation errors: {errors}")

        return type_list
