-- Devoted Fans

-- You must not change the next 2 lines or the table definition.
SET SEARCH_PATH TO Library, public;
DROP TABLE IF EXISTS q6 cascade;

CREATE TABLE q6 (
    patronID Char(20),
    devotedness INT
);


-- Do this for each of the views that define your intermediate steps.  
-- (But give them better names!) The IF EXISTS avoids generating an error 
-- the first time this file is imported.
DROP VIEW IF EXISTS singlecontributor CASCADE;
DROP VIEW IF EXISTS isbook CASCADE;
DROP VIEW IF EXISTS checksingle CASCADE;
DROP VIEW IF EXISTS satisfy1 CASCADE;
DROP VIEW IF EXISTS allcheckout CASCADE;
DROP VIEW IF EXISTS notReview CASCADE;
DROP VIEW IF EXISTS satisfy2 CASCADE;
DROP VIEW IF EXISTS lowrate CASCADE;
DROP VIEW IF EXISTS satisfy3 CASCADE;
DROP VIEW IF EXISTS notfan CASCADE;

-- Define views for your intermediate steps here:
create view singlecontributor as (select holding from holdingcontributor) except (select c1.holding from holdingcontributor c1, holdingcontributor c2 where c1.holding= c2.holding and c1.contributor > c2.contributor);
create view isbook as select id as holding, contributor from holdingcontributor, singlecontributor, holding where holdingcontributor.holding= singlecontributor.holding and singlecontributor.holding = id and htype= 'books';
create view checksingle as select distinct isbook.holding as holding, contributor, patron from isbook, checkout where isbook.holding=checkout.holding;
create view satisfy1 as select distinct c1.contributor as contributor, patron from (select contributor, count(holding) from isbook group by contributor) as c1, (select contributor, patron, count(holding) from checksingle group by contributor, patron)as c2 where c1.contributor = c2.contributor and c1.count-c2.count<=1;
create view allcheckout as select distinct satisfy1.patron as patron, isbook.holding as holding from isbook, satisfy1, checkout where isbook.contributor= satisfy1.contributor and isbook.holding = checkout.holding and satisfy1.patron = checkout.patron;
create view notReview as (select patron, holding from allcheckout ) except (select patron, holding from review);
create view satisfy2 as (select contributor, patron from satisfy1) except (select contributor, patron from (select c1.contributor as contributor, c1.patron as patron  from notreview, checksingle c1 where notreview.patron =c1.patron and notreview.holding=c1.holding) as notinit);
create view lowrate as select satisfy2.contributor as contributor, satisfy2.patron as patron from satisfy2, review, checksingle where satisfy2.contributor= checksingle.contributor and satisfy2.patron = review.patron and review.patron= checksingle.patron and review.holding = checksingle.holding group by satisfy2.contributor, satisfy2.patron having avg(stars)< 4;
create view satisfy3 as select patron, count(contributor) from ((select* from satisfy2) except (select* from lowrate)) as satisfy group by patron;
create view notfan as select card_number as patronID, 0 as devotedness from  ((select card_number from patron) except (select patron from satisfy3)) as nofan;

-- Your query that answers the question goes below the "insert into" line:
insert into q6 (select * from satisfy3) union (select * from notfan);
