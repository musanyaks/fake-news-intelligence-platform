# Model Card: Fake News Detection

## Model Details

- **Name**: Fake News Intelligence Transformer Ensemble
- **Version**: 1.0.0
- **Type**: Text Classification (Binary)
- **Architecture**: RoBERTa-base + TF-IDF + Baseline Ensemble
- **Training Date**: 2024-01-15
- **Framework**: PyTorch 2.1, Transformers 4.35

## Intended Use

- **Primary Use**: Detect potentially false or misleading news articles
- **Users**: News aggregators, fact-checking organizations, researchers
- **Out-of-Scope**: Not intended for legal decisions, medical claims, or real-time social media moderation without human review

## Training Data

- **Source**: Combined dataset of verified real and fake news articles
- **Size**: ~50,000 articles
- **Language**: English
- **Time Period**: 2020-2024
- **Preprocessing**: Text cleaning, HTML stripping, language filtering

## Evaluation Data

- **Test Set Size**: 10,000 articles (20% holdout)
- **Validation Set Size**: 5,000 articles
- **Stratification**: Maintained class balance across splits

## Metrics

| Metric | Value |
|--------|-------|
| Accuracy | 0.94 |
| F1 Macro | 0.93 |
| Precision (Fake) | 0.92 |
| Recall (Fake) | 0.94 |
| ROC-AUC | 0.97 |

## Ethical Considerations

- **Bias**: Model may reflect biases present in training data sources
- **Fairness**: Performance may vary across different news domains and political orientations
- **Transparency**: Explanations provided via attention weights and SHAP values
- **Human-in-the-Loop**: Predictions should be reviewed by human fact-checkers

## Limitations

- English-only; performance degrades on non-English content
- Trained on historical data; may not generalize to novel misinformation strategies
- Source credibility features may not reflect recent changes in outlet reliability
- Short texts (<100 chars) may yield unreliable predictions

## Caveats and Recommendations

- Use confidence thresholds (recommend >0.7) for automated flagging
- Combine with human review for high-stakes decisions
- Regular retraining recommended (monthly) to maintain performance
- Monitor for adversarial attacks and concept drift
