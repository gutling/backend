from pydoc import locate

from fastapi import Query, Body, Path, APIRouter
from sqlalchemy.sql.operators import like_op
from watchfiles import awatch

from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, Hotel
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsORM

from sqlalchemy import insert, select, func


router = APIRouter(prefix="/hotels", tags=["Отели"])




@router.get('', summary='Получение отелей')
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description='Местоположение отеля'),
        title: str | None = Query(None, description='Название отеля')):

    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session
                                      ).get_all(location=location,
                                      title=title,
                                      limit=per_page,
                                      offset=per_page * (pagination.page - 1))


@router.post('', summary='Запись нового отеля')
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': 'Сочи',
          'value':
              {
                  'title': 'Прекрасный отель в Сочи',
                  'location': 'Улица Моря, д. 5'
              }
          },
    '2': {'summary': 'Дубай',
          'value':
              {
                  'title': 'Прекрасный отель в Дубайске',
                  'location': 'Улица Ракушкина, д. 12'
              }
          }
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {'message': 'OK', 'data': hotel}


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
    if hotel_data.title or hotel_data.location:
        for hotel in hotels:
            if hotel['id'] == hotel_id:
                if hotel_data.title and not hotel_data.location:
                    hotel['title'] = hotel_data.title
                    hotels[i] = hotel
                elif hotel_data.location and not hotel_data.title:
                    hotel['location'] = hotel_data.location
                    hotels[i] = hotel
                else:
                    hotel['title'] = hotel_data.title
                    hotel['location'] = hotel_data.location
                    hotels[i] = hotel
                return hotels
            i += 1
    return {'message': 'Введите title или name отеля'}


@router.delete('/{hotel_id}', summary='Удаление отеля')
def delete_hotel(hotel_id: int = Path(description='ID отеля')):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}