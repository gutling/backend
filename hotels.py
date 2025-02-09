from tkinter.scrolledtext import example

from fastapi import FastAPI, Query, Body, Path, APIRouter
from pyexpat.errors import messages

from schemas.hotels import HotelPatch, Hotel

Hotel
router = APIRouter(prefix='/hotels')


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
def get_hotels(id: int | None = Query(None, description='ID отеля'),
               title: str | None = Query(None, description='Название отеля'),
               page: int | None = Query(1, description='Номер страницы'),
               per_page: int | None = Query(3, description='Кол-во отелей на странице')):
    _hotels = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        _hotels.append(hotel)
    if page * per_page <= len(_hotels):
        slise_finish: int = page * per_page
        slice_start: int = slise_finish - per_page
        return _hotels[slice_start:slise_finish]
    return {'message': 'Количество запрашиваемых отелей превышает число доступных'}




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