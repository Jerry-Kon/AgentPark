from agentpark.tools.tools import zhipu_search
from openai import OpenAI
import json
from agentpark.utils import json_extract
from agentpark.config.model import MODEL_API

API_KEY = MODEL_API[1]["api_key"]
API_URL = MODEL_API[1]["api_base"]
MODEL_NAME = MODEL_API[1]["name"]


tools_dict = {"zhipu_search": zhipu_search}


def use_tools(chat_result):
    api_json = json_extract(chat_result)
    api_name = api_json["function_name"]
    api_para = api_json["function_params"]
    func = tools_dict[api_name]
    result = func(api_para)
    return result


def llm_chat(system_prompt, user_prompt):
    clinet = OpenAI(
        api_key=API_KEY,
        base_url=API_URL,
    )
    result = clinet.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {"role": "user", "content": user_prompt},
        ],
    )
    return result.choices[0].message.content


system_prompt = """
## 任务
你在运行一个“思考”，“工具调用”，“响应”循环。每次只运行一个阶段。
1.“思考”阶段：你要仔细思考用户的问题
2.“工具调用阶段”：选择可以调用的工具，并且输出对应工具需要的参数
3.“响应”阶段：根据工具调用返回的结果，回复用户问题。

## 工具
### 工具1
用途：用于搜索天气状况
API请求体结构：
{
	"function_name":"get_weather",
	"function_params":{
		"location": "" //地点
	}
}
### 工具2
用途：用于搜索新闻资讯
API请求体结构：
{
	"function_name":"zhipu_search",
	"function_params":{
		"keywords": "" //搜索关键词
	}
}

## Example
question：天津的天气怎么样？
thought：我应该调用工具查询天津的天气情况
Action：
```json
{   
	"function_name":"get_weather"
	"function_params":{
		"location":"天津"
	}
}
```
调用Action的结果：“天气晴朗”
Answer:天津的天气晴朗
"""

query = input("输入问题：")
res = llm_chat(system_prompt, query)
print(res)
func_reault = use_tools(res)
print("-----------------")
print(func_reault)
user_prompt = (
    "question：{}\n".format(query)
    + "Action：\n{}\n".format(res)
    + "调用Action的结果：\n{}\n".format(func_reault)
)
result = llm_chat(system_prompt, user_prompt)

print("-----------------")
print(result)
