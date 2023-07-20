import asyncio
from db import db_insert
from models import CountryModel, BookModel
from asyncio import run

countries = [CountryModel(name="Poland", continent="Europe"),
             CountryModel(name="Great Britain", continent="Europe"),
             CountryModel(name="Germany", continent="Europe")]

books = [BookModel(title="Iluzjonista", author="Remigiusz Mroz", genre="crime",
                   year_published=2019, status="available", country_id=1),
         BookModel(title="Ekstremista", author="Remigiusz Mroz", genre="crime",
                   year_published=2021, status="available", country_id=1),
         BookModel(title="Duch Zaglady", author="Graham Masterton", genre="horror",
                   year_published=2021, status="available", country_id=2)
         ]


async def create_countries(dbi: db_insert()):

    for c in countries:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into countries(name, continent) values ($1, $2)",
                c.name, c.continent
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}

async def create_books(dbi: db_insert()):

    for b in books:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into books(title, author, genre, year_published, status, country_id) "
                "values ($1, $2, $3, $4, $5, $6)",
                b.title, b.author, b.genre, b.year_published, b.status, b.country_id
            )
    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def main():
    dbi = db_insert()
    await dbi.initialize()

    c = await create_countries(dbi)
    b = await create_books(dbi)

    return c, b

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(main())
