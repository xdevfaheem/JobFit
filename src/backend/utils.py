import datetime
import io
import os
import re
import shutil

import markitdown
import numpy as np
import pymupdf
from fastapi import UploadFile
from PIL import Image


def generate_keywords(target_job_title: str): ...


def generate_resume(resume_json: dict):
    # json -> rendercv yaml -> resume pdf (with custom/default theme)
    ...


def convert_pdf_to_image(pdf_path: str):
    doc = pymupdf.open(pdf_path)
    file_paths = []

    for i in range(len(doc)):
        page = doc.load_page(i)
        pix = page.get_pixmap(dpi=300)
        file_name = "{}_page_num_{}.png".format(pdf_path.split(".")[0], i)
        pix.save(file_name)
        file_paths.append(file_name)

    doc.close()
    return file_paths


def convert_pdf_to_markdown_format(pdf_path):
    # using fairly simple markitdown (https://github.com/microsoft/markitdown) as of now. But had to rewrite this for more robust conversion, something like MinerU (https://github.com/opendatalab/MinerU)

    md = markitdown.MarkItDown()
    result = md.convert(pdf_path)
    return result.text_content


def check_resume_ats_friendliness(pdf_path):
    # Analyze a PDF resume to determine if it contains elements that might not be ATS-friendly.

    results = {
        "has_images": False,
        "has_charts": False,
        "has_complex_layout": False,
        "has_tables": False,
        "has_multiple_columns": False,
        "ats_friendly": True,
        "issues_found": [],
    }

    try:
        # Open the PDF
        doc = pymupdf.open(pdf_path)

        # Track elements across all pages
        total_images = 0
        total_text_blocks = 0

        for page_num, page in enumerate(doc):
            # Check for images
            image_list = page.get_images(full=True)
            if image_list:
                results["has_images"] = True
                total_images += len(image_list)
                results["issues_found"].append(
                    f"Found {len(image_list)} images on page {page_num + 1}"
                )

            # Check for complex layout
            blocks = page.get_text("dict")["blocks"]
            total_text_blocks += len(blocks)

            # Analyze text blocks for multi-column layout
            if len(blocks) > 3:  # Simple heuristic for complexity
                x_positions = []
                for block in blocks:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                x_positions.append(span["bbox"][0])  # x0 position

                # If there are significant clusters of x-positions, might be multi-column
                if x_positions:
                    x_positions = np.array(x_positions)
                    unique_positions = np.unique(np.round(x_positions, -1))

                    if len(unique_positions) >= 3:
                        results["has_multiple_columns"] = True
                        results["issues_found"].append(
                            "Detected possible multi-column layout"
                        )

            # Check for tables by looking for grid-like patterns
            text = page.get_text()
            if (
                len(re.findall(r"\|\s+\|", text)) > 2
                or len(re.findall(r"\+[-+]+\+", text)) > 0
            ):
                results["has_tables"] = True
                results["issues_found"].append(
                    f"Detected possible tables on page {page_num + 1}"
                )

            # Additional check for charts - simple heuristic based on image size and position
            for img_index, img in enumerate(image_list):
                xref = img[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    img = Image.open(io.BytesIO(image_bytes))

                    # Check if image dimensions suggest a chart (typically wider than tall)
                    width, height = img.size
                    if width > height * 1.5 and width > 200:
                        results["has_charts"] = True
                        results["issues_found"].append(
                            f"Detected possible chart on page {page_num + 1}"
                        )
                except Exception:
                    # If we can't analyze the image, better to flag it as potential issue
                    results["issues_found"].append(
                        f"Unanalyzable image found on page {page_num + 1}"
                    )

        # Determine overall complex layout
        if total_text_blocks > 15 or results["has_multiple_columns"]:
            results["has_complex_layout"] = True

        # Determine ATS friendliness
        if (
            results["has_images"]
            or results["has_charts"]
            or results["has_complex_layout"]
            or results["has_tables"]
            or results["has_multiple_columns"]
        ):
            results["ats_friendly"] = False

    except Exception as e:
        results["error"] = str(e)
        results["ats_friendly"] = False
        results["issues_found"].append(f"Error analyzing PDF: {str(e)}")

    return results


def save_upload_file(upload_file: UploadFile, destination_dir: str = "uploads") -> str:
    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Define the full path to save the file
    file_path = os.path.join(destination_dir, upload_file.filename)

    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


def clean_date(date_str):
    """Format dates to YYYY-MM format for RenderCV"""
    if not date_str:
        return None

    # Handle "present" or current dates
    if date_str.lower() in ["present", "current", "now"]:
        return "present"

    # Try to parse different date formats
    date_formats = [
        "%Y-%m-%d",
        "%Y-%m",
        "%Y/%m/%d",
        "%Y/%m",
        "%m/%Y",
        "%m-%Y",
        "%B %Y",
        "%b %Y",
    ]

    for fmt in date_formats:
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            # Return in YYYY-MM format
            return parsed_date.strftime("%Y-%m")
        except ValueError:
            continue

    # If only year is available
    if re.match(r"^\d{4}$", date_str):
        return date_str

    # Return as is if we couldn't parse it
    return date_str
