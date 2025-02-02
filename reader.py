'''
Author: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
Date: 2025-01-26 11:04:14
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2025-01-27 10:49:22
FilePath: \AI-chat\reader.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import vosk
import pyaudio
import numpy as np
import json
import speech_recognition as sr

class WebReader:
    #基于google的语音识别服务，需要翻墙，但是识别效果较好
    def __init__(self):  
        self.r=sr.Recognizer()
        
    def read_from_micro(self):
        # 使用默认麦克风作为音频来源
        while True:
            with sr.Microphone() as source:
                print("问：",end="")
                audio = self.r.listen(source)
            
                try:
                    # 使用Google Web Speech API进行识别
                    text = self.r.recognize_google(audio, language='zh-CN')
                    return text
                except sr.UnknownValueError:
                    print("再讲一次:")
                    continue
                except sr.RequestError as e:
                    raise f"Could not request results from Google Speech Recognition service; {e}"
    def stop(self):
        return            


class VoskReader:
    def __init__(self,
                 MODEL_PATH = "vosk-model-small-cn-0.22",
                 VOLUME_THRESHOLD = 100,
                 SILENCE_THRESHOLD = 5):
        
        # 模型路径
        self.MODEL_PATH = MODEL_PATH  # 修改为你的模型路径

        # 初始音量阈值
        self.VOLUME_THRESHOLD = VOLUME_THRESHOLD  # 可以根据实际情况调整
        # 静默时间阈值（秒）
        self.SILENCE_THRESHOLD = SILENCE_THRESHOLD  # 静默5秒后停止录音

        # 加载模型
        self.model = vosk.Model(self.MODEL_PATH)

        # 初始化识别器
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

        # 初始化PyAudio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        
    def read_from_micro(self):
        self.stream.start_stream()
        # 用于记录静默时间
        silence_time = 0.0

        while True:
            data = self.stream.read(4000)
            if len(data) == 0:
                break

            # 将音频数据转换为numpy数组
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # 计算音量
            volume = np.abs(audio_data).mean()
            # 检查音量是否低于阈值
            if volume < self.VOLUME_THRESHOLD:
                silence_time += 0.25  # 假设每次循环间隔为0.25秒
                if silence_time >= self.SILENCE_THRESHOLD:
                    #print("请说话")
                    continue
            else:
                silence_time = 0.0  # 重置静默时间

            if self.rec.AcceptWaveform(data):
                result = self.rec.Result()
                result_dict = json.loads(result)
                text = result_dict.get("text", "")
                text=text.replace(" ","")
                if text:
                    self.stream.stop_stream()
                    return text
                   
    def stop(self):
        # 停止流
       
        self.stream.close()
        self.p.terminate()
    
if __name__=="__main__":
    reader = VoskReader() #
    print(reader.read_from_micro())
    reader.stop()