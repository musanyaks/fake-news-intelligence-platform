"""Model calibration utilities."""
import numpy as np
from sklearn.calibration import calibration_curve
from sklearn.isotonic import IsotonicRegression


class ModelCalibrator:
    """Calibrate model probabilities."""

    def __init__(self, method: str = "isotonic"):
        self.method = method
        self.calibrator = None

    def fit(self, y_true: np.ndarray, y_prob: np.ndarray) -> "ModelCalibrator":
        if self.method == "isotonic":
            self.calibrator = IsotonicRegression(y_min=0, y_max=1, out_of_bounds="clip")
            self.calibrator.fit(y_prob, y_true)
        return self

    def calibrate(self, y_prob: np.ndarray) -> np.ndarray:
        if self.calibrator is None:
            raise RuntimeError("Calibrator not fitted")
        return self.calibrator.predict(y_prob)

    @staticmethod
    def expected_calibration_error(
        y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10
    ) -> float:
        bin_boundaries = np.linspace(0, 1, n_bins + 1)
        ece = 0.0
        for i in range(n_bins):
            mask = (y_prob >= bin_boundaries[i]) & (y_prob < bin_boundaries[i + 1])
            if i == n_bins - 1:
                mask = (y_prob >= bin_boundaries[i]) & (y_prob <= bin_boundaries[i + 1])
            if mask.sum() > 0:
                avg_confidence = y_prob[mask].mean()
                avg_accuracy = y_true[mask].mean()
                ece += mask.sum() * np.abs(avg_confidence - avg_accuracy)
        return ece / len(y_true)
