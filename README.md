<!--
 * @Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @Date: 2025-01-27 10:14:40
 * @LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
 * @LastEditTime: 2025-02-02 09:38:53
 * @FilePath: \AI-chat\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# AI 聊天机器人 #

## 说明
基于 llmstudio 以及vosk/google speech recognition的对话聊天机器人


## 配置说明 ##
1. 下载并安装配置好 llmstudio，并在 `开发者`选项卡中启动llm server，修改[](./main.py) 15行，改成你自己的port，同时请下载好模型:`llama-3.2-3b-instruct`(也可以用其他模型，修改这里的model key就可以)
2. 安装 `requirement.txt` 中的依赖包
3. 下载并解压到当前目录： [vosk语音识别模型](https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip), 也支持其他模型，但需要修改[reader.py](./reader.py)中vosk reader的 `MODEL_PATH`

## 使用说明 ##
```text
 python3.13.exe .\main.py --help
usage: main.py [-h] [--use_google]

AI聊天机器人

options:
  -h, --help    show this help message and exit
  --use_google  OpenAI API key
```
默认使用vosk本地语音识别，加上--use_google 使用谷歌语音识别（需要科学上网）  



   