# Introduction:

Foreword:
---------
Chapter 3 introduces us to concepts that will help us building our own blog

What is a Database?
-------------------
A database is a program that stores and retrieves large amounts of data

Why Databases?
--------------
Problems with querying by hand:
	+ error-prone
	+ tedious
	+ most importanty slow. Imagine million or a billion entries and the time it takes to sort the entries and return a result. You may not even be able to get the result by having this in memory

So, databases exist to take in big amount of data and search a result in a reasonable amount of time

Types of Databases:
-------------------
+ Relational Databases ( SQL )
	- Postgresql (Reddit, Hipmunk)
	- MySQL (Facebook and everybody)
	- SQLite
	- Oracle, bought MySQL
	- Google App Engine's Datastore
	- [Dynamo](http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf)

Structured Query Language (SQL):
--------------------------------
You use SQL to query relational database to get data out of the database invented in the 1970's much before the existance of the Internet.

Ex: SELECT * FROM links where id = 5;
where:
- SELECT : fetch data
- '\*'   : all columns (can be a list of columns)
- links  : table
- id = 5 : constraint

Sharding the Database:
----------------------
Spreading the data across multiple machines
	- Google's spanner shards the data across multiple PAXOS state machines

Atomicity, Consistency, Isolation, Durability (ACID):
----------------------------------------------------
Atomicity: All parts of a transaction succeed or fail together
Consistency: Database will always be consistent
Isolation: No transaction can interfere with each other(locking, mutexex)
Durability: Once a transaction is committed there's no way to lose the data

[Google App Engine Datastore](https://cloud.google.com/appengine/docs/python/datastore/):
----------------------------
Database provided by Google App Engine

Features:
	- GQL - simplified version of SQL that only works with App Engine
	- all queries should start with "select *"
	- no joins
	- all queries must be indexed
	- datastore is both sharded and replicated
	- columns are not fixed
	- all have an ID 

Notes:
------
- CSS styling was introduced in last lecture of Chapter 3(Styling)
