import json5

def json_extract(llm_out: str) -> dict:
    json_str = llm_out.split("```json\n")[1].split("\n```")[0]
    llm_dict = json5.loads(json_str)
    return llm_dict