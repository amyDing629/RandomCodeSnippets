-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.DROP VIEW IF EXISTS intermediate_step CASCADE;


-- You might find this helpful for solving update 1:
-- A mapping between the day of the week and its index

DROP VIEW IF EXISTS schedule CASCADE;
DROP VIEW IF EXISTS hours CASCADE;
DROP VIEW IF EXISTS outbound CASCADE;
DROP VIEW IF EXISTS deleevent CASCADE;
DROP VIEW IF EXISTS delesignup CASCADE;

-- You might find this helpful for solving update 1:
-- A mapping between the day of the week and its index
DROP VIEW IF EXISTS day_of_week CASCADE;
CREATE VIEW day_of_week (day, idx) AS
SELECT * FROM (
	VALUES ('sun', 0), ('mon', 1), ('tue', 2), ('wed', 3),
	       ('thu', 4), ('fri', 5), ('sat', 6)
) AS d(day, idx);


-- Define views for your intermediate steps here, and end with a
-- INSERT, DELETE, or UPDATE statement.
create view schedule as select event, edate,
extract(dow from edate) as dayofweeks, start_time, end_time from eventschedule;

create view hours as select library, idx, start_time, end_time
from libraryhours, day_of_week where cast(libraryhours.day as text) = day_of_week.day;
create view outbound as select event, edate from libraryevent, libraryroom, schedule, hours
where event = libraryevent.id and room = libraryroom.id and libraryroom.library=hours.library and dayofweeks = idx
and (schedule.start_time < hours.start_time or schedule.end_time > hours.end_time);

create view deleevent as (select event from outbound)
except
(select event from  ((select event, edate from eventschedule )
except (select * from outbound)) as notout);
create view delesignup as
select patron, eventsignup.event as event from eventsignup, deleevent
where eventsignup.event = deleevent.event;

delete from libraryevent using deleevent where id = event;
delete from eventschedule using outbound
where eventschedule.event = outbound.event and eventschedule.edate = outbound.edate;



-- Define views for your intermediate steps here, and end with a
-- INSERT, DELETE, or UPDATE statement.