from pydantic import BaseModel, Field


class ScanResult(BaseModel):
    score: int = Field(
        ...,
        title="Score",
        description="Numerical score in the scale from 1 to 10",
        examples=[5, 7, 9.5],
    )
    feedback: str = Field(
        ..., title="Feedback", description="Explain why you gave that score"
    )
    suggestion: str = Field(
        ...,
        title="Improvement Suggestions",
        description="Give some specific suggestions for improvement",
    )

    model_config = {
        "extra": "allow"  # to add name and weight attribute later on, else it throws attribute error
    }


class FinalVerdict(BaseModel):
    verdict: list[str] = Field(
        ...,
        title="Final Verdict",
        description="The final verdict/thoughts including the overall feedbacks and improvements",
    )


class FullAnalysisResult(BaseModel):
    overall_resume_score: int = 0
    overall_results: list[ScanResult]
    overall_feedback: FinalVerdict
