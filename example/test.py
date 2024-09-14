from agentpark.agentbase import AgentPark
from agentpark.config.model import MODEL_API


if __name__ == "__main__":
    api_list = [MODEL_API[0], MODEL_API[1]]
    park = AgentPark.register(api_list)
    park.work("开发一个web端的贪吃蛇小游戏程序")


# import random
# api_list = [MODEL_API[0], MODEL_API[1]]
# agent_nums = 4
# if len(api_list) < agent_nums:
#     api_map = api_list
#     for i in range(agent_nums - len(api_list)):
#         api_map.append(random.choice(api_list))
#     random.shuffle(api_map)
# else:
#     api_map = random.sample(api_list, agent_nums)

# print(api_map)