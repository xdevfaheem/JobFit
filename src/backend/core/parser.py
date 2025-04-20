import mimetypes
import os
import time

import requests
import yaml
from utils import clean_date

extraction_id, batch_id = None, None
token = os.environ["EXTRACTA_API_KEY"]

# found extracta.ai super intersting, just define the target struture you need and pass in you file, get structured extracted data, sounds cool at first
# but making it work sucks... not good enough documentation, feels gptye.. no sdk/package as of now, so i got to glue together two endpoints and poll the second one with the ouput of first request... all these just by following docs words...
# global vars ...
# https://docs.extracta.ai/api-reference/api-endpoints


def create_extraction(field_schema: list[dict]):
    global token
    url = "https://api.extracta.ai/api/v1/createExtraction"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}

    extraction_details = {
        "extractionDetails": {
            "name": "RenderCV Format Extraction",
            "language": "Multi-Lingual",
            "options": {
                "hasTable": False,
                "hasVisuals": True,
                "handwrittenTextRecognition": False,
            },
            "fields": field_schema,
        }
    }

    try:
        response = requests.post(url, json=extraction_details, headers=headers)
        response.raise_for_status()  # Raises an HTTPError if the response status code is 4XX/5XX
        global extraction_id
        extraction_id = response.json()["extractionId"]
    except requests.RequestException as e:
        # Handles any requests-related errors
        print(e)
        return None


def get_file_result(file):
    global extraction_id, batch_id, token

    upload_url = "https://api.extracta.ai/api/v1/uploadFiles"
    upload_headers = {
        "Content-Type": "multipart/form-data",
        "Authorization": f"Bearer {token}",
    }

    # Prepare the files for uploading
    file_streams = [
        (
            "files",
            (
                file,
                open(file, "rb"),
                mimetypes.guess_type(file)[0] or "application/octet-stream",
            ),
        )
    ]
    payload = {"extractionId": extraction_id}
    if batch_id is not None:
        payload["batchId"] = batch_id

    try:
        # upload file (https://docs.extracta.ai/api-reference/api-endpoints/5.-upload-files)
        response = requests.post(
            upload_url, files=file_streams, data=payload, headers=upload_headers
        )
        if response.status_code == 200:
            upload_result = response.json()  # Return the parsed JSON response
        else:
            response.raise_for_status()

        batch_id = upload_result["batchId"]
        file_id = upload_result["files"][0]["fileId"]

        # get response (https://docs.extracta.ai/api-reference/api-endpoints/6.-get-results)
        # poll untill result is processed
        result_url = "https://api.extracta.ai/api/v1/getBatchResults"
        result_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        }
        payload["batchId"] = batch_id
        payload["fileId"] = file_id

        while True:
            response = requests.post(result_url, json=payload, headers=result_headers)

            if response.status_code == 200:
                result = response.json()
                if result["status"] == "waiting":
                    time.sleep(2)
                    continue
                else:
                    return result["files"][0]["result"]
            else:
                response.raise_for_status()

    except requests.HTTPError as e:
        # Print server-side error message
        if response.status_code >= 400:
            error_message = response.json()
            print(f"Server returned an error: {error_message}")
        else:
            print(f"HTTP error occurred: {e}")
    except requests.RequestException as e:
        # Handle other requests exceptions
        print(f"Failed to upload files: {e}")
    except Exception as e:
        # Handle other possible exceptions
        print(f"An unexpected error occurred: {e}")
    return None


