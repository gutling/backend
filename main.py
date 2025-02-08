from fastapi import FastAPI, Query, Path, Body
import uvicorn

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": 'Сочи'},
    {"id": 2, "title": "Дубай", 'name': 'Дубай'},
]

@app.get('/hotels')
def get_hotels(id: int | None = Query(None, description='ID отеля'),
               title: str | None = Query(None, description='Название отеля')):
    _hotels = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        _hotels.append(hotel)
    return _hotels


@app.post('/hotels')
def create_hotel(title: str = Body(embed=True)):
    global hotels
    hotels.append(
        {'id': hotels[-1]['id'] + 1,
                'title': title
    })


@app.put('/hotels/{hotel_id}')
def put_hotel(hotel_id: int, title: str = Body(), name: str = Body()):
    global hotels
    if hotel_id and title and name:
        i = 0
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                _hotel = {'id': hotel_id, 'title': title, 'name': name}
                hotels[i] = _hotel
                return hotels
            i += 1
    return {'message': 'Укажите все данные'}


@app.patch('/hotels/{hotel_id}')
def patch_hotel(hotel_id:int,
                title: str = Body(default=None),
                name: str = Body(None)):
    i = 0
    if title or name:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                if title and not name:
                    hotel['title'] = title
                    hotels[i] = hotel
                elif name and not title:
                    hotel['name'] = name
                    hotels[i] = hotel
                else:
                    hotel['title'] = title
                    hotel['name'] = name
                    hotels[i] = hotel
                return hotels
            i += 1
    return {'message': 'Введите title или name отеля'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int = Path(description='ID отеля')):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)