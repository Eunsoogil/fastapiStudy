from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


inventory = {}


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


# configuration : uvicorn python_file_name:app 식으로 run한다
# --reload 옵션 추가시 변경될때마다 다시 돌아간다
@app.get("/")
def home():
    # localhost:8000/docs -> 문서 자동 산출
    return {"Data": "testing"}


@app.get("/get-item/{item_id}")
# path에 여러 옵션을 줄 수 있다
# None이라고 명시하면 default값이 없다는 의미이다
# * 을 앞에 붙이면 path로 default값을 준 파라미터를 앞에 배치 가능
def get_item(*, item_id: int = Path(None, description="id는 2보다 작아야합니다", gt=0, lt=2), name: Optional[str] = None):
    if name is not None:
        for i in inventory:
            if inventory[i].name == name:
                return inventory[i]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='해당 이름이 없습니다')
    return inventory[item_id]


@app.post('/create-item/{item_id}')
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='아이템이 존재하지 않습니다')

    inventory[item_id] = item
    return inventory[item_id]


@app.patch("/update-item/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='아이템이 존재하지 않습니다')

    if item.name is not None:
        inventory[item_id].name = item.name

    if item.price is not None:
        inventory[item_id].price = item.price

    if item.brand is not None:
        inventory[item_id].brand = item.brand

    return inventory[item_id]


@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="아이템의 id", gt=0),):
    if item_id not in inventory:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='아이템이 존재하지 않습니다')

    del inventory[item_id]
    return {'message': '성공'}
