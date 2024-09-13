from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List

from pydantic import BaseModel, Field

class OCAAst(BaseModel):
    version: str
    commands: List["Command"]
    commands_meta: Dict[int, "CommandMeta"]
    meta: Dict[str, str]


class Command(BaseModel):
    kind: "CommandType" = Field(alias="type")
    object_kind: 'ObjectKind'


class CommandType(Enum):
    Add = "Add"
    Remove = "Remove"
    Modify = "Modify"
    From = "From"


class CommandMeta(BaseModel):
    line_number: int
    raw_line: str

class ObjectKind(Enum):
    CaptureBase: 'CaptureContent' = "CaptureBase"
    OCABunde: 'OCABundle' = "OCABundle"
    Overlay: 'Overlay' = "Overlay"



class CaptureContent(BaseModel):
    attributes: Optional[Dict[str, 'NestedAttrType']] = Field(default_factory=dict)
    properties: Optional[Dict[str, 'NestedValue']] = Field(default_factory=dict)
    flagged_attributes: Optional[List[str]] = Field(default_factory=list)


class NestedAttrType(BaseModel):
    pass

class NestedValue(BaseModel):
    pass

class OCABundle(BaseModel):
    pass

class Overlay(Enum):
    pass
