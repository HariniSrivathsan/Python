import psycopg2
import logging
from psycopg2 import OperationalError, errorcodes, errors


logger = logging.getLogger("Civis - Making dataset.")


class MakeDataset:
    def __init__(self, config=None):
        self.config = config

    def get_db_conn_hdl(self):
        """
        Get postgres DB connection handle.
        :return:
        """
        logger.info(f'Creating the DB connection string.')
        myhost = self.config.get('postgres', 'host')
        myport = self.config.getint('postgres', 'port')
        mydbname = self.config.get('postgres', 'dbname')
        myuser = self.config.get('postgres', 'user')
        passwd = self.config.get('postgres', 'pwd')

        conn_str = "host=" + myhost + " port=" + str(myport) + " dbname=" + mydbname + " user=" + myuser + " password=" + passwd

        logger.info(f'Getting the connection handle using psycopg2')
        try:
            db_conn = psycopg2.connect(conn_str)
        except psycopg2.Error as e:
            logger.info("Error: Could not make connection to the Postgres database")
            print(e)
        else:
            db_conn.set_session(autocommit=True)
            logger.info('Got connection handle and set to autocommit')
            return db_conn

    def run_sql(self, sql_file, task_name):
        logger.info(f'\n\nExecuting {sql_file}')
        try:
            db_conn = self.get_db_conn_hdl()
        except:
            logger.info(f'Unable to get a connection handle')
        else:
            try:
                logger.info(f'Running task: {task_name}')
                with db_conn.cursor() as cursor:
                    try:
                        cursor.execute(open(sql_file, "r").read())
                    except:
                        logger.error(f'Some error in executing {sql_file}')
                        db_conn.close()
                        logger.info(f'********{task_name} failed *********')
                    else:
                        logger.info(f'{task_name} successful')
            finally:
                db_conn.close()







