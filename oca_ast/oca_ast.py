from enum import Enum
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, ValidationError, model_validator


class OCAAst(BaseModel):
    version: str = "1.0.0"
    commands: List["Command"] = []
    commands_meta: Dict[int, "CommandMeta"] = {}
    meta: Dict[str, str] = {}


class Command(BaseModel):
    kind: "CommandType" = Field(alias="type")
    object_kind: "ObjectKind"

    @model_validator(mode="before")
    def validate_object_kind(cls, values):
        object_kind_data = values.get("object_kind")
        if not object_kind_data:
            raise ValueError("Missing field: object_kind")
        object_kind_type = object_kind_data.get("type")
        if not object_kind_type:
            raise ValueError("Missing field: object_kind.type")

        if object_kind_type == ObjectKindType.CaptureBase:
            content = object_kind_data.get("content")
            if not content:
                raise ValueError("Missing field: conent for CaptureBase")
            values["object_kind"] = ObjectKind.capture_base(CaptureContent(**content))
        elif object_kind_type == ObjectKindType.OCABunde:
            content = object_kind_data.get("content")
            if not content:
                raise ValueError("Missing field: conent for OCABunde")
            values["object_kind"] = ObjectKind.oca_bundle(BundleContent(**content))
        elif object_kind_type == ObjectKindType.Overlay:
            content = object_kind_data.get("content")
            if not content:
                raise ValueError("Missing field: conent for Overlay")
            values["object_kind"] = ObjectKind.overlay(Overlay(**content))
        else:
            raise ValueError(f"Unknown object_kind type: {object_kind_type}")

        return values


class CommandTypeValue(str, Enum):
    Add = "Add"
    Remove = "Remove"
    Modify = "Modify"
    From = "From"


class CommandType(BaseModel):
    type: CommandTypeValue

    @classmethod
    def add(cls):
        return cls(type=CommandTypeValue.Add)

    @classmethod
    def remove(cls):
        return cls(type=CommandTypeValue.Remove)

    @classmethod
    def modify(cls):
        return cls(type=CommandTypeValue.Modify)

    @classmethod
    def from_(cls):
        return cls(type=CommandTypeValue.From)


class CommandMeta(BaseModel):
    line_number: int
    raw_line: str


class ObjectKindType(str, Enum):
    CaptureBase = "CaptureBase"
    OCABunde = "BundleContent"
    Overlay = "Overlay"


