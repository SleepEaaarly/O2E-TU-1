from pymilvus import connections, drop_collection
from pymilvus import CollectionSchema, FieldSchema, DataType, Collection

_HOST = '116.63.14.146'
# _HOST = '101.200.191.47'
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


def create_milvus_collection(db_id_name, collection_name, vec_dim):
    """
    新建Milvus集合
    """
    get_milvus_connection()
    milvus_id = FieldSchema(
        name="milvus_id",
        dtype=DataType.INT64,
        is_primary=True,
        auto_id=True
    )
    vector = FieldSchema(
        name="vector",
        dtype=DataType.FLOAT_VECTOR, dim=vec_dim
    )
    db_id = FieldSchema(
        name=db_id_name,
        dtype=DataType.INT64
    )
    schema = CollectionSchema(
        fields=[milvus_id, vector, db_id],
    )
    collection = Collection(
        name=collection_name,
        schema=schema,
        using='default',
        # shards_num=2,
        # consistency_level="Strong"
    )


def del_milvus_collection(name):
    """
    删除指定collection
    """
    drop_collection(name)


def get_milvus_collection(name):
    """
    获取指定collection
    """
    collection = Collection(name)
    return collection


def discribe_milvus_collection(name):
    """
    展示collection信息
    """
    collection = Collection(name)
    # collection.load(verbose=True)

    # 获取集合属性并访问 'num_entities' 属性
    desc = collection.describe()
    # print(desc)
    num_entities = collection.num_entities

    print(f'集合 {name} 中有 {num_entities} 个向量')


def milvus_insert(collection_name, data, partition_name=None):
    """
    插⼊数据。
    :param collection_name: collection名称
    :param partition_name: partition名称
    :param data: 待插⼊的数据，list-like(list, tuple)
    :return: Milvus⽣成的ids
    """
    collection = get_milvus_collection(collection_name)
    print('milvus_insert 1')
    print(data)
    try:
        res = collection.insert(partition_name=partition_name, data=data)
    except Exception as e:
        print(e)
    print('milvus_insert 2')
    ids = res.primary_keys # 这个id是由Milvus⽣成的，⼤家注意要和论⽂id对应起来保存
    print('milvus_insert 3')
    
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
    根据id（scibert）获取成果ID
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


def milvus_query_expert_by_id(query):
    """
    根据id获取专家ID
    """
    collection = Collection("O2E_EXPERT")
    res = collection.query(
        expr=query,
        output_fields=["expert_id"],
        consistency_level="Strong"
    )
    return res


def milvus_query_enterprise_by_id(query):
    """
    根据id获取企业ID
    """
    collection = Collection("O2E_ENTERPRISE")
    res = collection.query(
        expr=query,
        output_fields=["enterprise_id"],
        consistency_level="Strong"
    )
    return res


def milvus_query_result_hit_by_id(query):
    """
    根据id（hitbert）获取成果ID
    """
    collection = Collection("O2E_RESULT_HIT")
    res = collection.query(
        expr=query,
        output_fields=["result_id"],
        consistency_level="Strong"
    )
    return res


if __name__ == '__main__':
    from pymilvus import drop_collection, list_collections
    get_milvus_connection()
    names = list_collections()
    print(names)
    for name in names:
        print()
        discribe_milvus_collection(name)
    disconnect_milvus()
