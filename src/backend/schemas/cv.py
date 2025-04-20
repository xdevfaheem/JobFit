cv_fields = [
    {
        "key": "personal_info",
        "description": "Personal information of the person",
        "type": "object",
        "properties": [
            {
                "key": "name",
                "description": "Full name of the person",
                "example": "John Doe",
                "type": "string",
            },
            {
                "key": "email",
                "description": "Email address of the person",
                "example": "john.doe@example.com",
                "type": "string",
            },
            {
                "key": "phone",
                "description": "Phone number of the person",
                "example": "+1 (555) 123-4567",
                "type": "string",
            },
            {
                "key": "location",
                "description": "Location or address of the person",
                "example": "New York, NY",
                "type": "string",
            },
            {
                "key": "website",
                "description": "Personal website URL",
                "example": "https://johndoe.com",
                "type": "string",
            },
        ],
    },
    {
        "key": "social_networks",
        "description": "Social media profiles of the person",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "network",
                    "description": "Name of the social network",
                    "example": "LinkedIn",
                    "type": "string",
                },
                {
                    "key": "username",
                    "description": "Username or profile identifier on the network",
                    "example": "johndoe",
                    "type": "string",
                },
            ],
        },
    },
    {
        "key": "summary",
        "description": "Professional or Exceutive summary of the person",
        "example": "Results-driven marketing manager with 7+ years of experience in digital advertising. Proven track record of increasing online engagement by 40% through strategic planning and social media campaigns. Skilled in data analysis and campaign optimization.",
        "type:": "string",
    },
    {
        "key": "work_experience",
        "description": "Professional work experience of the person",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "company",
                    "description": "Name of the company or organization",
                    "example": "Acme Corporation",
                    "type": "string",
                },
                {
                    "key": "position",
                    "description": "Job title or role",
                    "example": "Senior Software Engineer",
                    "type": "string",
                },
                {
                    "key": "location",
                    "description": "Location of the job",
                    "example": "San Francisco, CA",
                    "type": "string",
                },
                {
                    "key": "start_date",
                    "description": "Start date of employment in YYYY-MM format",
                    "example": "2020-01",
                    "type": "string",
                },
                {
                    "key": "end_date",
                    "description": "End date of employment in YYYY-MM format or 'present' for current jobs",
                    "example": "2022-06",
                    "type": "string",
                },
                {
                    "key": "summary",
                    "description": "Brief description of the role",
                    "example": "Led a team of 5 developers in creating a new customer portal.",
                    "type": "string",
                },
                {
                    "key": "highlights",
                    "description": "Key accomplishments or responsibilities as bullet points",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "example": "Increased system performance by 40% through database optimization",
                    },
                },
            ],
        },
    },
    {
        "key": "education",
        "description": "Educational background of the person",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "institution",
                    "description": "Name of the educational institution",
                    "example": "Stanford University",
                    "type": "string",
                },
                {
                    "key": "area",
                    "description": "Field of study or major",
                    "example": "Computer Science",
                    "type": "string",
                },
                {
                    "key": "degree",
                    "description": "Type of degree earned",
                    "example": "Master of Science",
                    "type": "string",
                },
                {
                    "key": "location",
                    "description": "Location of the institution",
                    "example": "Stanford, CA",
                    "type": "string",
                },
                {
                    "key": "start_date",
                    "description": "Start date of education in YYYY-MM format",
                    "example": "2018-09",
                    "type": "string",
                },
                {
                    "key": "end_date",
                    "description": "End date of education in YYYY-MM format",
                    "example": "2020-06",
                    "type": "string",
                },
                {
                    "key": "highlights",
                    "description": "Notable achievements, activities, or courses",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "example": "Graduated with Honors (GPA: 3.9/4.0)",
                    },
                },
            ],
        },
    },
    {
        "key": "skills",
        "description": "Technical and professional skills",
        "type": "array",
        "items": {"type": "string", "example": "JavaScript"},
    },
    {
        "key": "languages",
        "description": "Languages spoken by the person",
        "type": "array",
        "items": {"type": "string", "example": "English (Native)"},
    },
    {
        "key": "certifications",
        "description": "Professional certifications",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "name",
                    "description": "Title of the certification",
                    "example": "AWS Certified Solutions Architect",
                    "type": "string",
                },
                {
                    "key": "date",
                    "description": "Date of certification in YYYY-MM format",
                    "example": "2022-03",
                    "type": "string",
                },
                {
                    "key": "summary",
                    "description": "Brief description of the certification",
                    "example": "An Amazon Web Services (AWS) certified solutions architect is a cloud network specialist who designs, creates, and maintains their employer's AWS-based services.",
                    "type": "string",
                },
            ],
        },
    },
    {
        "key": "publications",
        "description": "Publications authored by the person",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "title",
                    "description": "Title of the publication",
                    "example": "Advances in Machine Learning Algorithms",
                    "type": "string",
                },
                {
                    "key": "authors",
                    "description": "Authors of the publication",
                    "example": "John Doe, Jane Smith",
                    "type": "string",
                },
                {
                    "key": "journal",
                    "description": "Name of the journal or publisher",
                    "example": "Journal of Artificial Intelligence",
                    "type": "string",
                },
                {
                    "key": "date",
                    "description": "Publication date in YYYY-MM format",
                    "example": "2021-04",
                    "type": "string",
                },
                {
                    "key": "url",
                    "description": "URL to access the publication",
                    "example": "https://example.com/publication",
                    "type": "string",
                },
                {
                    "key": "doi",
                    "description": "Digital Object Identifier",
                    "example": "10.1000/xyz123",
                    "type": "string",
                },
            ],
        },
    },
    {
        "key": "projects",
        "description": "Personal or professional projects",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "name",
                    "description": "Name of the project",
                    "example": "Portfolio Website",
                    "type": "string",
                },
                {
                    "key": "summary",
                    "description": "Brief description of the project",
                    "example": "Personal website showcasing my work and skills",
                    "type": "string",
                },
                {
                    "key": "start_date",
                    "description": "Start date of the project in YYYY-MM format",
                    "example": "2021-06",
                    "type": "string",
                },
                {
                    "key": "end_date",
                    "description": "End date of the project in YYYY-MM format or 'present'",
                    "example": "2021-08",
                    "type": "string",
                },
                {
                    "key": "highlights",
                    "description": "Key features or achievements of the project",
                    "type": "array",
                    "items": {
                        "type": "string",
                        "example": "Implemented responsive design using React and Tailwind CSS",
                    },
                },
            ],
        },
    },
    {
        "key": "custom_sections",
        "description": "Additional sections in the resume",
        "type": "array",
        "items": {
            "type": "object",
            "properties": [
                {
                    "key": "title",
                    "description": "Title of the custom section",
                    "example": "Volunteer Experience",
                    "type": "string",
                },
                {
                    "key": "entries",
                    "description": "Entries in this custom section",
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": [
                            {
                                "key": "content",
                                "description": "Content of the entry, could be text or structured information",
                                "example": "Volunteer at Local Food Bank (2020-2022)",
                                "type": "string",
                            }
                        ],
                    },
                },
            ],
        },
    },
]