class ObjectKind(BaseModel):
    type: ObjectKindType
    value: Union["CaptureContent", "BundleContent", "Overlay"]

    @classmethod
    def capture_base(cls, content: "CaptureContent"):
        return cls(type=ObjectKindType.CaptureBase, value=content)

    @classmethod
    def oca_bundle(cls, content: "BundleContent"):
        return cls(type=ObjectKindType.OCABunde, value=content)

    @classmethod
    def overlay(cls, content: "Overlay"):
        return cls(type=ObjectKindType.Overlay, value=content)

    def __hash__(self):
        if self == ObjectKind.CaptureBase:
            return hash((self.value, CaptureContent))
        elif self == ObjectKind.OCABunde:
            return hash((self.value, BundleContent))
        elif self == ObjectKind.Overlay:
            return hash((self.value, Overlay))

    def capture_content(self, content: "CaptureContent"):
        if self == ObjectKind.CaptureBase:
            return content
        return None

    def overlay_content(self, content: "Overlay"):
        if self == ObjectKind.Overlay:
            return content
        return None

    def oca_bundle_content(self, content: "BundleContent"):
        if self == ObjectKind.OCABunde:
            return content
        return None

    def serialize(self, content):
        if self == ObjectKind.CaptureBase:
            return {
                "object_kind": "CaptureBase",
                "content": content,
            }
        elif self == ObjectKind.OCABunde:
            return {
                "object_kind": "OCABunde",
                "content": content,
            }

        elif self == ObjectKind.Overlay:
            return {
                "object_kind": "Overlay",
                "content": content,
            }

    @classmethod
    def from_int(cls, val: int) -> "ObjectKind":
        mapping = {
            0: cls.capture_base(CaptureContent()),
            1: cls.oca_bundle(BundleContent(said="")),
            2: cls.overlay(OverlayType.Label, Content()),
            3: cls.overlay(OverlayType.Information, Content()),
            4: cls.overlay(OverlayType.Encoding, Content()),
            5: cls.overlay(OverlayType.CharacterEncoding, Content()),
            6: cls.overlay(OverlayType.Format, Content()),
            7: cls.overlay(OverlayType.Meta, Content()),
            8: cls.overlay(OverlayType.Standard, Content()),
            9: cls.overlay(OverlayType.Cardinality, Content()),
            10: cls.overlay(OverlayType.Conditional, Content()),
            11: cls.overlay(OverlayType.Conformance, Content()),
            12: cls.overlay(OverlayType.EntryCode, Content()),
            13: cls.overlay(OverlayType.Entry, Content()),
            14: cls.overlay(OverlayType.Unit, Content()),
            15: cls.overlay(OverlayType.AttributeMapping, Content()),
            16: cls.overlay(OverlayType.EntryCodeMapping, Content()),
            17: cls.overlay(OverlayType.Subset, Content()),
            18: cls.overlay(OverlayType.UnitMapping, Content()),
            19: cls.overlay(OverlayType.Layout, Content()),
            20: cls.overlay(OverlayType.Sensitivity, Content()),
        }
        if val in mapping:
            return mapping[val]
        else:
            raise ValueError("Unknown object type")

    def to_int(self) -> int:
        reverse_mapping = {
            (ObjectKindType.CaptureBase, None): 0,
            (ObjectKindType.OCABundle, None): 1,
            (ObjectKindType.Overlay, OverlayType.Label): 2,
            (ObjectKindType.Overlay, OverlayType.Information): 3,
            (ObjectKindType.Overlay, OverlayType.Encoding): 4,
            (ObjectKindType.Overlay, OverlayType.CharacterEncoding): 5,
            (ObjectKindType.Overlay, OverlayType.Format): 6,
            (ObjectKindType.Overlay, OverlayType.Meta): 7,
            (ObjectKindType.Overlay, OverlayType.Standard): 8,
            (ObjectKindType.Overlay, OverlayType.Cardinality): 9,
            (ObjectKindType.Overlay, OverlayType.Conditional): 10,
            (ObjectKindType.Overlay, OverlayType.Conformance): 11,
            (ObjectKindType.Overlay, OverlayType.EntryCode): 12,
            (ObjectKindType.Overlay, OverlayType.Entry): 13,
            (ObjectKindType.Overlay, OverlayType.Unit): 14,
            (ObjectKindType.Overlay, OverlayType.AttributeMapping): 15,
            (ObjectKindType.Overlay, OverlayType.EntryCodeMapping): 16,
            (ObjectKindType.Overlay, OverlayType.Subset): 17,
            (ObjectKindType.Overlay, OverlayType.UnitMapping): 18,
            (ObjectKindType.Overlay, OverlayType.Layout): 19,
            (ObjectKindType.Overlay, OverlayType.Sensitivity): 20,
        }
        overlay_type = (
            self.value.get("overlay_type")
            if self.type == ObjectKindType.Overlay
            else None
        )
        key = (self.type, overlay_type)
        if key in reverse_mapping:
            return reverse_mapping[key]
        else:
            raise ValueError("Unknown object type")

    @model_validator(mode="before")
    def deserialize(cls, values):
        object_kind = values.get("type")
        overlay_type = values.get("overlay_type")
        content = Content()

        object_kind_mapping = {
            ObjectKindType.CaptureBase: lambda: cls.capture_base(CaptureContent()),
            ObjectKindType.OCABundle: lambda: cls.oca_bundle(BundleContent(said="")),
            ObjectKindType.Overlay: lambda: overlay_mapping.get(
                overlay_type, lambda: None
            )(),
        }

        overlay_mapping = {
            OverlayType.Label: lambda: cls.overlay(OverlayType.Label, content),
            OverlayType.Information: lambda: cls.overlay(
                OverlayType.Information, content
            ),
            OverlayType.Encoding: lambda: cls.overlay(OverlayType.Encoding, content),
            OverlayType.CharacterEncoding: lambda: cls.overlay(
                OverlayType.CharacterEncoding, content
            ),
            OverlayType.Format: lambda: cls.overlay(OverlayType.Format, content),
            OverlayType.Meta: lambda: cls.overlay(OverlayType.Meta, content),
            OverlayType.Standard: lambda: cls.overlay(OverlayType.Standard, content),
            OverlayType.Cardinality: lambda: cls.overlay(
                OverlayType.Cardinality, content
            ),
            OverlayType.Conditional: lambda: cls.overlay(
                OverlayType.Conditional, content
            ),
            OverlayType.Conformance: lambda: cls.overlay(
                OverlayType.Conformance, content
            ),
            OverlayType.EntryCode: lambda: cls.overlay(OverlayType.EntryCode, content),
            OverlayType.Entry: lambda: cls.overlay(OverlayType.Entry, content),
            OverlayType.Unit: lambda: cls.overlay(OverlayType.Unit, content),
            OverlayType.AttributeMapping: lambda: cls.overlay(
                OverlayType.AttributeMapping, content
            ),
            OverlayType.EntryCodeMapping: lambda: cls.overlay(
                OverlayType.EntryCodeMapping, content
            ),
            OverlayType.Subset: lambda: cls.overlay(OverlayType.Subset, content),
            OverlayType.UnitMapping: lambda: cls.overlay(
                OverlayType.UnitMapping, content
            ),
            OverlayType.Layout: lambda: cls.overlay(OverlayType.Layout, content),
            OverlayType.Sensitivity: lambda: cls.overlay(
                OverlayType.Sensitivity, content
            ),
        }

        if object_kind in object_kind_mapping:
            return object_kind_mapping[object_kind]()
        else:
            raise ValueError(f"Unknown object kind: {object_kind}")


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

    def serialize(self):
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

    @classmethod
    def deserialize(cls, s: str):
        mapping = {
            "spec/overlays/label/1.0": cls.Label,
            "spec/overlays/information/1.0": cls.Information,
            "spec/overlays/encoding/1.0": cls.Encoding,
            "spec/overlays/character_encoding/1.0": cls.CharacterEncoding,
            "spec/overlays/format/1.0": cls.Format,
            "spec/overlays/meta/1.0": cls.Meta,
            "spec/overlays/standard/1.0": cls.Standard,
            "spec/overlays/cardinality/1.0": cls.Cardinality,
            "spec/overlays/conditional/1.0": cls.Conditional,
            "spec/overlays/conformance/1.0": cls.Conformance,
            "spec/overlays/entry_code/1.0": cls.EntryCode,
            "spec/overlays/entry/1.0": cls.Entry,
            "spec/overlays/unit/1.0": cls.Unit,
            "spec/overlays/mapping/1.0": cls.AttributeMapping,
            "spec/overlays/entry_code_mapping/1.0": cls.EntryCodeMapping,
            "spec/overlays/subset/1.0": cls.Subset,
            "spec/overlays/unit_mapping/1.0": cls.UnitMapping,
            "spec/overlays/layout/1.0": cls.Layout,
            "spec/overlays/sensitivity/1.0": cls.Sensitivity,
        }
        if s in mapping:
            return mapping[s]
        else:
            raise ValueError(f"{s} is not a valid OverlayType")

    @classmethod
    def from_str(cls, s: str):
        mapping = {
            "Label": cls.Label,
            "Information": cls.Information,
            "Encoding": cls.Encoding,
            "CharacterEncoding": cls.CharacterEncoding,
            "Format": cls.Format,
            "Meta": cls.Meta,
            "Standard": cls.Standard,
            "Cardinality": cls.Cardinality,
            "Conditional": cls.Conditional,
            "Conformance": cls.Conformance,
            "EntryCode": cls.EntryCode,
            "Entry": cls.Entry,
            "Unit": cls.Unit,
            "Mapping": cls.AttributeMapping,
            "EntryCodeMapping": cls.EntryCodeMapping,
            "Subset": cls.Subset,
            "UnitMapping": cls.UnitMapping,
            "Layout": cls.Layout,
            "Sensitivity": cls.Sensitivity,
        }
        if s in mapping:
            return mapping[s]
        else:
            raise ValueError(f"{s} is not a valid OverlayType")

    def __self__(self):
        return self


