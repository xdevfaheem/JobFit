# core llm call logic
import json
import os

import litellm
from pydantic import BaseModel

litellm.enable_json_schema_validation = True


def call(system_prompt: str, user_prompt: str, output_schema: BaseModel):
    response = litellm.completion(
        model=os.environ["LLM_ID"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=1.3,
        reasoning_effort="medium",
        response_format=output_schema,
        modalities="text",
        api_key=os.environ["LLM_API_KEY"],
    )

    json_out = json.loads(response.choices[0].message.content.strip())
    return output_schema(**json_out)
