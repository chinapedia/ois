import argparse
import os
import torch
from utils import UNK, TEST_SENTENCE, CUR_MODEL
from model import BiLSTM_CRF
from preprocess import load_obj


def get_tag(model, sentence, idx_to_tag):
    sentence = sentence.unsqueeze(1)
    mask = sentence.ne(0)
    best_tag_ids = model.decode(sentence, mask)
    tags = [idx_to_tag[idx] for idx in best_tag_ids[0]]
    return tags


if __name__ == '__main__':
    print(TEST_SENTENCE)
    data_dir = 'data/chinese/processed'
    word_to_idx = load_obj(os.path.join(data_dir, 'word_to_idx.pkl'))
    tag_to_idx = load_obj(os.path.join(data_dir, 'tag_to_idx.pkl'))

    idx_to_tag = {v: k for k, v in tag_to_idx.items()}

    model = BiLSTM_CRF(len(word_to_idx), len(tag_to_idx), 100, 200, 0.1)
    model.load_state_dict(torch.load(CUR_MODEL, map_location=torch.device('cuda')))
    model.eval()

    processed_sen = [i.split('/')[0] for i in TEST_SENTENCE.split()]
    sentence = torch.LongTensor(
        [word_to_idx.get(w, word_to_idx[UNK]) for w in processed_sen]
    )
    best_tags = get_tag(model, sentence, idx_to_tag)
    print(' '.join(best_tags))
