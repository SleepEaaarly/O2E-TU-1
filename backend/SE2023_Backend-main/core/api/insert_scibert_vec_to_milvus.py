import pymysql
from milvus_utils import get_milvus_connection, milvus_insert, disconnect_milvus, milvus_query_paper_by_id, \
    get_milvus_collection
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel


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

    instruction = "update " + entity + " set vector_sci=" + vector + " where id=" + str(id)

    try:
        cursor.execute(instruction)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print("执行MySQL错误")
    result = cursor.fetchall()
    close_database(connection, cursor)
    return result


class ContrastiveSciBERT(nn.Module):
    def __init__(self, out_dim, tau, device='cpu'):
        """⽤于对⽐学习的SciBERT模型
        :param out_dim: int 输出特征维数
        :param tau: float 温度参数τ
        :param device: torch.device, optional 默认为CPU
        """
        super().__init__()
        self.tau = tau
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
        self.model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased').to(device)
        self.linear = nn.Linear(self.model.config.hidden_size, out_dim).to(device)

    def get_embeds(self, texts, max_length=64):
        """将⽂本编码为向量
        :param texts: List[str] 输⼊⽂本列表，⻓度为N


        # Press the green button in the gutter to run the script.
        if __name__ == '__main__':
            print("success")
        :param max_length: int, optional padding最⼤⻓度，默认为64
        :return: tensor(N, d_out)
        """
        encoded = self.tokenizer(
            texts, padding='max_length', truncation=True, max_length=max_length, return_tensors='pt'
        ).to(self.device)
        return self.linear(self.model(**encoded).pooler_output)

    def calc_sim(self, texts_a, texts_b):
        """计算两组⽂本的相似度
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N) 相似度矩阵，S[i, j] = cos(a[i], b[j]) / τ
        """
        embeds_a = self.get_embeds(texts_a)  # (N, d_out)
        embeds_b = self.get_embeds(texts_b)  # (N, d_out)
        embeds_a = embeds_a / embeds_a.norm(dim=1, keepdim=True)
        embeds_b = embeds_b / embeds_b.norm(dim=1, keepdim=True)
        return embeds_a @ embeds_b.t() / self.tau

    def forward(self, texts_a, texts_b):
        """计算两组⽂本的对⽐损失（直接返回损失）
        :param texts_a: List[str] 输⼊⽂本A列表，⻓度为N
        :param texts_b: List[str] 输⼊⽂本B列表，⻓度为N
        :return: tensor(N, N), float A对B的相似度矩阵，对⽐损失
        """
        # logits_ab等价于预测概率，对⽐损失等价于交叉熵损失
        logits_ab = self.calc_sim(texts_a, texts_b)
        logits_ba = logits_ab.t()
        labels = torch.arange(len(texts_a), device=self.device)
        loss_ab = F.cross_entropy(logits_ab, labels)
        loss_ba = F.cross_entropy(logits_ba, labels)
        loss = (loss_ab + loss_ba) / 2
        return loss


d_name = "core_results"
c_name = "O2E_RESULT"
rst = get_all_entity(d_name)
inp = [[r[1], r[0], r[9]] for r in rst]
# print(pap_titles)
state_dict = torch.load("D:\\大学学习\\大三下\\软件工程\\O2E-TU-1\\backend\\SE2023_Backend-main\\model.pt", map_location='cpu')
model = ContrastiveSciBERT(out_dim=128, tau=0.07)
model.load_state_dict(state_dict)
get_milvus_connection()
for i in inp:
    if i[2] == 1:
        get_milvus_connection()
        vector = model.get_embeds(i[0])
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