from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field, RootModel


class EnvVar(BaseModel):
    name: str
    value: str


class GitInput(BaseModel):
    url: str
    input_type: Literal["git"] = "git"
    includes_submodules: bool = False
    revision: Optional[str] = None


class ArchiveInput(BaseModel):
    input_type: Literal["archive"] = "archive"
    url: Optional[str] = None


class NPMProjectDependency(BaseModel):
    tool: Literal["npm", "yarn", "pnpm"]
    lockfile: bool
    node_version: Optional[str] = None


class ProjectDependency(BaseModel):
    npm: Optional[NPMProjectDependency] = None
    foundry: Optional[bool] = False


class ProjectInfo(BaseModel):
    name: str
    project_root: str
    env_vars: list[EnvVar] = Field(default_factory=list)
    dependencies: Optional[ProjectDependency] = None
    build_system: Optional[Literal["hardhat", "hardhat-ignition", "foundry"]] = None
    contents: Optional[list[Literal["circom", "solidity", "picus", "llzk"]]] = Field(
        default_factory=list
    )
    src_path: str
    include_path: Optional[str] = None
    specs_path: Optional[str] = None
    hints_path: Optional[str] = None
    deployment_script_path: Optional[str] = None
    input_info: GitInput | ArchiveInput


class Project(ProjectInfo):
    id: int
    created_at: datetime


class IdAndMessageResponse(BaseModel):
    id: int
    message: str


class UserProfile(BaseModel):
    id: str
    name: str
    email: str
    rights: list[str]
    disable_online_notifications: bool
    disable_digest_notifications: bool


class OrganizationAccessRestriction(BaseModel):
    function: str
    value: Optional[int] = None
    detector: Optional[str] = None


OrganizationAccessRestrictions = RootModel[list[OrganizationAccessRestriction]]
