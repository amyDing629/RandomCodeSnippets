-- Lure Them Back

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q5 cascade;

CREATE TABLE q5 (
    patronID CHAR(20),
    email TEXT NOT NULL,
    usage INT,
    decline INT,
    missed INT
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS
    checkoutcount, differentitems, missedmonths, declinebooks, allactive2018, halfactive2019, active2020, noactive2020, patronrequired, rst
    CASCADE;

create view checkoutcount as
select patron, date_part('year', checkout_time) as years, date_part('month', checkout_time) as months, count(*) as cc_eachmonth
from checkout
group by patron, date_part('year', checkout_time), date_part('month', checkout_time);

create view differentitems as
select patron, count(distinct holding) as usages
from checkout
group by patron;

create view missedmonths as
select patron, (12 - count(months)) as missed
from checkoutcount
group by patron, years
having years = 2019;

create view declinebooks as
select patron, cc_2018 - cc_2019 as decline
from (select patron, sum(cc_eachmonth) as cc_2019
from checkoutcount
group by patron, years
having years = 2019) table2019 natural join
(select patron, sum(cc_eachmonth) as cc_2018
from checkoutcount
group by patron, years
having years = 2018) table2018;

create view allactive2018 as
select patron
from checkoutcount
group by patron, years
having years = 2018 and count(distinct months) = 12;

create view halfactive2019 as
select patron
from checkoutcount
group by patron, years
having years = 2019 and count(distinct months) >= 5 and count(distinct months) <= 11;

create view active2020 as
select patron
from checkoutcount
group by patron, years
having years = 2020;

create view noactive2020 as
select card_number as patron from patron
where card_number not in (select patron from active2020);

create view patronrequired as
select patron from
(allactive2018 natural join halfactive2019 natural join noactive2020);

create view rst as
select patron as patronID, COALESCE(email, 'none') as email, usages as usage, decline, missed
from patronrequired natural left join differentitems natural join patron natural join declinebooks natural join missedmonths
where patron.card_number = patron;

-- Define views for your intermediate steps here:


-- Your query that answers the question goes below the "insert into" line:
insert into q5
select * from rst;