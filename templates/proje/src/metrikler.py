"""Klinik değerlendirme metrikleri: tek fonksiyonla ROC-AUC, PR-AUC, Brier ve eşiğe bağlı ölçütler."""
import numpy as np
from sklearn.metrics import (average_precision_score, brier_score_loss, confusion_matrix,
                             roc_auc_score)


def klinik_rapor(y_true, p, esik=0.5):
    """y_true: 0/1 dizisi, p: pozitif sınıf olasılığı. Sözlük döndürür."""
    y_true = np.asarray(y_true); p = np.asarray(p)
    yhat = (p >= esik).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, yhat, labels=[0, 1]).ravel()
    return {
        "roc_auc": roc_auc_score(y_true, p),
        "pr_auc": average_precision_score(y_true, p),
        "brier": brier_score_loss(y_true, p),
        "esik": esik,
        "duyarlilik": tp / (tp + fn) if tp + fn else float("nan"),
        "ozgulluk": tn / (tn + fp) if tn + fp else float("nan"),
        "ppv": tp / (tp + fp) if tp + fp else float("nan"),
        "npv": tn / (tn + fn) if tn + fn else float("nan"),
    }
