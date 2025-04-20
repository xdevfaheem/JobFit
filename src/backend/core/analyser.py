# Analyse the resume (json object)
# Run scans and return their score and feedback
#   - keyword check
#   - Formattinf & readability check
#   - Tone & clarity
#   - relevance
#   - spelling & grammar
#   - legth appropriateness


import llm
from models.schemas import FinalVerdict, ScanResult, UserData
from utils import (
    check_resume_ats_friendliness,
    convert_pdf_to_image,
    convert_pdf_to_markdown_format,
)


class AnalyzeResume:
    def __init__(self, user_data: UserData):
        self.user_data = user_data
        self.resume_data = user_data.original_resume
        self.resume_file_path = user_data.resume_file_path
        self.resume_images_path = convert_pdf_to_image(self.resume_file_path)
        self.resume_in_markdown_format = convert_pdf_to_markdown_format(self.pdf_path)
        # variable naming sucks!

        self.analyzers = [
            (self.keyword_analysis, 0.20),
            (self.formatting_and_readability_analysis, 0.25),
            (self.relevancy_analysis, 0.25),
            (self.tone_and_language_analysis, 0.15),
            (self.spelling_and_grammar_analysis, 0.15),
        ]

    def keyword_analysis(self):
        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} postions"

        prompt = f"""
        Here is my resume (in markdown format):
        ---
        {self.resume_in_markdown_format}
        ---

        Please analyze it thouroughly for appropriate/relevant Keyword & Industry terminology usage across my resume, As it is a crucial step for ATS optimization

        Provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, prompt, ScanResult)

    def formatting_and_readability_analysis(self):
        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} postions"

        prompt = f"""
        This is my resume.

        I have analysed it thoroughly via series of scans. Here is the scan result.
        {check_resume_ats_friendliness(self.resume_file_path)}

        Please analyze it thouroughly yourself for Formatting & Readbility. Check it for clean, clear formatting, ATS-friendly layout (no complex graphics, charts, tables, or unusual fonts). As ATS-compliant is essential.

        Based on the scan results and your review, provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, [self.resume_images_path, prompt], ScanResult)

    def relevancy_analysis(self):
        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} postions"

        prompt = f"""
        Here is my resume (in markdown format):
        ---
        {self.resume_in_markdown_format}
        ---

        Please analyze it thouroughly for Alignment & Relevancy. Check how well the resume content (skills, education, experience, etc) aligns with the target position. As tailoring the resume for the target job/position is the key.

        Provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, prompt, ScanResult)

    def tone_and_language_analysis(self):
        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} postions"

        prompt = f"""
        Here is my resume (in markdown format):
        ---
        {self.resume_in_markdown_format}
        ---

        Please analyze it thoroughly for Tone & Professional language across my resume. As confident and professional tone is really important.

        Provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, prompt, ScanResult)

    def spelling_and_grammar_analysis(self):
        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} postions"

        prompt = f"""
        Here is my resume (in markdown format):
        ---
        {self.resume_in_markdown_format}
        ---

        Please analyze it thoroughly for Spelling & Grammatical errors across my resume.

        Provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, prompt, ScanResult)

    def generate_overall_feedback(self, results: list[ScanResult]):
        str_results = []
        for result in results:
            str_scan_result = f"""
            **{result.name}**
            Score: {result.score}
            Feedback(s): {"\n\t-".join(result.feedback)}
            Suggestion(s): {"\n\t-".join(result.suggestion)}
        """
            str_results.append(str_scan_result)

        final_str_results = "\n\n".join(str_results)

        system_prompt = f"You are an expert resume reviewer specializing in {self.user_data.target_job_title} positions"

        result_prompt = f"""
        Here is my resume (in markdown format):
        ---
        {self.resume_in_markdown_format}
        ---

        Here is the breif rundown on various analysis and it's result
        {final_str_results}
        
        Provide a well-thought response as specified in the ouput schema.
        """

        return llm.call(system_prompt, result_prompt, FinalVerdict)

    def analyze(self):
        results = []
        overall_score = 0

        for analysis_func, analysis_weight in self.analyzers:
            result = analysis_func()

            # converting function name to scan title
            analysis_title = analysis_func.__name__.replace("and", "&").split("_")
            result.name = (
                analysis_title[0].capitalize()
                + " "
                + analysis_title[1]
                + " ".join([word.capitalize() for word in analysis_title[2:]])
            )

            results.append(result)

            overall_score += int((result.score * 10) * analysis_weight)
            # score (1-10) * 10 (100 now) * scan's weight (weighted score out of 100)

        final_feedback = self.generate_overall_feedback(results)

        return {
            "overall_resume_score": overall_score,
            "overall_scan_results": results,
            "overall_feedback": final_feedback,
        }
