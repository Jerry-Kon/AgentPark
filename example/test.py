from agentpark.agentbase import AgentPark
from agentpark.config.model import MODEL_API


if __name__ == "__main__":
    api_list = [MODEL_API[0], MODEL_API[1]]
    park = AgentPark.register(api_list)
    output = park.work("开发一个web端的贪吃蛇小游戏程序")
