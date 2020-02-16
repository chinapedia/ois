import os
import pickle

from utils import PAD, UNK, DATASET


word_to_idx = {PAD: 0, UNK: 1}      # PAD 填充    UNK 未知

tag_to_idx = {}


def is_num(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sentences = f.read().split('\n')
        data = []
        for s in sentences:
            tuples = [ln.split('/') for ln in s.split(' ')]

            data.append(tuple(zip(*tuples)))
    return data


def get_idx(train_data):

    global word_to_idx
    global tag_to_idx
    for words, tags in train_data:
        for w in words:
            if w not in word_to_idx:
                word_to_idx[w] = len(word_to_idx)
        for t in tags:
            if t not in tag_to_idx:
                tag_to_idx[t] = len(tag_to_idx)


def zero_setting(data):             # 将数字置零减少维度
    new_data = []
    for words, tags in data:
        new_words = []
        for w in words:
            new_w = '0' if is_num(w) else w
            new_words.append(new_w)
        new_tags = list(tags)
        new_data.append((new_words, new_tags))
    return new_data


def dump_obj(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_obj(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return obj


def transform(data):             # word, tag 转换成 id
    new_data = []
    for words, tags in data:
        word_ids = [word_to_idx.get(w, word_to_idx[UNK]) for w in words]
        tag_ids = [tag_to_idx.get(t) for t in tags]
        new_data.append((word_ids, tag_ids))
    return new_data


def my_preprocess():
    train_data = read_file(f'data/{DATASET}/raw/train.txt')
    test_data = read_file(f'data/{DATASET}/raw/test.txt')
    dev_data = read_file(f'data/{DATASET}/raw/dev.txt')
    print(f'train: {len(train_data)}, test: {len(test_data)}, dev: {len(dev_data)}')

    train_data = zero_setting(train_data)
    test_data = zero_setting(test_data)
    dev_data = zero_setting(dev_data)
    print(train_data[0], test_data[0], dev_data[0])

    get_idx(train_data)
    print(f'words: {len(word_to_idx)}')
    print(tag_to_idx)

    # word tag -> id
    train_data = transform(train_data)
    dev_data = transform(dev_data)
    test_data = transform(test_data)

    # 保存预处理结果
    data_dir = f'data/{DATASET}/processed'
    dump_obj(train_data, os.path.join(data_dir, 'train.pkl'))
    dump_obj(test_data, os.path.join(data_dir, 'test.pkl'))
    dump_obj(dev_data, os.path.join(data_dir, 'dev.pkl'))
    dump_obj(word_to_idx, os.path.join(data_dir, 'word_to_idx.pkl'))
    dump_obj(tag_to_idx, os.path.join(data_dir, 'tag_to_idx.pkl'))
    print('processed done!')


if __name__ == '__main__':
    my_preprocess()
