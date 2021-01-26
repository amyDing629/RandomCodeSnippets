-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS
    needchange, hasthur, nothur
    CASCADE;

create view needchange as
select distinct library, day from libraryhours where library not in
(select distinct library from libraryhours where
cast(day as text) = 'sun' or end_time > '18:00:00');

create view hasthur as select distinct library
from libraryhours where day = cast('thu' as  week_day);

create view nothur as
select distinct library, cast( 'thu' as week_day)  as day, cast( '18:00:00' as time) as start_time ,
cast( '21:00:00' as time)  as end_time
from libraryhours natural join needchange where library not in (select * from hasthur);

update libraryhours set end_time = cast('21:00:00' as time)
from needchange natural join hasthur where needchange.library = libraryhours.library
and cast(libraryhours.day as text) = 'thu';

INSERT INTO libraryhours SELECT library, day, start_time, end_time FROM nothur;





-- Define views for your intermediate steps here, and end with a
-- INSERT, DELETE, or UPDATE statement.