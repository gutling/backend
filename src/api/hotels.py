from fastapi import Query, Body, Path, APIRouter

from src.schemas.hotels import HotelPatch, Hotel
from src.api.dependencies import PaginationDep


router = APIRouter(prefix='/models')


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('', summary='Получение отелей')
def get_hotels(pagination: PaginationDep,
               id: int | None = Query(None, description='ID отеля'),
               title: str | None = Query(None, description='Название отеля')):
    _hotels = []

    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        _hotels.append(hotel)
    if pagination.per_page and pagination.page:
        return _hotels[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return _hotels




examples = {
    '1': {'summary': 'Сочи',
          'value':
              {
                  'title': 'Прекрасный отель в Сочи',
                  'name': 'Отель SochiHotel'
              }
          },
    '2': {'summary': 'Дубай',
          'value':
              {
                  'title': 'Прекрасный отель в Дубайске',
                  'name': 'Отель ДубайскHotel'
              }
          }
}


@router.post('', summary='Запись нового отеля')
def create_hotel(hotel_data: Hotel = Body(openapi_examples=examples)):
    global hotels
    hotels.append(
        {'id': hotels[-1]['id'] + 1,
         'title': hotel_data.title,
         'name': hotel_data.name
    })
    return {'message': 'OK'}


@router.put('/{hotel_id}', summary='Полное изменение отеля')
def put_hotel(hotel_id: int, hotel_data:  Hotel):
    global hotels
    if hotel_id and hotel_data.title and hotel_data.name:
        i = 0
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                _hotel = {'id': hotel_id, 'title': hotel_data.title, 'name': hotel_data.name}
                hotels[i] = _hotel
                return hotels
            i += 1
    return {'message': 'Укажите все данные'}


@router.patch('/{hotel_id}', summary='Частичное изменение отеля')
def patch_hotel(hotel_id:int,
                hotel_data: HotelPatch):
    i = 0
    if hotel_data.title or hotel_data.name:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                if hotel_data.title and not hotel_data.name:
                    hotel['title'] = hotel_data.title
                    hotels[i] = hotel
                elif hotel_data.name and not hotel_data.title:
                    hotel['name'] = hotel_data.name
                    hotels[i] = hotel
                else:
                    hotel['title'] = hotel_data.title
                    hotel['name'] = hotel_data.name
                    hotels[i] = hotel
                return hotels
            i += 1
    return {'message': 'Введите title или name отеля'}


@router.delete('/{hotel_id}', summary='Удаление отеля')
def delete_hotel(hotel_id: int = Path(description='ID отеля')):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}