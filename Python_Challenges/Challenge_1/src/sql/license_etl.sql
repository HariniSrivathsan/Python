
INSERT INTO license(license_id, business_name, address, city, state, start_dt)
select id, name, address, city, state, start_dt
from raw_license_start
where start_dt IS NOT NULL;


update
   license l
SET
   end_dt = e.end_dt
from  (select * from raw_license_end
	   where end_dt IS NOT NULL) e
where (l.license_id = e.id)and (l.business_name = e.name)and (e.end_dt = l.start_dt);


with unused_records as
(
    select r.* from raw_license_end r
    where not exists (select 1
				      from license l
				      where (r.id = l.license_id) and (r.name = l.business_name)
				      and (r.end_dt = l.end_dt) and l.end_dt IS NOT NULL)
     and  r.end_dt IS NOT NULL	)
update
   license l
SET
   end_dt = e.end_dt
from  (select * from unused_records) e
where (l.license_id = e.id)and (l.business_name = e.name)and (e.end_dt > l.start_dt)
  and  l.end_dt IS NULL;

with unused_records2 as
(
    select r.* from raw_license_end r
    where not exists (select 1
				      from license l
				      where (r.id = l.license_id) and (r.name = l.business_name)
				      and (r.end_dt = l.end_dt) and l.end_dt IS NOT NULL)
     and  r.end_dt IS NOT NULL	)
INSERT INTO license(license_id, business_name, address, city, state, end_dt)
select e.id, e.name, e.address, e.city, e.state, e.end_dt
from unused_records2 e;

INSERT INTO license(license_id, business_name, address, city, state, start_dt)
select s.id, s.name, s.address, s.city, s.state, s.start_dt from raw_license_start s
where
not exists (
                   select 1 from license l
	                where (s.id = l.license_id) and (s.name = l.business_name) and (l.start_dt IS NULL)
)
and
start_dt IS NULL;

INSERT INTO license(license_id, business_name, address, city, state, end_dt)
select
       e.id, e.name, e.address, e.city, e.state, e.end_dt
from raw_license_end e
where
not exists (
                   select 1 from license l
	                where (e.id = l.license_id) and (e.name = l.business_name) and (l.end_dt IS NULL)
)
and
end_dt IS NULL;