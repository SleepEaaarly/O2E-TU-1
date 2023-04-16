from pymilvus import connections
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection

_HOST = '116.63.14.146'
_PORT = '19530'


def get_milvus_connection():
    """
    建⽴Milvus连接
    """
    connections.connect(
        alias="default", host=_HOST, port=_PORT
    )


def disconnect_milvus():
    connections.disconnect("default")


def create_milvus_collection():
    """
    建⽴Milvus连接
    """
    milvus_id = FieldSchema(
        name="milvus_id",
        dtype=DataType.INT64,
        is_primary=True,
        auto_id=True
    )
    paper_vector = FieldSchema(
        name="vector",
        dtype=DataType.FLOAT_VECTOR, dim=128
    )
    schema = CollectionSchema(
        fields=[milvus_id, paper_vector],
        description="O2E_TEMP"
    )
    collection_name = "O2E_TEMP"
    collection = Collection(
        name=collection_name,
        schema=schema,
        using='default',
        # shards_num=2,
        # consistency_level="Strong"
    )


def get_milvus_collection(name):
    """
    获取指定collection
    """
    collection = Collection(name)
    return collection


def milvus_insert(collection_name, data, partition_name=None):
    """
    插⼊数据。
    :param collection_name: collection名称
    :param partition_name: partition名称
    :param data: 待插⼊的数据，list-like(list, tuple)
    :return: Milvus⽣成的ids
    """
    collection = get_milvus_collection(collection_name)
    res = collection.insert(partition_name=partition_name, data=data)
    ids = res.primary_keys # 这个id是由Milvus⽣成的，⼤家注意要和论⽂id对应起来保存
    return ids


def milvus_search(collection_name, partition_names, query_vectors, topk, eps=0, expr=None):
    """
    查询相关向量。
    :param collection_name: collection名称
    :param partition_names: partition名称列表
    :param query_vectors: 待查询的数据，list-like(list, tuple)
    :param topk: 每个query返回的最相似个数
    :param eps: 
    :param expr: 条件表达式
    :return: ids_list, (list,list)
    """
    collection = get_milvus_collection(collection_name)
    res = collection.search(
        partition_names=partition_names,
        data=query_vectors,
        anns_field="vector",
        limit=topk,
        expr=expr,
        param={"metric_type": "L2", "params": {"nprobe": 10, "eps": eps}}
    )
    ids_list=[]
    for item in res:
        ids = []
        for p in item:
            ids.append(p.id)
        ids_list.append(ids)
    return ids_list


def milvus_get_by_id(collection_name, id):
    """
    根据id获取数据
    """
    collection = get_milvus_collection(collection_name)
    res = collection.query("milvus_id == {}".format(id))
    for item in res:
        print(item)


def milvus_query_paper_by_id(query):
    """
    根据id获取论文知兔ID
    """
    collection = Collection("O2E_PAPER")
    res = collection.query(
        expr=query,
        output_fields=["paper_id"],
        consistency_level="Strong"
    )
    return res


def milvus_query_need_by_id(query):
    """
    根据id获取需求ID
    """
    collection = Collection("O2E_NEED")
    res = collection.query(
        expr=query,
        output_fields=["need_id"],
        consistency_level="Strong"
    )
    return res


def milvus_query_result_by_id(query):
    """
    根据id获取成果ID
    """
    collection = Collection("O2E_RESULT")
    res = collection.query(
        expr=query,
        output_fields=["result_id"],
        consistency_level="Strong"
    )
    return res


def milvus_query_set_question_by_id(query):
    """
    根据id获取预设问题ID
    """
    collection = Collection("SET_QUESTION")
    res = collection.query(
        expr=query,
        output_fields=["question_id"],
        consistency_level="Strong"
    )
    return res

