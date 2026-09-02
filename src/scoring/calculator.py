"""Truth score calculation."""
from typing import Dict, List


class TruthScoreCalculator:
    """Calculate truth score from multiple evidence sources."""

    def calculate(
        self,
        model_confidence: float,
        model_prediction: int,
        fact_checks: Dict,
        web_evidence: Dict,
        source_analysis: List[Dict],
    ) -> Dict:
        # Model score (0-100)
        model_score = model_confidence * 100
        if model_prediction == 1:  # FAKE
            model_score = 100 - model_score

        # Fact-check score
        fc_count = fact_checks.get("count", 0)
        fc_agreement = fact_checks.get("agreement_score", 0) or 0
        fc_consensus = fact_checks.get("verdict_consensus")

        fc_score = 50  # neutral
        if fc_count > 0:
            if fc_consensus == "supported":
                fc_score = 80 + (fc_agreement * 0.2)
            elif fc_consensus == "likely_false":
                fc_score = 20 - (fc_agreement * 0.2)
            elif fc_consensus == "misleading":
                fc_score = 50

        # Source credibility score
        if source_analysis:
            avg_cred = sum(s.get("credibility_score", 50) for s in source_analysis) / len(source_analysis)
        else:
            avg_cred = 50

        # Web evidence score
        web_score = 50
        if web_evidence.get("has_official_source"):
            web_score += 20
        if web_evidence.get("has_news_coverage"):
            web_score += 10
        if web_evidence.get("count", 0) > 3:
            web_score += 10

        # Weighted combination (model has higher weight for strong predictions)
        weights = {"model": 0.40, "factcheck": 0.30, "source": 0.15, "web": 0.15}
        truth_score = (
            model_score * weights["model"] +
            fc_score * weights["factcheck"] +
            avg_cred * weights["source"] +
            web_score * weights["web"]
        )

        # Overall confidence
        overall_confidence = model_confidence
        if fc_count > 0:
            overall_confidence = max(overall_confidence, fc_agreement / 100)

        return {
            "truth_score": round(max(0, min(100, truth_score)), 1),
            "overall_confidence": round(overall_confidence, 3),
            "evidence_score": round(web_score, 1),
            "source_credibility": round(avg_cred, 1),
            "breakdown": {
                "model": round(model_score, 1),
                "fact_check": round(fc_score, 1),
                "source": round(avg_cred, 1),
                "web": round(web_score, 1),
            },
        }
