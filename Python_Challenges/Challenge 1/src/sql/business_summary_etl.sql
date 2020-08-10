INSERT INTO business_summary(business_name)
select distinct dba_name
   from raw_inspection;