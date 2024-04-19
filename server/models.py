from pydantic import BaseModel, conlist, conint
from typing import List, Tuple

class RectangleRequest(BaseModel):
    image_base64: str
    rectangle_coords: List[Tuple[conint(ge=0), conint(ge=0), conint(gt=0), conint(gt=0)]]
    color: conlist(conint(ge=0, le=255), min_length=3, max_length=3) = [0, 0, 0]
    thickness: conint(gt=0) = 1
