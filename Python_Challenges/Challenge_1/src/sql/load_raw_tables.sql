SET datestyle = MDY;
COPY raw_license_start FROM '/home/srivathsan/PycharmProjects/civis/input/license_start.csv' DELIMITERS ',' CSV header;
COPY raw_license_end FROM '/home/srivathsan/PycharmProjects/civis/input/license_end.csv' DELIMITERS ',' CSV header;
COPY raw_inspection FROM '/home/srivathsan/PycharmProjects/civis/processed/cleansed_inspections.csv' DELIMITERS ',' CSV header;


