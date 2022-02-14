#Read me

This repository is mostly about doing CRUD operations on mysql database using fastAPI as backend and sqlAlchemy as ORM.

follow this commands to run this application

1.pip install fastapi uvicorn pymysql sqlalchemy
2.uvicorn index:app --reload

alembic is a migration tool, used it here for schema change

you need to write the code for setup class and tear down class, such that whatever records are created in testing database 
will be dropped down when testing is done, so when running testing again so database will be empty and works just fine.

Basic testing is done.
to run this testing file use this command

pyhton -m unittest tests.test_database