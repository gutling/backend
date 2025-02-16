from fastapi import Query, Body, Path, APIRouter

from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelPatch, Hotel
from src.api.dependencies import PaginationDep



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


@router.get('/{hotel_id}', summary='Получение отеля')
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)



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
    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}', summary='Полное изменение отеля')
async def put_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}', summary='Частичное изменение отеля')
async def patch_hotel(hotel_id:int,
                hotel_data: HotelPatch):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}', summary='Удаление отеля')
async def delete_hotel(hotel_id: int = Path(description='ID отеля')):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id = hotel_id)
        await session.commit()
    return {'status': 'OK'}