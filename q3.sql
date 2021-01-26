-- Promotion

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q3 cascade;

create domain patronCategory as varchar(10)
  check (value in ('inactive', 'reader', 'doer', 'keener'));

create table q3 (
    patronID Char(20),
    category patronCategory
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS
    lib_patron_book, patron_totalcheckouts, patron_totalevents,
    lib_patron_event, categories, full_com,
    patron_libraries, patron_avr, rst, patrons_samelibrarybook, patrons_samelibraryevent
    ,patrons_avrbook, patrons_avrevent
    CASCADE;

create view patron_totalcheckouts as select patron, count(*) as tc from checkout group by patron;

create view patron_totalevents as select patron, count(*) as te from eventsignup group by patron;

create view lib_patron_book as select distinct patron, library from checkout;

create view lib_patron_event as select distinct patron, library from eventsignup, libraryevent, libraryroom
where event = libraryevent.id and libraryroom.id = libraryevent.room;

create view patron_libraries as (select * from lib_patron_book) union (select * from lib_patron_event);

create view patrons_samelibrarybook as
select distinct pl.patron as patron, pb.patron as compare
from patron_libraries as pl, lib_patron_book as pb
where pl.library = pb.library;

create view patrons_avrbook as
select distinct patrons_samelibrarybook.patron, avg(tc) as avg_tc
from patrons_samelibrarybook, patron_totalcheckouts
where compare = patron_totalcheckouts.patron
group by patrons_samelibrarybook.patron;

create view patrons_samelibraryevent as
select distinct pl.patron as patron, pe.patron as compare
from patron_libraries as pl, lib_patron_event as pe
where pl.library = pe.library;

create view patrons_avrevent as
select patrons_samelibraryevent.patron, avg(te) as avg_te
from patrons_samelibraryevent, patron_totalevents
where compare = patron_totalevents.patron
group by patrons_samelibraryevent.patron;

create view patron_avr as
select patron as patron, avg_tc, avg_te
from (select distinct patron from patron_libraries)a natural left join patrons_avrbook natural left join patrons_avrevent;

create view full_com as
select patron, avg_tc, avg_te, coalesce(tc, 0) as tc, coalesce(te, 0) as te
from patron_avr natural left join patron_totalcheckouts natural left join patron_totalevents;

create view categories as
select patron, (case
when tc < 0.25 * avg_tc and te < 0.25 * avg_te
then 'inactive'
when tc > 0.75 * avg_tc and te > 0.75 * avg_te
then 'keener'
when tc > 0.75 * avg_tc and te < 0.25 * avg_te
then 'reader'
when tc < 0.25 * avg_tc and te > 0.75 * avg_te
then 'doer'
else null end) category
from full_com;

create view rst as
select card_number, category
from patron left join categories on card_number = patron;

-- Define views for your intermediate steps here:
select * from patron_avr;

-- Your query that answers the question goes below the "insert into" line:
insert into q3
select * from rst;