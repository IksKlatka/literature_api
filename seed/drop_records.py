import asyncio
from db_conf import db_connection
from asyncio import run
from datas import *


async def drop_countries(dbi: db_connection()):
    for c, country in enumerate(countries):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from countries where id = $1", c+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def drop_books(dbi: db_connection()):

    for b, book in enumerate(books):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from books where id=$1", b+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def drop_clients(dbi: db_connection()):

    for c, client in enumerate(clients):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from clients where id=$1", c+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}

async def drop_roles(dbi: db_connection()):

    for r, role in enumerate(roles):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from roles where id=$1", r+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}

async def drop_client_roles(dbi: db_connection()):

    for cr, client_role in enumerate(client_roles):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from client_roles where id=$1", cr+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong"}


async def drop_rents(dbi: db_connection()):

    for r, rent in enumerate(rents):
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "delete from book_rent where id=$1", r+1
            )

    if record:
        return {"message": "everything ok"}
    return {"message": "something went wrong."}


async def main():
    dbd = db_connection()
    await dbd.initialize()

    # c = await drop_countries(dbd)
    # b = await drop_books(dbd)
    # ct = await drop_clients(dbd)
    # r = await drop_roles(dbd)
    # ctr = await drop_client_roles(dbd)
    rt = await drop_rents(dbd)

    # return c, b, ct, r, ctr, rt
    return rt

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(main())

