from fastapi import FastAPI, Path

inventory = {
    1: {
        "name": "milk",
        "price": 4,
        "brand": "seoul"
    }
}

app = FastAPI()


# configuration : uvicorn python_file_name:app 식으로 run한다
# --reload 옵션 추가시 변경될때마다 다시 돌아간다
@app.get("/")
def home():
    # localhost:8000/docs -> 문서 자동 산출
    return {"Data": "testing"}


@app.get("/get-item/{item_id}/{name}")
# path에 여러 옵션을 줄 수 있다
# None이라고 명시하면 default값이 없다는 의미이다
# * 을 앞에 붙이면 path로 default값을 준 파라미터를 앞에 배치 가능
def get_item(*, item_id: int = Path(None, description="id는 2보다 작아야합니다", gt=0, lt=2), name: str):
    if len(name) > 0:
        for i in inventory:
            if inventory[i]['name'] == name:
                return inventory[i]
    return inventory[item_id]
