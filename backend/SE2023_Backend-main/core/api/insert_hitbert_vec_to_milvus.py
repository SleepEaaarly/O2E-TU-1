import pymysql
from milvus_utils import get_milvus_connection, milvus_insert, disconnect_milvus, milvus_query_paper_by_id, \
    get_milvus_collection
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as ny
from transformers import AutoTokenizer, AutoModel, BertTokenizer, BertModel


def connect_database():
    connection = pymysql.connect(host="116.63.14.146",
                                 port=3306,
                                 db="se2023",
                                 user="root",
                                 passwd="O2E-TH-1!",
                                 charset="utf8")
    cursor = connection.cursor()
    return connection, cursor


def close_database(connection, cursor):
    connection.close()
    cursor.close()


def get_all_entity(entity: str):
    connection, cursor = connect_database()

    instruction = "select * from " + entity

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result


def update_vector(entity: str, vector: str, id: int):
    connection, cursor = connect_database()

    instruction = "update " + entity + " set vector=" + vector + " where id=" + str(id)

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result


class HitBert:
    def __init__(self, hitModelPath, device):
        self.hit_tokenizer = BertTokenizer.from_pretrained(hitModelPath)
        self.hit_model = BertModel.from_pretrained(hitModelPath)
        self.device = device
        self.hit_model.to(device)
        self.hit_model.eval()

    def encode(self, sent):
        encode_tensors = self.hit_tokenizer.encode_plus(sent, add_special_tokens=True, return_tensors='pt',
                                                        max_length=None)
        input_ids = encode_tensors['input_ids']
        lengths = torch.from_numpy(ny.array([input_ids.shape[1] for _ in range(input_ids.shape[0])])).float()
        # padding_mask = get_padding_mask(lengths)  # transformers==2.3.0
        padding_mask = encode_tensors['attention_mask']  # transformers>3.0
        with torch.no_grad():
            outputs = self.hit_model(input_ids.to(self.device), attention_mask=padding_mask.to(self.device))[0]
            outputs.masked_fill_(padding_mask[:, :, None].to(self.device) == 0, 0)
            outputs = outputs[:, 1:-1, :].sum(dim=1).to(self.device) / (lengths[:, None] - 2).to(self.device)
        # return outputs[0].cpu().numpy().tolist()
        return outputs

    def encode_2_list(self, sent):
        return self.encode(sent)[0].cpu().numpy().tolist()


d_name = "core_need"    # 换成专家、企业的表
c_name = "O2E_NEED"
rst = get_all_entity(d_name)
inp = [[r[1], r[0]] for r in rst]
# print(pap_titles)
hit = HitBert(hitModelPath="E:\\lcm\\Course\\软件工程\\代码\\O2E-TU-1\\backend\\SE2023_Backend-main\\resource\\bert", device="cpu")
get_milvus_connection()
for i in inp:
    get_milvus_connection()
    vector = hit.encode_2_list(i[0])    # 可能不对，检查一下
    # vector = vector / vector.norm(dim=1, keepdim=True)
    v = vector.tolist()[0]
    mid = milvus_insert(c_name, data=[[v], [i[1]]])
    disconnect_milvus()
    update_vector(d_name, str(mid[0]), i[1])

# m = ContrastiveSciBERT(128, 25.0)
# key_vector = m.get_embeds(pap_titles)




'''
get_milvus_connection()

print(list(rst[0:2]))
m_id = milvus_insert("O2E_PAPER", list(rst[0:2]))
print(m_id)
'''