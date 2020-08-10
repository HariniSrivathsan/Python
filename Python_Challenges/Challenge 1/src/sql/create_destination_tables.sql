CREATE TABLE IF NOT EXISTS license(
    license_id       bigint NOT NULL,
    business_name    text NOT NULL,
    address          text NOT NULL,
    city             varchar(25) NOT NULL,
    state            char(5) NOT NULL,
    start_dt         DATE,
    end_dt           DATE
 );


 CREATE TABLE IF NOT EXISTS Inspection_Stats(
    business_name  text PRIMARY KEY,
    most_recent_license_id bigint,
    most_recent_inspection_id bigint,
    first_inspection_dt date,
    most_recent_inspection_dt date,
    most_recent_inspection_result varchar(30),
    num_of_inspections int,
    avg_pass_rate_by_zip_code decimal(5,2)
 );


