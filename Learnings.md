1. Virtual Environments

   - Example:
     - Project 1
       - Fastapi v1.2.3
       - System -> Fastapi v1.2.3
     - Project 2
       - Fast api v2.4.5
       - System -> Upgrade to v 2.4.5?
         - Is it backward compatible
   - Venv example:
     - Project 1
       - Venv1
         - Fastapi v1.2.3 -> Isolated
     - Project 2
       - Venv 2
         - Fast api v2.4.5 -> Isolated
     - System -> Doesn't pollute it
   - Virtual environment provide a fresh, isolated environment for libraries and frameworks to exist without polluting the global environment
   - Command
     ```bash
         python3 -m venv <name>
     ```
   - Activate Command
     ```bash
         source ./venv/bin/activate
     ```
   - VSCode -> Select the interpreter

2. Run command

   - ```bash
         uvicorn main:app
     ```
   - `main`: the file `main.py`(the Python "module")
   - `app`: the object created inside of `main.py` with the line `app = FastAPI`
   - `--reload`: makes the server restart after code changes. Only use for development.

3. Path Operation

   - ```python
       @app.get("/")
       def root():
           return {"message": "Hello World!"}
     ```
   - `app` => FastAPI
   - `get` => HTTP Method
   - `/` => Path
   - `root` => Function that performs all the logic and returns data to the user

4. Order of Execution

   - FastAPI returns from the first matched path
   - Therefore, order is important

5. Schema

   - Explicitly define what the data should look like(a contract)
   - Why do we need it?
     - It's a pain to extract values from the body
     - The client can send whatever data they want
     - The data isn't getting validated
     - We ultimately want to force the client to send data in a schema that we expect
   - [`Pydantic`](https://docs.pydantic.dev/) to define schema

6. CRUD

   - Create
     - `POST`
     - `/posts`
       ```python
         @app.post("/posts")
       ```
   - Read
     - `GET`
     - `/posts:id`
       ```python
         @app.get("/posts/{id}")
       ```
     - `/posts`
       ```python
         @app.get("/posts")
       ```
   - Update
     - `PUT/PATCH`
     - `/posts/:id`
       ```python
         @app.put("/posts/{id}")
       ```
     - `PUT` => Have to send all the data
     - `PATCH` => Can only send the updated data
   - Delete
     - `DELETE`
     - `/posts/:id`
       ```python
         @app.delete("/posts/{id}")
       ```
   - Standard convention
     - Use plural
     - Above url format

7. Documentation

   - FastAPI auto generates documentation. There are two ways to generate documentation.
     1. `<API_URL>/docs` via `Swagger`
     2. `<API_URL>/redoc` via `Redocly`

8. Database

   - Database is a collection of organized data that can be easily accessed and managed
   - DBMS
     - Database management system
     - We don't work or interact with the database directly
     - Pattern(Abstraction) => High level API rather than low level API
     - Popular DBMS
       - Relational
         - MySQL
         - PostgreSQL
         - Oracle
         - SQL Server
       - NoSQL
         - MongoDB
         - DynamoDB
         - Oracle
         - SQL Server
   - Relational Database & SQL
     - Structured Query Language(SQL) - Language used to communicated with DBMS
   - Postgres
     - Fact: Each instance of postgres can be carved into multiple separate databases(can achieve isolation)
     - By default "postgres" database is present on installation
       - This is required because if we need to connect to a Postgres instance, then a database is required
   - Table
     - A table represents a subject or an event in an application
     - The perform a relationship with other tables in the database
     - Important to map out the relationship before creating the database
     - A table is made up of columns and rows
       - Columns vs Rows
         - Each column represents a different attribute
         - Each row represents a different entity in the table
       - Postgres Datatype
         - Need to specify Datatypes for each column
         - | Datatype | Postgres               | Python     |
           | -------- | ---------------------- | ---------- |
           | Numeric  | Int, Decimal Precision | Int, Float |
           | Text     | Varchar, text          | string     |
           | bool     | boolean                | boolean    |
           | sequence | array                  | list       |
       - Primary Key
         - Is a column or a group of columns that uniquely identifies each row in a table
         - Table can have one and only one primary key
       - Constraints
         - A constraint can be applied to any column
         - Unique constriants
           - makes sure every record has a unique value for that column
         - Null Constraints
           - By default, when adding a new entry to the database, any column can be left blank. When a column is left blank, it has a null value.
           - If you need column to be properly filled in to create a new record, a NOT NULL constraint can be added to the column to ensure is never left blank
       - Composite Key
         - Primary key that spans multiple columns

9. Object Relational Mapper(ORM)

   - Layer of abstraction that sits between the database and us
   - We can perform all database operations through traditional Python code. No more SQL!
   - What can ORMs do?
     - Instead of manually defining tables in postgres, we ca define our tables as python codes
     - Queries can be made exclusively through python code.
   - ORMs understand language; they donot directly communicate with the database
   - ORMs utilize database driver to communicate with the database; e.g. here psycopg is used

10. Pydantic vs ORM models

    - Schema Models
      - Schema/Pydantic models define the structure of a request & response
      - The models ensures the body has the correct type and filled data as required
    - ORM models
      - Responsible for defining the columns of the database
      - Is used to perform CRUD operations

11. Relational DB - Relationships

    - Foreign key
      - Column that identifies the relationship between tables
