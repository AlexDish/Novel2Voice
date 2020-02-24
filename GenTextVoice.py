from aip import AipSpeech
import os
import re


APPID = '×××'
APIKEY = '×××'
SECRETKEY = '×××'

ARTICLE_PATH = 'Articles'
SAVE_VOICE_PATH = 'Voice'
VOICE_TYPE = 'mp3'

START_ID = '-1'

def getSpeechObj(AppID=APPID, APIKey=APIKEY, SecretKey=SECRETKEY):
    speecher = AipSpeech(AppID, APIKey, SecretKey)
    return speecher

def get_one_file(path):
    for root, dirs, file_names in os.walk(path):
        file_names.sort()
        for file_name in file_names:
            # 多加一个因为停止后重新跑的开始ID
            file_id = re.findall('(\d+)_', file_name)[0]
            if int(START_ID) < int(file_id):
                article_data = get_one_article(file_name)
                yield article_data, file_name
            # exit()

def get_one_article(file_name):
    print(file_name)
    article_data = ''
    with open('./'+ARTICLE_PATH+'/'+file_name, 'r', encoding='utf-8') as f:
        article_data = f.read()
    return article_data

def do_synthesis(speecher, text):
    # 这里做一个对text长度进行切片1024以内
    texts = text.split('\n')
    text_list = []
    text_temp = ''
    for text_i in texts:
        if len(text_temp) < 800:
            text_temp = ''.join([text_temp, text_i])
        else:
            text_list.append(text_temp)
            text_temp = ''
    text_list.append(text_temp)
    for i, text_slice in enumerate(text_list):
        voice_data = speecher.synthesis(text_slice, options={'per': 4, 'spd': 3})
        yield voice_data, i

def save_voice_file(voice_data, path, f_name, slice_id, types='mp3'):
    if not isinstance(voice_data, dict):
        with open('./'+path+'/'+f_name[:-4]+'_'+str(slice_id)+'.'+types, 'wb') as f:
            f.write(voice_data)
    else:
        print(voice_data)
        exit()

"""
if __name__ == '__main__':
    speecher = getSpeechObj()
    for art, f_name in get_one_file(ARTICLE_PATH):
        for voice, i in do_synthesis(speecher, art):
            save_voice_file(voice, SAVE_VOICE_PATH, f_name, i)
"""
if __name__ == '__main__':
    speecher = getSpeechObj()
    for art, f_name in get_one_file(ARTICLE_PATH):
        with open('./'+SAVE_VOICE_PATH+'/'+f_name[:-3]+VOICE_TYPE, 'wb') as f:
            for voice, i in do_synthesis(speecher, art):
                if not isinstance(voice, dict):
                    f.write(voice)
                else:
                    print(voice)
                    print('Error f_name: {}!'.format(f_name))
