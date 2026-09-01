"""Optuna-based hyperparameter tuning."""

import argparse

import optuna
from optuna.trial import Trial
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


def objective(trial: Trial) -> float:
    n_estimators = trial.suggest_int("n_estimators", 50, 500)
    max_depth = trial.suggest_int("max_depth", 3, 30)
    min_samples_split = trial.suggest_int("min_samples_split", 2, 20)

    X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=42,
        n_jobs=-1,
    )

    score = cross_val_score(clf, X, y, cv=5, scoring="f1_macro").mean()
    return float(score)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=100)
    args = parser.parse_args()

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=args.trials)

    print(f"Best score: {study.best_value}")
    print(f"Best params: {study.best_params}")


if __name__ == "__main__":
    main()
