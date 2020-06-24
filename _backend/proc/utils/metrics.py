"""
@auther Hyunwoong
@since {6/23/2020}
@see : https://github.com/gusdnd852
"""
import numpy as np
from pandas import DataFrame
from sklearn.metrics import \
    accuracy_score, \
    f1_score, \
    classification_report, \
    confusion_matrix, precision_score, recall_score


class Metrics:

    def __init__(self, label_dict, logging_precision):
        self.label_dict = label_dict
        self.p = logging_precision
        self.train_label, self.train_predict = None, None
        self.test_label, self.test_predict = None, None

    def evaluate(self, label, predict, mode) -> dict:
        """
        accuracy와 loss를 출력합니다.

        :param label: 라벨
        :param predict: 예측
        :param mode: train or test
        :return: 정확도
        """

        if mode == 'train':
            self.train_label = label
            self.train_predict = predict

        elif mode == 'test':
            self.test_label = label
            self.test_predict = predict

        else:
            raise Exception("mode는 train과 test만 가능합니다.")

        if not isinstance(label, np.ndarray):
            label = label.detach().cpu().numpy()
        if not isinstance(predict, np.ndarray):
            predict = predict.detach().cpu().numpy()

        return {'accuracy': accuracy_score(label, predict),
                'precision': precision_score(label, predict, average='macro'),
                'recall': recall_score(label, predict, average='macro'),
                'f1_score': f1_score(label, predict, average='macro')}

    def report(self, mode):
        """
        분류 보고서와 confusion matrix를 출력합니다.
        여기에는 Precision, Recall, F1 Score, Accuracy 등이 포함됩니다.

        :return: 다양한 메트릭으로 측정한 모델 성능
        """

        if mode == 'train':
            label = self.train_label
            predict = self.train_predict

        elif mode == 'test':
            label = self.test_label
            predict = self.test_predict

        else:
            raise Exception("mode는 train과 test만 가능합니다.")

        if not isinstance(label, np.ndarray):
            label = label.detach().cpu().numpy()
        if not isinstance(predict, np.ndarray):
            predict = predict.detach().cpu().numpy()

        report = DataFrame(
            classification_report(
                y_true=label,
                y_pred=predict,
                target_names=list(self.label_dict),
                output_dict=True
            )
        )

        matrix = confusion_matrix(
            y_true=label,
            y_pred=predict
        )

        return report.round(self.p), matrix