class RefValueType(str, Enum):
    Said = "Said"
    Name = "Name"


class RefValue(BaseModel):
    type: RefValueType
    value: str

    @classmethod
    def said(cls, identifier: str):
        return cls(type=RefValueType.Said, value=identifier)

    @classmethod
    def name(cls, identifier: str):
        return cls(type=RefValueType.Name, value=identifier)

    def __str__(self):
        if self.type == RefValueType.Said:
            return f"refs:{self.value}"
        elif self.type == RefValueType.Name:
            return f"refn:{self.value}"
        return super().__str__()

    def serialize(self):
        if self.type == RefValueType.Said:
            return f"refs:{self.value}"
        elif self.type == RefValueType.Name:
            return f"refn:{self.value}"

    @classmethod
    def deserialize(cls, s: str):
        try:
            tag, rest = s.split(":", 1)
        except ValueError:
            raise ValueError(f"invalid reference: {s}")

        if tag == "refs":
            return cls.said(rest)
        elif tag == "refn":
            return cls.name(rest)
        else:
            raise ValueError(f"unknown reference type: {tag}")


class ReferenceAttrType(BaseModel):
    type: str
    value: RefValue

    @classmethod
    def reference(cls, ref_value: RefValue):
        return cls(type="Reference", value=ref_value)


