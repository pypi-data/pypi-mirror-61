from enum import Enum
from typing import List, Dict, Optional

from pydantic import BaseModel


class SimplePermission(BaseModel):
    name: str
    uri: str


class PermissionEnum(str, Enum):
    admin = "m"
    delete = "d"
    deploy = "w"
    annotate = "n"
    read = "r"


class PrincipalsPermission(BaseModel):
    users: Optional[Dict[str, List[PermissionEnum]]] = None
    groups: Optional[Dict[str, List[PermissionEnum]]] = None


class Permission(BaseModel):
    name: str
    includesPattern: str = "**"
    excludesPattern: str = ""
    repositories: List[str]
    principals: PrincipalsPermission
