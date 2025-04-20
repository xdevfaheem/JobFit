import uvicorn
from core.analyser import AnalyzeResume
from core.parser import create_extraction, parse
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from schemas.analysis import FullAnalysisResult
from schemas.cv import cv_fields
from schemas.io import UploadResponse
from schemas.user_data import UserData
from utils import save_upload_file

# in-memory db (just for now, will swap them later :)
db = {}

# create extrata ai data extraction for parsing
create_extraction(cv_fields)

app = FastAPI(
    title="JobFit API", description="AI-Powered Resume Optimization & Job Matching"
)


@app.post("/upload", tags=["Resume"], response_model=UploadResponse)
async def upload_resume(
    user_id: str = Form(...),
    target_job_title: str = Form(...),
    file: UploadFile = File(...),
):
    # Upload and parse the resume and save the user

    try:
        # saving it locally now, but later would do cloud storage object
        file_path = save_upload_file(file)
        parsed_resume = parse(file_path)

        db[user_id] = UserData(
            target_job_title=target_job_title,
            resume_file_path=file_path,
            original_resume=parsed_resume,
        )
        return {"message": "Resume successfully parsed and stored!"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal error occured: {str(e)}")


@app.post("/analyze", tags=["Resume"], response_model=FullAnalysisResult)
async def analyze_resume(user_id: str = Form(...)):
    # Analyze the user resume and provide feedbac

    try:
        if user_id not in db:
            raise HTTPException(
                status_code=400,
                detail=f"User ({user_id}) is not found. upload your resume first",
            )

        analyzer = AnalyzeResume(db[user_id])
        response = analyzer.analyze()

        # store the user analysis
        db[user_id].analysis_results = response

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Internal error occured: {str(e)}")


# @app.post("/enhance", tags=["Resume"])
# async def enhance_resume(user_id: str = Form(...)):
#     """Enhance the resume based on previous analysis"""

#     try:
#         if user_id not in db:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"User ({user_id}) not found. Upload your resume first.",
#             )

#         # Check if analysis has been done
#         if "analysis_results" not in db[user_id].__dict__:
#             raise HTTPException(
#                 status_code=400, detail="Resume analysis not found. Run analysis first."
#             )

#         enhancer = EnhanceResume(db[user_id], db[user_id].analysis_results)
#         enhanced_resume = enhancer.enhance()

#         # Store the enhanced resume
#         db[user_id].enhanced_resume = enhanced_resume

#         return enhanced_resume

#     except Exception as e:
#         raise HTTPException(
#             status_code=400, detail=f"Internal error occurred: {str(e)}"
#         )


@app.get("/jobs", tags=["Jobs"])
async def find_matching_jobs(skills: list, experience: int, location: str):
    """Find jobs matching a candidate's profile"""
    # Job matching logic here
    return {"matches": []}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
