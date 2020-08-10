INSERT INTO Inspection_Stats(business_name)
select lower(trim(dba_name)) as business_name
from raw_inspection
group by lower(TRIM(dba_name))
ORDER BY lower(TRIM(dba_name));



with stats as (
    select l.inspection_id, lower(trim(l.dba_name)) as dba_name, l.licence_num, l.inspection_dt,results, cnt
    from
        (select inspection_id, dba_name, licence_num, inspection_dt,results,
            row_number() over (partition by dba_name order by inspection_dt desc, inspection_id  desc ) as rn,
            count(inspection_id) over (partition by dba_name) as cnt
            from  raw_inspection) l
    where l.rn =1
)
UPDATE
     Inspection_Stats
SET
     most_recent_license_id = i1.licence_num,
	 most_recent_inspection_id = i1.inspection_id,
	 most_recent_inspection_dt = i1.inspection_dt,
     most_recent_inspection_result = i1.results,
	 num_of_inspections = cnt
FROM
      (select * from stats) i1
where Inspection_Stats.business_name = i1.dba_name ;


with first_inspection_dt as (
    select lower(trim(dba_name)) as dba_name, min(inspection_dt) as first_inspection_dt
    from raw_inspection
    where inspection_dt IS NOT NULL
    group by lower(TRIM(dba_name))
)
UPDATE
      Inspection_Stats
SET first_inspection_dt = f.first_inspection_dt
from first_inspection_dt f
where Inspection_Stats.business_name = f.dba_name;


with pass_cnt as (
	select distinct	zip,
	coalesce(count(distinct dba_name),0) as pass_cnt
	from raw_inspection
	where lower(trim(results)) = 'pass'
	group by zip), total_cnt as (
        select distinct	zip,
        coalesce(count(distinct dba_name),0) as total_cnt
        from raw_inspection
        group by zip ),
        business_zip as(
        select distinct lower(trim(dba_name)) as dba_name, max(zip) as zip
        from raw_inspection
        group by lower(trim(dba_name)))
	UPDATE Inspection_Stats
		SET avg_pass_rate_by_zip_code = round((p.pass_cnt/t.total_cnt::numeric),2)
	from	pass_cnt p
	INNER JOIN total_cnt t ON (p.zip = t.zip)
	INNER JOIN business_zip  b ON (b.zip = t.zip)
	where (b.dba_name = Inspection_Stats.business_name)	;