class NestedValueType(str, Enum):
    Reference = "Reference"
    Value = "Value"
    Object = "Object"
    Array = "Array"


class NestedValue(BaseModel):
    type: NestedValueType
    value: Union[RefValue, str, Dict[str, "NestedValue"], List["NestedValue"]]

    @classmethod
    def reference_value(cls, ref_value: RefValue):
        return cls(type=NestedValueType.Reference, value=ref_value)

    @classmethod
    def str_value(cls, value: str):
        return cls(type=NestedValueType.Value, value=value)

    @classmethod
    def object_value(cls, value: Dict[str, "NestedValue"]):
        return cls(type=NestedValueType.Object, value=value)

    @classmethod
    def list_value(cls, value: List["NestedValue"]):
        return cls(type=NestedValueType.Array, value=value)

    def __hash__(self):
        if self.type == NestedValueType.Reference:
            return hash((self.type, self.value))
        elif self.type == NestedValueType.Value:
            return hash((self.type, self.value))
        elif self.type == NestedValueType.Object:
            return hash((self.type, tuple(self.value.items())))
        elif self.type == NestedValueType.Array:
            return hash((self.type, tuple(self.value)))


class NestedAttrType(BaseModel):
    pass


class BundleContent(BaseModel):
    said: "ReferenceAttrType"


class RefValueParsingErrorType(str, Enum):
    MissingColon = "MissingColon"
    UnknownTag = "UnknownTag"
    SaidError = "SaidError"


class RefValueParsingError(Exception):
    def __init__(
        self,
        error_type: RefValueParsingErrorType,
        message: str = "",
        inner_exception: Exception = None,
    ):
        self.error_type = error_type
        self.message = message
        self.inner_exception = inner_exception
        super().__init__(message)

    def __str__(self):
        if self.inner_exception:
            return f"{self.error_type.value}: {self.message} (caused by {self.inner_exception})"
        return f"{self.error_type.value}: {self.message}"


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
