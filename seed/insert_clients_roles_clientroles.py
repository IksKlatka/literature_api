from db import db_insert
from models import ClientModel, RoleModel, ClientRole
from asyncio import run, create_task, gather
import asyncio
from passlib.hash import pbkdf2_sha256


clients = [ClientModel(first_name="John", last_name="Doe", email="doe.male@mail.com",
                       password = pbkdf2_sha256.hash("died_in_1987")),
           ClientModel(first_name="Jane", last_name="Doe", email="doe.female@mail.com",
                       password=pbkdf2_sha256.hash("died_in_1992")),
           ClientModel(first_name="N", last_name="N", email="no.name@mail.com",
                       password = pbkdf2_sha256.hash("who_am_i"))]

roles = [RoleModel(name="Administrator", tag="admin"),
         RoleModel(name="Super-Administrator", tag="super_admin"),
         RoleModel(name="Regular", tag="regular")]

client_roles = [ClientRole(client_id=1, role_id=3),
                ClientRole(client_id=2, role_id=2),
                ClientRole(client_id=3, role_id=1)]

async def create_clients(dbi: db_insert()):

    for c in clients:
        async with dbi.pool.acquire() as connection:
            record = await connection.fetchrow(
                "insert into clients(first_name, last_name, email, password) values ($1,$2,$3,$4)",
                c.first_name, c.last_name, c.email, c.password
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


async def main():

    dbi = db_insert()
    await dbi.initialize()

    tasks = [create_task(create_clients(dbi)),
             create_task(create_roles(dbi))]
    await gather(*tasks)

    await create_client_roles(dbi)

    # cc = await create_clients()
    # cr = await create_roles()
    # ccr = await create_client_roles()


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    run(main())
