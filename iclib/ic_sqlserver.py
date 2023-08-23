# coding: utf-8
import platform
import pyodbc
from contextlib import contextmanager


def parse_connection_string(str_cnn):
    res = dict()
    split_dt = str_cnn.split(";")
    for c_sp in split_dt:
        k, v = c_sp.split("=")
        res[k.strip()] = v.replace("'", "").replace('"', '')
    return res


class DatabaseIO(object):

    def __init__(self, server=None, port=None, user=None, password=None, database=None, driver=None, conn_str=None):
        if conn_str:
            dict_conn = parse_connection_string(conn_str)
            self.server, self.port = dict_conn["Server"].split(",")
            self.port = int(self.port)
            self.user = dict_conn["User Id"]
            self.password = dict_conn["Password"]
            self.database = dict_conn["Database"]
        else:
            self.server = server
            self.port = port
            self.user = user
            self.password = password
            self.database = database
        if driver is None:
            system = platform.system()
            self.driver = "{FreeTDS}"
            if system == 'Linux':
                self.driver = "{ODBC Driver 17 for SQL Server}"
                # xem ở /etc/odbcinst.ini
            elif system == 'Windows':
                self.driver = "{SQL Server}"
                # xem ở Control Panel > Administrator Tools > Data Source > Drivers
            else:
                self.driver = None
        else:
            self.driver = driver
        self.conn_str = 'DRIVER={0};SERVER={1};PORT={2};DATABASE={3};UID={4};PWD={5}'.format(str(self.driver),
                                                                                             str(self.server),
                                                                                             str(self.port),
                                                                                             str(self.database),
                                                                                             str(self.user),
                                                                                             str(self.password))

    @contextmanager
    def connect_database(self):
        """
        Kết nối với DB, hàm sẽ tự động đóng kết nối và commit dữ liệu khi kết thúc.
        Sử dụng theo mẫu
            with connect_database() as conn:
                with conn.cursor() as cursor:
                    try:
                        cursor.execute(SQL_QUERY, ...)
                    except:
                        ...
        :return: trả về generator
        """
        cnxn = None
        try:
            cnxn = pyodbc.connect(self.conn_str, unicode_results=True)
            yield cnxn
        finally:
            if cnxn:
                cnxn.close()

    def connect_database_keep(self):
        try:
            cnxn = pyodbc.connect(self.conn_str, unicode_results=True, autocommit=True)
        except Exception as ve:
            raise ve
        return cnxn

    def query_db(self, sql_query, *args):
        with self.connect_database() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql_query, *args)
                except pyodbc.DataError as de:
                    raise de
                else:
                    # for rec in cursor:
                    #     yield rec
                    results = cursor.fetchall()
                    for rec in results:
                        yield rec

    def query_insert_db(self, sql_query, *args):
        with self.connect_database() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql_query, *args)
                except Exception as ve:
                    raise ve

    @staticmethod
    def query_insert_db_keep_connect(conn, sql_query, *args):
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_query, *args)
            except Exception as ve:
                raise ve

    @staticmethod
    def query_db_keep_connect(conn, sql_query, *args):
        with conn.cursor() as cursor:
            try:
                cursor.execute(sql_query, *args)
            except pyodbc.DataError as de:
                raise de
            else:
                for rec in cursor:
                    yield rec


if __name__ == "__main__":
    server_, port_, user_, password_, database_, driver_ = None, None, None, None, None, None
    dbio = DatabaseIO(server_, port_, user_, password_, database_, driver_)
    records = dbio.query_db("""SELECT count(*) as value 
                           FROM [autotag].[dbo].[autotag_face] with (nolock)""")
    for record in records:
        print(record)
