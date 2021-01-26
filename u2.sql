-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS stillhold CASCADE;
DROP VIEW IF EXISTS indownsview CASCADE;
DROP VIEW IF EXISTS nofive CASCADE;
DROP VIEW IF EXISTS noseven CASCADE;
DROP VIEW IF EXISTS meetreq CASCADE;

-- Define views for your intermediate steps here, and end with a
-- INSERT, DELETE, or UPDATE statement.
create view stillhold as
select hold.id as id, patron, holding, checkout_time,library
from ((select id from checkout) except (select checkout from return)) as hold, checkout
where hold.id = checkout.id;

create view indownsview as select stillhold.id
as id, patron,holding,checkout_time from stillhold, librarybranch, holding
where library =code and name ='Downsview' and holding =holding.id and htype='books';

create view nofive as
select patron from indownsview group by patron having count(holding)<=5;

create view noseven as
(select * from nofive) except
(select distinct nofive.patron as patron from indownsview, nofive
where indownsview.patron= nofive.patron and current_date-(date(checkout_time)+21 )>7);

create view meetreq as select id, checkout_time from indownsview, noseven
where indownsview.patron = noseven.patron and current_date-(date(checkout_time)+21) > 0;

update checkout set checkout_time = date(meetreq.checkout_time)+interval '35 days'
from meetreq where meetreq.id = checkout.id;


-- Define views for your intermediate steps here, and end with a
-- INSERT, DELETE, or UPDATE statement.