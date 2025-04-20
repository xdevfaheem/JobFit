from dataclasses import dataclass, field
from typing import Any

from analysis import FullAnalysisResult


@dataclass
class UserData:
    target_job_title: str
    resume_file_path: str
    original_resume: dict[str, Any] = field(default_factory=dict)
    analysis_results: FullAnalysisResult = field(default=None)
    enhanced_resume: dict[str, Any] = field(default_factory=dict)
