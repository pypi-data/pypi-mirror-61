An interface for using plain SQL, in files.
=============================================

Does writing complex queries in an ORM feel like driving with the handbrake on?
Embrace SQL! Put your SQL queries in regular ``.sql`` files, and embrace will
load them.

Usage::

    import embrace

    # Connect to your database, using any db-api connector.
    # If python supports it, so does embrace.
    conn = psycopg2.connect("postgresql:///mydb")

    # Create a module populated with queries from a collection of *.sql files:
    queries = embrace.module("resources/sql", conn)

    # Run a query
    users = queries.list_users(order_by='created_at')

Your query would be specified like this::

    -- :name list_users :many
    select * from users where active = :active order by :identifier:order_by


By embrace returns rows using the underlying db-api cursor. Most db-api libraries have cursor types that return dicts or namedtuples. For example in Postgresql you could do this::

    conn = psycopg2.connect(
        "postgresql:///mydb",
        cursor_factory=psycopg2.extras.NamedTupleCursor)
    )

What types can queries return?
------------------------------

Many rows:
::

    -- :name list_users :many
    select * from users

A single row:

::

    -- :name get_user_by_id :one
    select * from users where id=:id

A single value:

::

    -- :name get_user_count :scalar
    select count(1) from users


An iterable over a single column:

::

    -- :name get_ips :column
    select distinct ip_addr from connections


A single file may contain multiple queries, separated by a structured SQL
comment. For example to create two query objects accessible as
``queries.list_users()`` and ``queries.get_user_by_id()``:

::

    -- :name list_users :many
    select * from users

    -- :name get_user_by_id :one
    select * from users where id=:id

But if you *don't* have the separating comment, embrace-sql can run
multiple statements in a single query call, returning the result from just the last one.

Why? Because it makes this possible in MySQL:


::

    -- :name create_user :column
    insert into users (name, email) values (:name, :email);
    select last_insert_id();


How do parameters work?
------------------------

Placeholders inserted using the ``:name`` syntax are escaped by the db-api
driver:

::

    -- Outputs `select * from user where name = 'o''brien'`;
    select * from users where name = :name

You can interpolate lists and tuples too:

``:tuple:`` creates a placeholder like this ``(?, ?, ?)``

``:value*:`` creates a placeholder like this ``?, ?, ?``

``:tuple*`` creates a placeholder like this ``(?, ?, ?), (?, ?, ?), …``
(useful for multiple insert queries)

::

    -- Call this with `queries.insert_foo(data=(1, 2, 3))`
    INSERT INTO foo (a, b, c) VALUES :tuple:data

    -- Call this with `queries.get_matching_users(names=("carolyn", "douglas"))`
    SELECT * from users WHERE name in (:values*:names)


You can escape identifiers with ``:identifier:``, like this:

::

    -- Outputs `select * from "some random table"`
    select * from :identifier:table_name

You can pass through raw sql too. This leaves you open to SQL injection attacks if you allow user input into such parameters:

::

    -- Outputs `select * from users order by name desc`
    select * from users order by :raw:order_clause


