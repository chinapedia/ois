import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence, pad_sequence
from torchcrf import CRF
import torch
from torch.utils.data import Dataset
from preprocess import load_obj


class BiLSTM_CRF(nn.Module):
    """
        vocab_size: 单词表大小
        num_tags: 总标签数量
        embed_dim: 词向量
        hidden_dim: lstm隐层
    """

    def __init__(self, vocab_size, num_tags, embed_dim, hidden_dim, dropout):
        super(BiLSTM_CRF, self).__init__()
        self.vocab_size = vocab_size
        self.num_tags = num_tags
        # Layers
        self.dropout = nn.Dropout(dropout)
        self.embeds = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim // 2, bidirectional=True)
        self.hidden_to_tag = nn.Linear(hidden_dim, num_tags)
        self.crf = CRF(num_tags)

    def get_emissions(self, seqs, masks):
        # 获取bilstm的输出
        embeds = self.embeds(seqs)  # (seq_len, batch_size, embed_dim)
        embeds = self.dropout(embeds)
        packed = pack_padded_sequence(embeds, masks.sum(0))
        lstm_out, u = self.lstm(packed)
        lstm_out, u = pad_packed_sequence(lstm_out)  # (seq_len, batch_size, hidden_dim)

        emissions = self.hidden_to_tag(lstm_out)
        return emissions

    def loss(self, seqs, tags, masks):
        # 通过crf计算损失函数
        emissions = self.get_emissions(seqs, masks)
        loss = -self.crf(emissions, tags, mask=masks, reduction="mean")
        return loss

    def decode(self, seqs, masks):
        # lstm + crf 解码
        emissions = self.get_emissions(seqs, masks)
        best_tags = self.crf.decode(emissions, mask=masks)
        return best_tags


class NERDataset(Dataset):

    def __init__(self, dataset_pkl):
        super(NERDataset, self).__init__()
        self.dataset = load_obj(dataset_pkl)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        return (
            torch.tensor(self.dataset[idx][0], dtype=torch.long),
            torch.tensor(self.dataset[idx][1], dtype=torch.long),
        )


class BatchPadding(object):
    # 填充并按照填充长度排序

    def __init__(self, descending=True):
        self.reverse = True if descending else False

    def __call__(self, batch):
        sorted_batch = sorted(batch, key=lambda x: len(x[0]), reverse=self.reverse)
        seqs, tags = tuple(zip(*sorted_batch))
        seqs = pad_sequence(seqs)  # 0 padding
        tags = pad_sequence(tags)
        masks = seqs.ne(0)
        return seqs, tags, masks
