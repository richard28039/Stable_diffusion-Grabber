import os
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

import time

if __name__ == '__main__':

    #Stable Difussion
    url='http://127.0.0.1:7860'

    #檔案路徑
    Input=r"C:\f_CPBL\Input_picture"
    Output=r"C:\f_CPBL\Output_picture"
    file_name=['兄弟','味全','統一','富邦','樂天','隊徽']

    Browser=webdriver.Chrome(service=Service("chromedriver.exe"))
    Browser.get(url)
    Browser.maximize_window()

    # 點擊img2img按鈕，該網站有用shadow-root，所以這裡用js取得位置
    Browser.implicitly_wait(3)
    Img_to_Img = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#tabs > div.flex.border-b-2.flex-wrap.dark\\\:border-gray-700 > button:nth-child(2)')")
    Img_to_Img.click()

    #調整參數
    Select_element=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#setting_sd_model_checkpoint > label > select')")
    Sel=Select(Select_element)
    Sel.select_by_value("v1-5-pruned-emaonly.safetensors [6ce0161689]")

    Crop_and_Resize=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#resize_mode > div.flex.flex-wrap.gap-2 > label:nth-child(2)')")
    Crop_and_Resize.click()

    Denoising_Strength=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_denoising_strength > div.w-full.flex.flex-col > div > input')")
    Denoising_Strength.clear()
    Denoising_Strength.send_keys('0.3')

    Seed=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_seed > label > input')")
    Seed.clear()
    Seed.send_keys('12345')

    Prompt= Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_prompt > label > textarea')")
    Prompt.send_keys('The face feature and skin color should similar to origin, male,same hair and beard color , 8k uhd, dslr, soft lighting, high quality, film grain, Fujifilm XT3')

    Negative_Prompt=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_neg_prompt > label > textarea')")
    Negative_Prompt.send_keys('(semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck,nose ring')

    for name in file_name:
        Input_path=os.path.join(Input,name)
        Output_path=os.path.join(Output,name)
        Jpg_files = os.listdir(Input_path)
        Jpg_files.sort(key=lambda x:int(x.split("_")[0]))
        print(Jpg_files)
        for i in range(len(Jpg_files)):
            Path = os.path.join(Input_path, Jpg_files[i])
            print(Path)

            #上傳圖片
            Upload_picture = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_image > div.h-60 > div > input')")
            Upload_picture.send_keys(Path)

            #生成圖片
            Generate=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_generate')")
            Generate.click()
            time.sleep(5)

            #取得圖片
            Download_picture=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_gallery > div.overflow-y-auto.h-full.p-2.min-h-\\\[350px\\\].max-h-\\\[55vh\\\].xl\\\:min-h-\\\[450px\\\] > div > button > img')")
            Picture_src=Download_picture.get_attribute("src")
            rem_src=Picture_src
            print(Picture_src)
            Img=requests.get(Picture_src)
            print(Img)
            with open(os.path.join(Output_path,Jpg_files[i]),'wb') as f:
                f.write(Img.content)

            #關圖片
            Close_picture = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_image > div.h-60.bg-gray-200 > div > div > button:nth-child(2)')")
            Close_picture.click()

    time.sleep(5)
    Browser.quit()
