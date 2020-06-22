import torch
from torch.nn import functional as F

from _backend.loss.base.base_loss import BaseLoss


class CrossEntropyLoss(BaseLoss):

    def __init__(self, label_dict):
        """
        cross entropy loss를 계산합니다.

        :param label_dict: 라벨 딕셔너리
        """

        super(CrossEntropyLoss, self).__init__()
        self.label_dict = label_dict

    def forward(self, input, target):
        return F.cross_entropy(input, target)

    def compute_loss(self, label, logits, feats, mask=None):
        if mask is None:
            return self(logits, label)
        else:
            logits = logits.permute(0, 2, 1)
            logits_flat = logits.view(-1, logits.size(-1))
            log_probs_flat = F.log_softmax(logits_flat)
            target_flat = label.view(-1, 1)
            losses_flat = -torch.gather(log_probs_flat, dim=1, index=target_flat)
            losses = losses_flat.view(mask.size())
            losses = losses * mask.float()
            return losses.mean()