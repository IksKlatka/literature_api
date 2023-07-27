import asyncio
from db_conf import db_insert
from asyncio import run
from datas import *


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
                "insert into books(title, author, genre, year_published, status, country_id, times_rented) "
                "values ($1, $2, $3, $4, $5, $6, $7)",
                b.title, b.author, b.genre, b.year_published, b.status, b.country_id, b.times_rented
            )
    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def create_clients(dbi: db_insert()):

    for c in clients:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into clients(first_name, last_name, email, password, no_books_rented) values ($1,$2,$3,$4,$5)",
                c.first_name, c.last_name, c.email, c.password, c.no_books_rented
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}

async def create_roles(dbi: db_insert()):

    for r in roles:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into roles(name, tag) values ($1,$2)",
                r.name, r.tag
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}

async def create_client_roles(dbi: db_insert()):

    for cr in client_roles:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into client_roles(client_id, role_id) values ($1,$2)",
                cr.client_id, cr.role_id
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def create_rents(dbi: db_insert()):

    for r in rents:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into book_rent(book_id, client_id, date_rented, date_returned, status ) "
                "values ($1, $2, $3, $4, $5)",
                r.book_id, r.client_id, r.date_rented, r.date_returned, r.status,
            )
    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong."}

# todo: clean database function

async def main():
    dbi = db_insert()
    await dbi.initialize()

    c = await create_countries(dbi)
    b = await create_books(dbi)
    ct = await create_clients(dbi)
    r = await create_roles(dbi)
    ctr = await create_client_roles(dbi)
    rt = await create_rents(dbi)

    return c, b, ct, r, ctr, rt

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(main())
