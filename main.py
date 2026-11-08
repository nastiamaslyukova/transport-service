from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Transport Service API",
    description="Микросервис управления транспортными маршрутами",
    version="1.0.0"
)

# DTO (модели данных)
class RouteModel(BaseModel):
    id: int
    name: str
    start_point: str
    end_point: str
    distance_km: float

class RouteCreate(BaseModel):
    name: str
    start_point: str
    end_point: str
    distance_km: float

# In-memory хранилище данных (заглушка)
routes_db = [
    {"id": 1, "name": "Маршрут №1", "start_point": "Центр", "end_point": "Вокзал", "distance_km": 12.5}
]

@app.get("/api/v1/routes/", response_model=List[RouteModel], status_code=status.HTTP_200_OK)
def get_routes():
    """Получение списка всех маршрутов"""
    return routes_db

@app.get("/api/v1/routes/{id}", response_model=RouteModel, status_code=status.HTTP_200_OK)
def get_route(id: int):
    """Получение детальной информации о маршруте по ID"""
    for route in routes_db:
        if route["id"] == id:
            return route
    raise HTTPException(status_code=404, detail="Route not found")

@app.post("/api/v1/routes/", response_model=RouteModel, status_code=status.HTTP_201_CREATED)
def create_route(route: RouteCreate):
    """Создание нового маршрута"""
    new_id = max([r["id"] for r in routes_db], default=0) + 1
    new_route = {"id": new_id, **route.dict()}
    routes_db.append(new_route)
    return new_route

@app.delete("/api/v1/routes/{id}", status_code=status.HTTP_200_OK)
def delete_route(id: int):
    """Удаление маршрута по ID"""
    for index, route in enumerate(routes_db):
        if route["id"] == id:
            routes_db.pop(index)
            return {"detail": f"Route with id {id} successfully deleted"}
    raise HTTPException(status_code=404, detail="Route not found")