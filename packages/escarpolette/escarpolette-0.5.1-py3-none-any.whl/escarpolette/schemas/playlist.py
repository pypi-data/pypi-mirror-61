from typing import List

from pydantic.main import BaseModel

from escarpolette.schemas.item import ItemSchemaOut


class PlaylistSchemaOut(BaseModel):
    items: List[ItemSchemaOut] = []
    idx: int = 0
