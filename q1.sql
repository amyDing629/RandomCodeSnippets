-- Branch Activity

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q1 cascade;

CREATE TABLE q1 (
    branch CHAR(5),
    year INT,
    events INT NOT NULL,
    sessions FLOAT NOT NULL,
    registration INT NOT NULL,
    holdings INT NOT NULL,
    checkouts INT NOT NULL,
    duration FLOAT
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.


-- Define views for your intermediate steps here:
DROP VIEW IF EXISTS
    eventschedule_mo, branch_eventname, top_five, eventsignup_mo,
    branch_holdings, checkout_mo, duration, years, all_comb
    CASCADE;

create view years as
select * from
(select 2015 x union select 2016 union select 2017 union select 2018 union
select 2019) A;

create view all_comb as
select code as branch, x as year
from librarybranch, years;

create view eventschedule_mo as
select date_part('year', edate) as year, event, count(start_time) as session
from eventschedule
group by date_part('year', edate), event;

create view branch_eventname as
select library as branch, libraryevent.id as event
from libraryroom,libraryevent
where room = libraryroom.id;

create view eventsignup_mo as
select event, count(patron) as reg
from eventsignup
group by event;

create view top_five as
select branch, year, count(event) as events, sum(session)/count(session) as sessions, sum(reg) as registration
from all_comb natural left join (branch_eventname natural left join eventschedule_mo natural left join eventsignup_mo)
group by branch, year;

create view branch_holdings as
select library as branch, sum(num_holdings) as holdings
from librarycatalogue
group by branch;

create view checkout_mo as
select library as branch, date_part('year', checkout_time) as year, count(*) as checkouts
from checkout
group by library, date_part('year', checkout_time);

create view duration as
select library as branch, date_part('year', checkout_time) as year, avg(date(return_time) - date(checkout_time)) as duration
from checkout, return
where checkout.id = return.checkout
group by library, date_part('year', checkout_time);


-- Your query that answers the question goes below the "insert into" line:
insert into q1
select branch, year, COALESCE(events, 0) as events, COALESCE(sessions, 0) as sessions, COALESCE(registration, 0) as registration
, COALESCE(holdings, 0) as holdings, COALESCE(checkouts, 0) as checkouts, COALESCE(duration, 0) as duration
from all_comb natural left join
top_five natural left join branch_holdings natural left join checkout_mo natural left join duration;


