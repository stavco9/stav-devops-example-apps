import psycopg2
import json
import os
import config
from modules.aws_conn import AWSConn
from modules.logger import Logger

class DBConn():
    def __init__(self, rds_conn_aws_secret):
        self.aws_client = AWSConn(region=config.DB_SECRET_REGION)
        self.logger = Logger()
        secret_val = self.aws_client.get_secret_value(rds_conn_aws_secret)

        if not secret_val:
            raise Exception("Cannot initalize DB connection because the aws secret cannot be accessed")

        self.db_conn_details = json.loads(secret_val)

        self.db_conn = psycopg2.connect(
            host=self.db_conn_details['host'], 
            database=self.db_conn_details['dbname'], 
            port=self.db_conn_details['port'],
            user=self.db_conn_details['username'],
            password=self.db_conn_details['password'])
        self.db_conn.set_client_encoding('utf8')
        self.crs = self.db_conn.cursor()

    def __del__(self):
        if hasattr(self, 'db_conn'):
            self.crs.close()
            self.db_conn.close()

    def run_execution(self, execute_command):
        try:
            self.crs.execute(execute_command, [])
            self.db_conn.commit()

            return True
        except Exception as e:
            self.logger.error("Error during executing command {}".format(execute_command))
            self.logger.error(e)
            return False

    def run_proc(self, schema_name, function_name, *function_params):
        func_run_string = str("call {}.{}('{}');").format(schema_name, function_name, ", ".join(function_params)).replace("''", "")

        if self.run_execution(func_run_string):
            self.logger.info(str("Procedure {} is schema {} executed successfully").format(schema_name, function_name))
        else:
            self.logger.error("Error during running sql procedure: {}".format(function_name))
            return False
        return True
    
    def run_func(self, schema_name, function_name, *function_params):
        func_run_string = str("select {}.{}('{}');").format(schema_name, function_name, ", ".join(function_params)).replace("''", "")
        
        if self.run_execution(func_run_string):
            self.logger.info(str("Function {} is schema {} executed successfully").format(schema_name, function_name))
        else:
            self.logger.error("Error during running sql function: {}".format(function_name))
            return False
        return True

    def run_select(self, schema_name, table_name, fields_to_select: list, filter_row: str = None):
        select_string = ""
        records = []
        for field in fields_to_select:
            select_string += "{}, ".format(field)
        select_string = select_string[:-2]

        update_select_string = str("select {} from {}.{}").format(select_string, schema_name, table_name)
        
        if filter_row:
            update_select_string += "where {}".format(filter_row)

        self.logger.info("Running {}".format(update_select_string))
        if self.run_execution(update_select_string):
            records = self.crs.fetchall()
        else:
            self.logger.error("Error during running sql query")
            return None
        return records

    def run_update(self, schema_name, table_name, fields_to_update: dict, filter_row: str = None):
        set_string = ""
        for k, v in fields_to_update.items():
            set_string += "{}='{}', ".format(k, v)
        set_string = set_string[:-2]

        update_run_string = str("update {}.{} set {}").format(schema_name, table_name, set_string)
        
        if filter_row:
            update_run_string += "where {}".format(filter_row)

        self.logger.info("Running {}".format(update_run_string))
        if self.run_execution(update_run_string):
            self.logger.info("Update query has been run successfully")
        else:
            self.logger.error("Error during running sql query")
            return False
        return True