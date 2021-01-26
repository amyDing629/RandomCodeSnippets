-- Explorers Contest

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q4 cascade;

CREATE TABLE q4 (
    patronID CHAR(20)
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS Allcombine CASCADE;
DROP VIEW IF EXISTS eventroom CASCADE;
DROP VIEW IF EXISTS actualcombine CASCADE;
DROP VIEW IF EXISTS Nohappen CASCADE;
DROP VIEW IF EXISTS YearPatron CASCADE;

-- Define views for your intermediate steps here:
create view Allcombine as select year, id as wardid, patron from (select date_part('year', edate) as year from eventschedule group by date_part('year', edate)) as Allyear, (select id from ward) as AllWard, (select patron from Eventsignup group by patron) as Patrons;
create view eventroom as select date_part('year', edate) as year, room, patron from Eventsignup, eventschedule, libraryevent where eventsignup.event = eventschedule.event and id = eventsignup.event group by date_part('year', edate), room,patron;
create view actualcombine as select year, ward as wardid, patron from eventroom, libraryroom, librarybranch where room = id and library = code;
create view Nohappen as select year, patron from ((select* from Allcombine) except (select * from actualcombine) ) as NotIN group by year, patron;
create view YearPatron as select year, patron from (select date_part('year', edate) as year from eventschedule group by date_part('year', edate)) as Allyear, (select patron from Eventsignup group by patron) as Patrons;


-- Your query that answers the question goes below the "insert into" line:
insert into q4 (select patron as patronID from ((select *  from yearPatron) except (select * from Nohappen)) as explorers group by patron);

