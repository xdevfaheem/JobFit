# 🧭 JobMatch - User Journey

## Phase 1 - Resume Optimization 
- Landing Page
- Get user input (resume upload + target title/role/job)
- Parse and get all the required attribute from the user data.
- Analysis the resume, run heuristic checks, generate scores and their corresponding feedbacks, showcase them to the user.Use minstral.ai LLM for this.
- Enhance all resume, based on the generated feedbacks, rewrite and improve all the necessary content, complying with the feedbacks gathered earlier.
- With the updated resume attributes, render it into a clean, elegant, ATS-friendly, common, universal format. I found an awesome [tool](https://rendercv.com/) and it python [package](https://github.com/rendercv/rendercv) too

## Phase 2 - Job Matching
- Get initial jobs based on the job title/role
- Generate match score based on job description and resume content (we got to we figure out this part)
- Shortlist the job records and rank them based on match score
- Recommend those jobs to the user.

By now, user would get the enhanced resume along with jobs that most fit the user.

## Phase 3 - Auto Apply (Optional)
- For now, for the sake of MVP, user has to apply to the jobs that we recommends, with the enhanced resume that we provides.
