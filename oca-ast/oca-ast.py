from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class OCAAst(BaseModel):
    version: str
    commands: List["Command"]
    commands_meta: Dict[int, "CommandMeta"]
    meta: Dict[str, str]


class Command(BaseModel):
    kind: "CommandType" = Field(alias="type")
    object_kind: "ObjectKind"


class CommandType(str, Enum):
    Remove = "Remove"
    Modify = "Modify"
    From = "From"


class CommandMeta(BaseModel):
    line_number: int
    raw_line: str


class ObjectKind(Enum):
    CaptureBase: "CaptureContent" = "CaptureBase"
    OCABunde: "BundleContent" = "BundleContent"
    Overlay: "Overlay" = "Overlay"

    def __hash__(self):
        if self == ObjectKind.CaptureBase:
            return hash((self.value, CaptureContent))
        elif self == ObjectKind.OCABunde:
            return hash((self.value, BundleContent))
        elif self == ObjectKind.Overlay:
            return hash((self.value, Overlay))


class CaptureContent(BaseModel):
    attributes: Optional[Dict[str, "NestedAttrType"]] = Field(default_factory=dict)
    properties: Optional[Dict[str, "NestedValue"]] = Field(default_factory=dict)
    flagged_attributes: Optional[List[str]] = Field(default_factory=list)

    def __hash__(self):
        hash_value = []

        for key, value in self.attributes.items():
            hash_value.append(hash(key))
            hash_value.append(hash(value))

        for key, value in self.properties.items():
            hash_value.append(hash(key))
            hash_value.append(hash(value))

        return hash(tuple(hash_value))


class Content(BaseModel):
    attributes: Optional[Dict[str, "NestedAttrType"]] = Field(default_factory=dict)
    properties: Optional[Dict[str, "NestedValue"]] = Field(default_factory=dict)


class Overlay(BaseModel):
    overlay_type: "OverlayType"
    content: "Content"


class OverlayType(Enum):
    Label = "Label"
    Information = "Information"
    Encoding = "Encoding"
    CharacterEncoding = "CharacterEncoding"
    Format = "Format"
    Meta = "Meta"
    Standard = "Standard"
    Cardinality = "Cardinality"
    Conditional = "Conditional"
    Conformance = "Conformance"
    EntryCode = "EntryCode"
    Entry = "Entry"
    Unit = "Unit"
    AttributeMapping = "AttributeMapping"
    EntryCodeMapping = "EntryCodeMapping"
    Subset = "Subset"
    UnitMapping = "UnitMapping"
    Layout = "Layout"
    Sensitivity = "Sensitivity"

    def to_serialized_str(self):
        mapping = {
            OverlayType.Label: "spec/overlays/label/1.0",
            OverlayType.Information: "spec/overlays/information/1.0",
            OverlayType.Encoding: "spec/overlays/encoding/1.0",
            OverlayType.CharacterEncoding: "spec/overlays/character_encoding/1.0",
            OverlayType.Format: "spec/overlays/format/1.0",
            OverlayType.Meta: "spec/overlays/meta/1.0",
            OverlayType.Standard: "spec/overlays/standard/1.0",
            OverlayType.Cardinality: "spec/overlays/cardinality/1.0",
            OverlayType.Conditional: "spec/overlays/conditional/1.0",
            OverlayType.Conformance: "spec/overlays/conformance/1.0",
            OverlayType.EntryCode: "spec/overlays/entry_code/1.0",
            OverlayType.Entry: "spec/overlays/entry/1.0",
            OverlayType.Unit: "spec/overlays/unit/1.0",
            OverlayType.AttributeMapping: "spec/overlays/mapping/1.0",
            OverlayType.EntryCodeMapping: "spec/overlays/entry_code_mapping/1.0",
            OverlayType.Subset: "spec/overlays/subset/1.0",
            OverlayType.UnitMapping: "spec/overlays/unit_mapping/1.0",
            OverlayType.Layout: "spec/overlays/layout/1.0",
            OverlayType.Sensitivity: "spec/overlays/sensitivity/1.0",
        }
        return mapping[self]


class NestedAttrType(BaseModel):
    pass


class NestedValue(BaseModel):
    pass


class BundleContent(BaseModel):
    pass


class AttributeType(str, Enum):
    Boolean = "Boolean"
    Binary = "Binary"
    Text = "Text"
    Numeric = "Numeric"
    Datetime = "Datetime"

    @classmethod
    def from_str(cls, s: str):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"{s} is not a valid AttributeType")


# testing
oca_ast = OCAAst(
    version="1.0.0",
    commands=[
        {"type": CommandType.Remove, "object_kind": ObjectKind.CaptureBase},
        {"type": CommandType.Modify, "object_kind": ObjectKind.OCABunde},
        {"type": CommandType.From, "object_kind": ObjectKind.Overlay},
    ],
    commands_meta={
        1: CommandMeta(line_number=1, raw_line="Remove CaptureBase"),
        2: CommandMeta(line_number=2, raw_line="Modify OCABunde"),
        3: CommandMeta(line_number=3, raw_line="From Overlay"),
    },
    meta={"key": "value"},
)

print(oca_ast)
