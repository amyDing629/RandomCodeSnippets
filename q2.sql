-- Overdue Items

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q2 cascade;

create table q2 (
    branch CHAR(5),
    email TEXT,
    title TEXT,
    overdue INT
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS noreturn CASCADE;
DROP VIEW IF EXISTS Inpark CASCADE;
DROP VIEW IF EXISTS estimate CASCADE;
DROP VIEW IF EXISTS overdate CASCADE;

-- Define views for your intermediate steps here:
create view noreturn as
(select id from checkout) except (select checkout as id from return) ;

create view Inpark as
select code, patron, holding, checkout_time
from checkout, librarybranch,ward, noreturn
where checkout.id= noreturn.id and library = code and ward.id=librarybranch.ward and ward.name = 'Parkdale-High Park';

create view estimate as
(select code, patron, title,date(checkout_time)+21 as duedate from holding, Inpark
where id = holding and (htype = 'books' or htype = 'audiobooks')) union (select code, patron, title, date(checkout_time)+7 as duedate from holding , inpark where id = holding and (htype ='music' or htype = 'movies' or htype = 'magazines and newspapers'));

create view overdate as
select code as library, email, title, current_date-duedate as overdue from patron, estimate
where card_number = patron and current_date>duedate;


-- Your query that answers the question goes below the "insert into" line:
insert into q2 (select * from overdate);

