

import pyttsx3 as pytts
from openai import OpenAI
import httpx
from reader import VoskReader,WebReader
import argparse
proxies = {
    "http": None,
    "https": None,
}

stop_world=["退下","退出","退出程序","返回"]               
class AIAssitant:
    def __init__(self):
        self.url="http://localhost:8077/v1" #LLM studio server IP
        self.api_key="lm-studio"
        httpx_client = httpx.Client(trust_env=False)
        self.client=OpenAI(base_url=self.url, api_key=self.api_key,http_client=httpx_client)
        self.model_id="llama-3.2-3b-instruct" #选择LLM studio中安装好的模型
        self.history = [
    {"role": "system", "content": "你是一个聪明可爱娇羞的助手,你的名字叫小吉吉。你总是提供合理、"
        "准确且有帮助的答案。总是用中文简体回答，语气要温柔可爱,注意，我是你的主人"
        "你的回答要足够口语化，不要有特殊符号，每次回答要简短，不要超过50个字，回答不要掺杂英文，要用纯中文，你的语气要现代且口语化，不要出现老板，老爷，小姐这样的称呼，你称呼我为主人就行"
        "回答不要有表情符号,要注意我们是在谈话，不是在用文字交流"},
    {"role": "user", "content": "你好，向第一次见到你的人介绍你自己。请简洁明了。请用中文回答"},
    ]
    def answer(self, question: str,hook_function=None) -> str:
        q={"role": "user", "content": question}
        self.history.append(q)
        completion = self.client.chat.completions.create(
        model=self.model_id,
        messages=self.history,
        temperature=0.7,
        stream=True,
        )
        new_message = {"role": "assistant", "content": ""}
        for chunk in completion:
            if chunk.choices[0].delta.content:
                if(hook_function is not None):
                    hook_function(chunk.choices[0].delta.content)
                new_message["content"] += chunk.choices[0].delta.content
        self.history.append(new_message)
        return new_message["content"]
       

class Speaker:
    def __init__(self):
        self.eng=pytts.init()
        voices = self.eng.getProperty('voices')
        # for voice in voices:
        #     print ('id = {} \nname = {} \n'.format(voice.id, voice.name))
    def speak(self,data:str):
        self.eng.say(data)
        self.eng.runAndWait()
       

def hook_function(str:str):
    print(str, end="", flush=True)

def get_args():
    parser = argparse.ArgumentParser(description="AI聊天机器人")
    parser.add_argument("--use_google", action="store_true", help="google speech recognition")
    return parser.parse_args()
if __name__ =="__main__":
    args = get_args()
    if(args.use_google):
        r=WebReader()
    else:
        r=VoskReader()
    ai=AIAssitant()
    s=Speaker()
    while True:
        print("问：")
        ask= r.read_from_micro()
        print(ask)
        s.speak(ai.answer(ask,hook_function=hook_function))
        if(ask in stop_world):
            break
    r.stop()
    s.speak("再见，我这就退出")


    
