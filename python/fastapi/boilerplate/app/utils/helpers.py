"""Utility helper functions."""

def format_prediction_result(prediction: dict) -> dict:
    """Format prediction result for response."""
    return {
        "label": prediction.get("label", "unknown"),
        "confidence": round(prediction.get("confidence", 0.0), 4)
    }

