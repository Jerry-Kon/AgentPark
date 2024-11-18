import requests
import uuid
from agentpark.config.model import ZHIPU_KEY


def zhipu_search(para):
    keyword = para["keywords"]
    msg = [
        {
            "role": "user",
            "content": keyword
        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': ZHIPU_KEY},
        timeout=300
    )

    search_str = ""
    resp_list = resp.json()["choices"][0]["message"]["tool_calls"][1]["search_result"]
    for i in range(len(resp_list)):
        search_str += "### 资讯{}：\n{}\n".format(i, resp_list[i]["content"])
        
    return search_str
        

if __name__ == '__main__':
    zhipu_search("24年美国总统大选")