from pymongo import MongoClient


class DBManager(object):
    """
    manage database connections, TODO, if ORM needed?
    """

    def __init__(self, config):
        self.hostname = config.get("database_hostname", "localhost")
        self.port = config.get("database_port", 27017)
        self.type = config.get("database_type", "mongodb")
        self.database = config.get("database_name", "chinese_annotator")
        self.table = config.get("table_name", "corpus")

        # TODO for test, this config param will be remove later.
        self.active = config.get("database_active", True)

        if self.type == "mongodb" and self.active:
            self.client = MongoClient(self.hostname, self.port)
        else:
            # TODO some other database type in future.
            # self.client = other interface
            pass

    def insert_row(self, item, database_name=None, table=None):
        """
        insert one row into database
        :param item: json format data
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            if self.client[database_name][table].find_one(item) is None:
                xid = self.client[database_name][table].insert_one(item).inserted_id
                return True
        # TODO catch exception
        return False

    def insert_rows(self, item, database_name=None, table=None):
        """
        insert one row into database
        :param item: list of json format data
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            xids = self.client[database_name][table].insert(item).inserted_id
            return True
        # TODO catch exception
        return False

    def update_rows(self, condition, new_value, database_name=None, table=None):
        """
        insert one row into database
        :param new_value:
        :param condition:
        :param database_name:
        :param table:
        :return: row_num or row id
        """
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            xids = self.client[database_name][table].update_many(condition, {"$set": new_value})
            if xids.matched_count > 0:
                return True
        return False

    def get_rows(self, conditions, database_name=None, table=None):
        """
        get rows according conditions
        :param table:
        :param database_name:
        :param conditions: json format data
        :return:
        """
        res = []
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            result = self.client[database_name][table].find(conditions)
            for item in result:
                res.append(item)
        return res

    def get_row_by_ids(self, ids, col_name="uuid", database_name=None, table=None):
        """
        get rows according conditions
        :param col_name:
        :param table:
        :param database_name:
        :param conditions: json format data
        :return:
        """
        res = []
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            result = self.client[database_name][table].find({col_name: {"$in": ids}})
            for item in result:
                res.append(item)
        return res

    def get_row(self, condition, database_name=None, table=None):
        """
        get row according conditions
        :param table:
        :param database_name:
        :param conditions: json format data
        :return:
        """
        if database_name is None:
            database_name = self.database
        if table is None:
            table = self.table

        if self.type == "mongodb":
            result = self.client[database_name][table].find_one(condition)
            return result
        return None

    def close(self):
        """
        close connection from database
        :return:
        """
        if self.type == "mongodb":
            self.client.close()

    def drop_database(self, database=None):
        """
        drop dataset for test now.
        :param database:
        :return:
        """
        if database is None:
            database = self.database
        if self.type == "mongodb":
            self.client.drop_database(database)
