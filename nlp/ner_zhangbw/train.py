import os
import torch
import torch.optim as optim
from seqeval.metrics import f1_score, precision_score, recall_score
from torch.utils.data import DataLoader
from utils import DATASET, EMBEDDING_DIM, HIDDEN_DIM, DROPOUT, BATCH_SIZE, LEARN_RATE, EPOCHS, LOG_INTERVAL, PATIENCE
from model import BatchPadding, NERDataset, BiLSTM_CRF
from preprocess import load_obj


def score(true_array, prediction_array):
    precision = precision_score(true_array, prediction_array)
    recall = recall_score(true_array, prediction_array)
    f1 = f1_score(true_array, prediction_array)
    return precision, recall, f1


def evaluate(model, loader, idx_to_tag):
    device = torch.device('cuda')
    model.eval()
    prediction_array = []
    true_array = []
    with torch.no_grad():
        for seqs, tags, masks in loader:
            # prediction
            tags_prediction = model.decode(seqs.to(device), masks.to(device))
            for tp in tags_prediction:
                prediction_array.append([idx_to_tag[idx] for idx in tp])
            # true
            lens = masks.sum(0).tolist()
            tags_true = tags.t().tolist()
            for t, length in zip(tags_true, lens):
                true_array.append([idx_to_tag[idx] for idx in t[:length]])
    return score(true_array, prediction_array)


def my_train():
    os.makedirs(f"model_result", exist_ok=True)
    torch.manual_seed(1)
    device = torch.device('cuda')

    data_dir = f"data/{DATASET}/processed"

    # 加载
    train_data = NERDataset(os.path.join(data_dir, "train.pkl"))
    test_data = NERDataset(os.path.join(data_dir, "test.pkl"))
    dev_data = NERDataset(os.path.join(data_dir, "dev.pkl"))

    word_to_idx = load_obj(os.path.join(data_dir, "word_to_idx.pkl"))
    tag_to_idx = load_obj(os.path.join(data_dir, "tag_to_idx.pkl"))

    idx_to_tag = {n: m for m, n in tag_to_idx.items()}

    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, collate_fn=BatchPadding(), shuffle=True, num_workers=2, pin_memory=True,)
    dev_loader = DataLoader(dev_data, batch_size=BATCH_SIZE, collate_fn=BatchPadding(), shuffle=True, num_workers=2, pin_memory=True,)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, collate_fn=BatchPadding(), shuffle=True, num_workers=2, pin_memory=True,)

    # 建模
    model = BiLSTM_CRF(len(word_to_idx), len(tag_to_idx), EMBEDDING_DIM, HIDDEN_DIM, DROPOUT).to(device)
    print(model)
    optimizer = optim.Adam(model.parameters(), lr=LEARN_RATE)

    print("\n开始训练")
    f1_max = 0
    cur_patience = 0        # 用于避免过拟合
    for epoch in range(EPOCHS):
        model.train()
        for i, (seqs, tags, masks) in enumerate(train_loader, 1):
            optimizer.zero_grad()
            loss = model.loss(seqs.to(device), tags.to(device), masks.to(device))
            loss.backward()
            optimizer.step()
            if i % LOG_INTERVAL == 0:
                print(
                    "epoch {}: {:.0f}%\t\tLoss: {:.6f}".format(epoch, 100.0 * i / len(train_loader), loss.item())
                )
        dev_precision, dev_recall, dev_f1 = evaluate(model, dev_loader, idx_to_tag)
        test_precision, test_recall, test_f1 = evaluate(model, test_loader, idx_to_tag)
        print(f"\ndev\tprecision: {dev_precision}, recall: {dev_recall}, f1: {dev_f1}")
        print(f"test\tprecision: {test_precision}, recall: {test_recall}, f1: {test_f1}\n")

        torch.save(model.state_dict(), f"model_result/{epoch}.pt")

        if dev_f1 > f1_max:                 # 用于检测过拟合情况
            f1_max = dev_f1
            cur_patience = 0
            if dev_f1 > 0.9 and test_f1 > 0.9:
                break
        else:
            cur_patience += 1
            if cur_patience >= PATIENCE:    # 多次低于最高f1，break
                break
    print("Best dev F1: ", f1_max)


if __name__ == '__main__':
    my_train()
