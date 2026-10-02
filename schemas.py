"""Define accepted API data and response formats."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

TicketStatus = Literal["open", "in_progress", "closed"]


class TicketCreate(BaseModel):
    # Trim surrounding whitespace and reject unexpected fields.
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1)
    description: str = Field(min_length=1)


class TicketUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: TicketStatus

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, value):
        # Normalize before checking the allowed status values.
        if isinstance(value, str):
            return value.strip().lower()
        return value


class TicketRead(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
