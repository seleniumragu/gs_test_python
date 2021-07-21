# -*- coding: utf-8 -*-
__author__ = 'wenjing.liu'

import pymssql
from pymssql import DatabaseError
from utils.logger import logger


class SqlDatabaseManager(object):
    def __init__(self, host, user, pwd, database):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.database = database
        self.conn = None

    def connect_database(self):
        try:
            self.conn = pymssql.connect(self.host, self.user,
                                        self.pwd, self.database,timeout=60*2, login_timeout=60)
            logger.info("Connect database %s successfully." % self.host)
        except Exception as e:
            logger.error("Connect database %s fail." % self.host)
            print("database connection fail:")
            print(e)

    def close_database(self):
        if self.conn:
            try:
                self.conn.close()
                logger.info("Close database %s successfully." % self.host)
            except DatabaseError :
                logger.error("Close database %s fail." % self.host)
                raise DatabaseError(
                     "Close database %s fail." % self.host
                )

    def execute_select_sql(self, sql):
        """
        execute select sql
        :param sql: sql query
        :return: query result
        """
        try:
            cur = self.conn.cursor()
            # Lock().acquire()
            cur.execute(sql)
            result = cur.fetchall()
            # Lock().release()
        except Exception:
            logger.info("execute sql fail: ")

            raise Exception(
                "Execute sql: {sql} fail.".format(sql=sql)
            )
        return result

    def execute_select_sql_dic(self, sql):
        """
        execute select sql
        :param sql: sql query
        :return: query result as dictionary
        """
        try:
            cur = self.conn.cursor(as_dict=True)
            # Lock().acquire()
            cur.execute(sql)
            result = []
            for row in cur:
                result.append(row)
            # Lock().release()
        except Exception:
            logger.info("execute sql fail: ")

            raise Exception(
                "Execute sql: {sql} fail.".format(sql=sql)
            )
        return result

    def execute_update_sql(self, sql):
        """
        execute sql to insert,update,delete
        :param sql: sql query
        :return: query result
        """
        try:
            cur = self.conn.cursor()
            # Lock().acquire()
            cur.execute(sql)
            self.conn.commit()
            result = cur.fetchall()
            # Lock().release()
        except Exception as error:
            self.conn.rollback()
            logger.error("execute sql fail: " + error)
            raise Exception(
                "Execute sql: {sql} fail.".format(sql=sql)
            )
        return result





