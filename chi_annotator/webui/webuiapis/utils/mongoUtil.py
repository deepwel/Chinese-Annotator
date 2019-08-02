# encoding:utf-8
import sys

# from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

'''
    Author: Gupern 周起超
    CreateTime: 2017-05-16
    Description: This is a file for easy manipulate the MongoDB

    LastModified:
        2017-05-24 : change class to func, for easily use
        2017-05-17 : add note params and return
    FunctionNote:
        renameField(col, _id, oldField, newField): 重命名field
        removeDocById(col, _id): 通过Id移除doc
        findOneById(col, _id): 通过id查找doc
        clientInsurance(func): 装饰器，用于保证client关闭
        cloneField(col, _id, key1, kye2): 克隆key1，到key2，成功返回1，失败返回0
        closeClient(client): 返回None
        insertOneDocument(col, document): 返回inserted_id
        updateOneField: col、_id、key和value，返回1（成功）或者0（失败）,'_id type error'（如果传入的参数有问题）
        getClient: 接收url，port，username和password，若无则设置为默认参数，返回client
        getCol：接收client，db和col，返回col
'''


def get_mongo_client(uri="mongodb://0.0.0.0:27017/", db="ca"):
    """
    Connect to MongoDB
    """
    try:
        # c = MongoClient("mongodb://upenergy:upenergy@db0.silknets.com:27000/sso")
        # uri = u"mongodb://mongo:mongo@127.0.0.1/sso?authMechanism=SCRAM-SHA-1"
        c = MongoClient(uri)

    except ConnectionFailure as e:
        sys.stderr.write("Could not connect to MongoDB: %s" % e)
        sys.exit(1)

    # Get a Database handle to a database named "mydb"
    dbh = c[db]
    print('connected succeed.')
    print(('URI: ' + uri + '  Database: ' + db))
    return dbh


# if __name__ == '__main__':
#     client = fastGetClient('aliWriter')
#     col = get_col(client, 'silkweb-production', 'guide')
#     result = removeDocById(col, '58537075f1d300535160d0e6')
#     print(result)
