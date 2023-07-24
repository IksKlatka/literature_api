from models import *
from passlib.hash import pbkdf2_sha256
from datetime import date

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

clients = [ClientModel(first_name="John", last_name="Doe", email="doe.male@mail.com",
                       password = pbkdf2_sha256.hash("died_in_1987")),
           ClientModel(first_name="Jane", last_name="Doe", email="doe.female@mail.com",
                       password=pbkdf2_sha256.hash("died_in_1992")),
           ClientModel(first_name="N", last_name="N", email="no.name@mail.com",
                       password = pbkdf2_sha256.hash("who_am_i"))]

roles = [RoleModel(name="Administrator", tag="admin"),
         RoleModel(name="Super-Administrator", tag="super_admin"),
         RoleModel(name="Regular", tag="regular")]

client_roles = [ClientRoleModel(client_id=1, role_id=3),
                ClientRoleModel(client_id=2, role_id=2),
                ClientRoleModel(client_id=3, role_id=1)]

rents = [BookRentModel(book_id=1, client_id=1,
                       date_rented=date(2023, 6, 29),
                       date_returned=date(2023, 7, 17),
                       status="returned"),
         BookRentModel(book_id=2, client_id=2,
                       date_rented=date(2023, 4, 13),
                       date_returned=date(2023, 6, 13),
                       status="returned"),
         BookRentModel(book_id=2, client_id=3,
                       date_rented=date(2023, 7, 1),
                       date_returned=date(2023, 7, 22), status="returned")]

