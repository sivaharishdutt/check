#Read me

This repository is mostly about doing CRUD operations on mysql database using fastAPI as backend and sqlAlchemy as ORM.

follow this commands to run this application

1.pip install fastapi uvicorn pymysql sqlalchemy
2.uvicorn index:app --reload

alembic is a migration tool, used it here for schema change

Basic testing is done.

to run this testing file use this command

pyhton -m unittest tests.test_database