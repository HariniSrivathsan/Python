CREATE TABLE IF NOT EXISTS raw_license_start(
    id bigint,
    name text,
    address text,
    city text,
    state text,
    start_dt date
);

CREATE TABLE IF NOT EXISTS raw_license_end(
    id bigint,
    name text,
    address text,
    city text,
    state text,
    end_dt date
);

CREATE TABLE IF NOT EXISTS raw_inspection(
    inspection_id bigint,
    dba_name text,
    aka_name text,
    licence_num bigint,
    facility_type varchar(50),
    risk varchar(25),
    address text,
    city varchar(50),
    state char(5),
    zip  varchar(15),
    inspection_dt date,
    inspection_type varchar(50),
    results text,
    latitude decimal(10,5),
    longitude decimal(10,5)
);


