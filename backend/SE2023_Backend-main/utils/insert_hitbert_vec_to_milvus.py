from sql_util import get_all_entity, update_sci_vector, update_hit_vector
from core.api.milvus_utils import get_milvus_connection, milvus_insert, disconnect_milvus, milvus_query_paper_by_id, \
    get_milvus_collection
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as ny
from transformers import AutoTokenizer, AutoModel, BertTokenizer, BertModel


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


d_name = "core_results"    # 换成专家、企业的表
c_name = "O2E_RESULT_HIT"
rst = get_all_entity(d_name)
inp = [[r[1], r[0], r[9]] for r in rst]
# print(pap_titles)
hit = HitBert(hitModelPath="D:\\大学学习\\大三下\\软件工程\\O2E-TU-1\\backend\\SE2023_Backend-main\\resource\\bert", device="cpu")
for i in inp:
    if i[2] == 1:
        get_milvus_connection()
        vector = hit.encode_2_list(i[0])    # 可能不对，检查一下
        # vector = vector / vector.norm(dim=1, keepdim=True)
        # v = vector.tolist()[0]
        mid = milvus_insert(c_name, data=[[vector], [i[1]]])
        disconnect_milvus()
        update_hit_vector(d_name, str(mid[0]), i[1])

