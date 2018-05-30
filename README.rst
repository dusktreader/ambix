*******
 ambix
*******

-----------------------------
alembic history cleaning tool
-----------------------------
The ambix tool is intended to be used to clean up alembic histories. It can
flatten badly branched alembic histories by using a toplogical sort. It can
also delete a migration with a specific revision.

WARNING
-------
The ambix tool is able to re-write your alembic python scripts and delete them.
Use mindfully, and make sure that you have used version control or some other
mechanism to backup your migration folder before you use ambix.

Requirements
------------
 - Python 3.4+

Installing
----------
Install using pip::

  $ pip install ambix

Using
-----
To flatten alembic migrations, run the following command::

  $ ambix-flatten <your-migration-directory>

To delete a specific revision, run the following command::

  $ ambix-prune <your-migration-directory> <id-of-revision-to-delete>

To rebase a migration on different bases, run the following command:

  $ ambix-rebase <your-migration-directory> <id-of-revision-to-rebase> <id-of-first-new-base> <id-of-second-new-base> ...
