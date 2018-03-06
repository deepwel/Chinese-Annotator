from chi_annotator.task_center.common import DBManager


class TestDatabase(object):
    """
    test database apis
    """

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        db.drop_database()
        db.close()

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        db.drop_database()
        db.close()

    def ignor_test_insert_one(self):
        """
        test insert one item into database
        :return:
        """

        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        flag = db.insert_row({"uuid": 12, "text": "我是测试", "label": "spam"})
        assert flag is True
        db.drop_database()
        db.close()

    def ignor_test_update(self):
        """
        test batch update
        :return:
        """
        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        db.insert_row({"uuid": 1, "text": "我是测试", "label": "spam"})
        flag = db.update_rows({"uuid": 1}, {"label": "notspam"})
        assert flag is True
        db.drop_database()
        db.close()

    def ignor_test_get_rows(self):
        """
        test get rows
        :return:
        """
        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        db.insert_row({"uuid": 1, "text": "我是测试", "label": "spam"})
        db.insert_row({"uuid": 2, "text": "我是测试2", "label": "notspam"})
        db.insert_row({"uuid": 3, "text": "我是测试", "label": "spam"})

        res = db.get_rows({"label": "spam"})
        assert len(res) == 2
        db.drop_database()
        db.close()

    def ignor_test_get_rows_by_ids(self):
        """
        test get rows
        :return:
        """
        db = DBManager(config={"database_name": "test_dataset", "table_name": "test_table"})
        db.insert_row({"uuid": 1, "text": "我是测试", "label": "spam"})
        db.insert_row({"uuid": 2, "text": "我是测试2", "label": "notspam"})
        db.insert_row({"uuid": 3, "text": "我是测试", "label": "spam"})

        res = db.get_row_by_ids([1, 2])
        assert len(res) == 2
        db.drop_database()
        db.close()
