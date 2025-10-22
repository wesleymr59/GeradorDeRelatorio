from datetime import datetime
from pydantic import BaseModel

class Products(BaseModel):
    produto: str
    quantidade: int
    preco_unitario: float
    data: datetime