def convert_to_rendercv(extracted_data):
    # convert extracted resume data to rendercv format
    rendercv_data = {"cv": {"sections": {}}}

    # Process personal information
    if "personal_info" in extracted_data:
        personal = extracted_data["personal_info"]
        if "name" in personal:
            rendercv_data["cv"]["name"] = personal["name"]
        if "location" in personal:
            rendercv_data["cv"]["location"] = personal["location"]
        if "email" in personal:
            rendercv_data["cv"]["email"] = personal["email"]
        if "phone" in personal:
            rendercv_data["cv"]["phone"] = personal["phone"]
        if "website" in personal:
            rendercv_data["cv"]["website"] = personal["website"]

    # Process social networks
    if "social_networks" in extracted_data:
        rendercv_data["cv"]["social_networks"] = []
        for network in extracted_data["social_networks"]:
            rendercv_data["cv"]["social_networks"].append(
                {"network": network["network"], "username": network["username"]}
            )

    # Process work experience
    if "work_experience" in extracted_data:
        rendercv_data["cv"]["sections"]["Work Experience"] = []
        for job in extracted_data["work_experience"]:
            job_entry = {"company": job["company"], "position": job["position"]}

            if "location" in job:
                job_entry["location"] = job["location"]

            if "start_date" in job:
                job_entry["start_date"] = clean_date(job["start_date"])

            if "end_date" in job:
                job_entry["end_date"] = clean_date(job["end_date"])

            if "summary" in job:
                job_entry["summary"] = job["summary"]

            if "highlights" in job:
                job_entry["highlights"] = job["highlights"]

            rendercv_data["cv"]["sections"]["Work Experience"].append(job_entry)

    # Process education
    if "education" in extracted_data:
        rendercv_data["cv"]["sections"]["Education"] = []
        for edu in extracted_data["education"]:
            edu_entry = {"institution": edu["institution"], "area": edu["area"]}

            if "degree" in edu:
                edu_entry["degree"] = edu["degree"]

            if "location" in edu:
                edu_entry["location"] = edu["location"]

            if "start_date" in edu:
                edu_entry["start_date"] = clean_date(edu["start_date"])

            if "end_date" in edu:
                edu_entry["end_date"] = clean_date(edu["end_date"])

            if "highlights" in edu:
                edu_entry["highlights"] = edu["highlights"]

            rendercv_data["cv"]["sections"]["Education"].append(edu_entry)

    # Process skills
    if "skills" in extracted_data and extracted_data["skills"]:
        rendercv_data["cv"]["sections"]["Skills"] = []
        for skill in extracted_data["skills"]:
            rendercv_data["cv"]["sections"]["Skills"].append({"bullet": skill})

    # Process languages
    if "languages" in extracted_data and extracted_data["languages"]:
        rendercv_data["cv"]["sections"]["Languages"] = []
        for language in extracted_data["languages"]:
            rendercv_data["cv"]["sections"]["Languages"].append({"numbered": language})

    # Process certifications
    if "certifications" in extracted_data and extracted_data["certifications"]:
        rendercv_data["cv"]["sections"]["Certifications"] = []
        for cert in extracted_data["certifications"]:
            cert_entry = {"name": cert["name"]}

            if "date" in cert:
                cert_entry["date"] = clean_date(cert["date"])

            if "summary" in cert:
                cert_entry["summary"] = cert["summary"]

            rendercv_data["cv"]["sections"]["Certifications"].append(cert_entry)

    # Process publications
    if "publications" in extracted_data and extracted_data["publications"]:
        rendercv_data["cv"]["sections"]["Publications"] = []
        for pub in extracted_data["publications"]:
            pub_entry = {"title": pub["title"], "authors": pub["authors"]}

            if "journal" in pub:
                pub_entry["journal"] = pub["journal"]

            if "date" in pub:
                pub_entry["date"] = clean_date(pub["date"])

            if "url" in pub:
                pub_entry["url"] = pub["url"]

            if "doi" in pub:
                pub_entry["doi"] = pub["doi"]

            rendercv_data["cv"]["sections"]["Publications"].append(pub_entry)

    # Process projects
    if "projects" in extracted_data and extracted_data["projects"]:
        rendercv_data["cv"]["sections"]["Projects"] = []
        for project in extracted_data["projects"]:
            proj_entry = {"name": project["name"]}

            if "summary" in project:
                proj_entry["summary"] = project["summary"]

            if "start_date" in project:
                proj_entry["start_date"] = clean_date(project["start_date"])

            if "end_date" in project:
                proj_entry["end_date"] = clean_date(project["end_date"])

            if "highlights" in project:
                proj_entry["highlights"] = project["highlights"]

            rendercv_data["cv"]["sections"]["Projects"].append(proj_entry)

    # Process custom sections
    if "custom_sections" in extracted_data:
        for section in extracted_data["custom_sections"]:
            section_entries = []

            for entry in section["entries"]:
                # Assuming these are simple text entries
                section_entries.append(entry["content"])

            rendercv_data["cv"]["sections"][section["title"]] = section_entries

    if "summary" in extracted_data:
        rendercv_data["cv"]["sections"]["Summary"] = extracted_data["summary"]

    return rendercv_data


def save_rendercv_yaml(data):
    # Save the parsed rendercv cv structure as rendercv yaml (load base, set attr, dump new)

    with open("assets/base_rendercv.yaml", "r") as f:
        yaml_data = yaml.safe_load(f)

    yaml_data["cv"] = data

    output_file = f"assets/{data['name']}_rendercv.yaml"
    with open(output_file, "w") as f:
        yaml.dump(yaml_data, f, sort_keys=False, default_flow_style=False)

    return output_file


def parse(file: str):
    # parse the input file (resume) into rendercv format

    extracted_data = get_file_result(file)
    rendercv_data = convert_to_rendercv(extracted_data)
    saved_file = save_rendercv_yaml(rendercv_data["cv"])

    return saved_file
