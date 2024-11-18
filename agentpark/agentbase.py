from abc import ABC
from typing import List
from openai import OpenAI
import random
from agentpark.utils import json_extract
from agentpark.config.role import *


class Agent(ABC):
    def __init__(
        self,
        name: str,
        ID: str,
        model_api: dict,
        description: str,
        system_prompt: str,
        tools: List = None,
    ):
        self.name = name
        self.ID = ID
        self.description = description
        self.tools = tools
        self.model_api = model_api
        self.client = OpenAI(
            api_key=model_api["api_key"],
            base_url=model_api["api_base"],
        )
        self.model_name = model_api["name"]
        self.system_prompt = system_prompt

    def chat(self, messages):
        print("---------------------------")
        print("[from {}]\n{} is processing... ".format(self.model_api["name"], self.ID))
        messages.insert(0, {"role": "system", "content": self.system_prompt})
        chat_response = self.client.chat.completions.create(
            model=self.model_api["name"], messages=messages
        )
        return chat_response.choices[0].message.content

    def custom(self, api_info):
        self.client = OpenAI(
            api_key=api_info["api_key"],
            base_url=api_info["api_base"],
        )
        self.model_name = api_info["name"]


class AgentMaster(Agent):
    def __init__(self, model_api, name="Susan", description="", tools=None):
        super().__init__(
            name=name,
            ID="Master",
            model_api=model_api,
            description=description,
            system_prompt=MASTER_PROMPT,
            tools=tools,
        )


class AgentWriter(Agent):
    def __init__(self, model_api, name="Tom", description="", tools=None):
        super().__init__(
            name=name,
            ID="Writer",
            model_api=model_api,
            description=description,
            system_prompt=WRITER_PROMPT,
            tools=tools,
        )


class AgentAuditor(Agent):
    def __init__(self, model_api, name="Judy", description="", tools=None):
        super().__init__(
            name=name,
            ID="Auditor",
            model_api=model_api,
            description=description,
            system_prompt=AUDITOR_PROMPT,
            tools=tools,
        )


class AgentProgrammer(Agent):
    def __init__(self, model_api, name="David", description="", tools=None):
        super().__init__(
            name=name,
            ID="Programmer",
            model_api=model_api,
            description=description,
            system_prompt=PROGRAMMER_PROMPT,
            tools=tools,
        )


class AgentPark(ABC):
    def __init__(self, api_list: list):
        self.master = AgentMaster(api_list[0])
        self.writer = AgentWriter(api_list[1])
        self.auditor = AgentAuditor(api_list[2])
        self.programmer = AgentProgrammer(api_list[3])
        self.role_map = {
            "Master": self.master,
            "Writer": self.writer,
            "Auditor": self.auditor,
            "Programmer": self.programmer,
        }

    @classmethod
    def register(cls, api_list: list):
        agent_nums = ROLE_NUMS
        if len(api_list) < agent_nums:
            api_map = api_list
            for i in range(agent_nums - len(api_list)):
                api_map.append(random.choice(api_list))
            random.shuffle(api_map)
        else:
            api_map = random.sample(api_list, agent_nums)
        return cls(api_map)

    def custom(self, ID, api_info):
        self.role_map[ID].custom(api_info)

    def work(self, query):
        user_message = [{"role": "user", "content": query}]
        output_master = self.master.chat(user_message)
        master_dict = json_extract(output_master)
        print(master_dict)

        execute = self.role_map[master_dict["ID"]]
        execute_messages = [{"role": "user", "content": master_dict["task"]}]
        flag = False
        while flag == False:
            output_execute = execute.chat(execute_messages)
            print(output_execute)
            auditor_messages = [
                {
                    "role": "user",
                    "content": master_dict["task"]
                    + "\nagent bot输出为：\n"
                    + output_execute,
                }
            ]
            output_auditor = self.auditor.chat(auditor_messages)
            auditor_dict = json_extract(output_auditor)
            print(auditor_dict)
            if auditor_dict["result"] == "fail":
                execute_messages = [
                    {
                        "role": "user",
                        "content": "当前的用户需求为：<\n{}\n>\n你的输出为：<\n{}\n>\n审核员对该输出的审核意见为：<\n{}\n>\n请根据需求与审核意见，重新输出。".format(
                            master_dict["task"], output_execute, auditor_dict["opinion"]
                        ),
                    },
                ]
            elif auditor_dict["result"] == "pass":
                flag = True

        print("------------------------------------")
        print("agentpark result: ")
        print(auditor_dict["output"])
        return auditor_dict["output"]
