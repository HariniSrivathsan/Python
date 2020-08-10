import logging
import logging.config
import configparser
import time
import os
import sys
import ast
import pandas as pd

from eda import EDA
import sweetviz as sv
from preprocess import PreProcess
from make_dataset import MakeDataset


logger = logging.getLogger("Civis Project Main")


def run_eda(config):
    """ Do some exploratory data analysis for all input files"""
    logger.info(f'Doing Exploratory Data Analysis...')
    raw_inspections_file = config.get('input', 'raw_inspections_file')
    raw_license_start_file = config.get('input', 'raw_license_start_file')
    raw_license_end_file = config.get('input', 'raw_license_end_file')
    infiles = [raw_inspections_file, raw_license_start_file, raw_license_end_file]
    for infile in infiles:
        name = os.path.basename(infile)
        name = name.split('.')[0]
        df = pd.read_csv(infile)
        eda_obj = EDA(data_df=df, config=config, filename=name)
        eda_obj.find_total_nulls_in_columns(name=name)
        eda_obj.missing_data(name=name)
        eda_obj.gen_profile_report(name=name)

def cleanse_inspections_data(config):
    """ Cleanse some stuff in inspections data """
    raw_inspections_file = config.get('input', 'raw_inspections_file')
    logger.info(f'Standardizing 7-Eleven business name...')
    df = pd.read_csv(raw_inspections_file)
    pp_obj = PreProcess(data_df=df, config=config)
    pp_obj.get_potential_messy_business_names()
    df = pp_obj.cleanse_7elevens()
    cleansed_file = config.get('processed', 'cleansed_inspections_file')
    df.to_csv(cleansed_file, index=False)
    logger.info(f'Stored the standardized inspections file: {cleansed_file}')

def main():
    prg_start_time = time.time()
    logging.config.fileConfig('config.properties', disable_existing_loggers=False)
    config = configparser.ConfigParser()
    config.read('config.properties')

    # ---------  Exploratory Data Analysis -----------------
    # Uncomment below line to run EDA. I have already done it.
    # run_eda(config)

    # standardize business names in inspections file.
    # Uncomment below line to cleanse inspections data. I have already done it.
    # cleanse_inspections_data(config)

    #------------------------------- Create tables, load and process -----------------

    sql_files = config.get('input', 'sql_tuples')
    sql_files = ast.literal_eval(sql_files)
    logger.info('Creating Dataset in local Postgres...')
    mkd_obj = MakeDataset(config)

    for sql_tuple in sql_files:
        sql_start_time = time.time()
        sql_file = sql_tuple[0]
        task_name = sql_tuple[1]
        mkd_obj.run_sql(sql_file, task_name)
        sql_end_time = time.time()
        execution_time = (sql_end_time - sql_start_time) / 3600
        logger.info(f'Time taken for executing {task_name}: {execution_time} hours.')


    prg_end_time = time.time()
    execution_time = (prg_end_time - prg_start_time) / 3600
    print("\n")
    logger.info(f'Time taken for ETL for loading  table: {execution_time} hours.')


if __name__ == '__main__':
    main()