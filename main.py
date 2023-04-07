import os
import requests
import time
import cv2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC

if __name__ == '__main__':

    url='http://127.0.0.1:7860'

    #檔案路徑
    Input=['C:/f_CPBL/原圖備份','C:/f_CPBL/Input_picture']
    Output=['C:/f_CPBL/Input_picture','C:/f_CPBL/deliberate_model','C:/f_CPBL/GTA_model','C:/f_CPBL/inkpunkDiffusion_model']
    file_name=['兄弟','味全','統一','富邦','樂天','隊徽']

    #模型名稱
    model_name=['deliberate_v2.safetensors [9aba26abdf]','realisticVisionV20_v20.safetensors [e6415c4892]','gta5ArtworkDiffusion_v1.ckpt [607aa02fb8]','inkpunkDiffusion_v2.ckpt [2182245415]']

    #Seed
    Seed_num=['1433591419','12345','21026525','2885656581']

    #跟源圖差多少
    Denoising_num=['0.49','0.2','0.45','0.575']

    #咒語
    Promts=['(masterpiece,pro artist,detailed,realistic),(picture should generated same color with input picture),Taiwan strong muscular man,heigh quality hair,dieselpunka1 man, male,portrait,(baseball player strong),heigh quality, ((((hdr)))), intricate scene, artstation, intricate details, vignette',
            'hat icon should same to origin picture and unity,gtav style,CPBL,Strong and handsome man,baseball player,perfect face, perfect black eyes,2D,same hair color to origin picture,high quality,8k,dslr',
            '(The face profile and hair style familiar with input picture),(snthwve style:1), (nvinkpunk:0.7),perfect face,drunken handsome strong baseball player,detailed hair,asian man,dark soft light, high detailed, 4k, RTX,hat only one color, paint splashes, splatter, outrun,shaded flat illustration, digital art, trending on artstation, highly detailed, fine detail, intricate']

    #不要做的咒語
    Negative_Prompts=['women ,child ,homo,deformed, bad anatomy, disfigured, poorly drawn face, mutation, mutated, extra limb, ugly, disgusting, poorly drawn hands,(missing limb), floating limbs, disconnected limbs, malformed hands, blurry, ((((mutated hands and fingers)))), watermark, watermarked, oversaturated, censored, distorted hands, amputation, missing hands, obese, doubled face, double hands',
                      '(tattoo on neck),different hat icon with input picture,woman, child, teen, kid,tattoo on neck and face, underage, deformed, ugly, hideous, lacklustre, malformed, glossy, doll, cgi, unrealistic, poorly drawn, bad quality, lowres, big tits, busty, huge breasts, duplicate, morbid, mutilated, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, poorly Rendered face, poorly drawn face, poor facial details, poorly drawn hands, poorly rendered hands, low resolution, bad composition, mutated body parts, blurry image, disfigured, oversaturated, bad anatomy, deformed body feature',
                      'women ,(tattoo),ugly face, clid,cartoon, 3d, ((disfigured)), ((bad art)), ((deformed)), ((poorly drawn)), ((extra limbs)), ((close up)), ((b&w)), weird colors, blurry']
    #控制參數調整

    Browser=webdriver.Chrome(service=Service("chromedriver.exe"))
    Browser.get(url)
    Browser.maximize_window()

    Wait=WebDriverWait(Browser,20)

    # 點擊img2img按鈕，該網站有用shadow-root，所以這裡用js取得位置
    Browser.implicitly_wait(3)
    Img_to_Img = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#tabs > div.flex.border-b-2.flex-wrap.dark\\\:border-gray-700 > button:nth-child(2)')")
    Img_to_Img.click()

    #調整參數
    Select_element=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#setting_sd_model_checkpoint > label > select')")
    Sel=Select(Select_element)
    Sel.select_by_value(model_name[0])

    Resize=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#resize_mode > div.flex.flex-wrap.gap-2 > label:nth-child(2) > span')")
    Resize.click()

    Denoising_Strength=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_denoising_strength > div.w-full.flex.flex-col > div > input')")
    Denoising_Strength.clear()
    Denoising_Strength.send_keys(Denoising_num[0])

    Seed=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_seed > label > input')")
    Seed.clear()
    Seed.send_keys(Seed_num[0])

    Prompt= Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_prompt > label > textarea')")
    Prompt.send_keys(Promts[0])

    Negative_Prompt=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_neg_prompt > label > textarea')")
    Negative_Prompt.send_keys(Negative_Prompts[0])

    # deliberate用
    Step=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_steps > div.w-full.flex.flex-col > div > input')")
    Step.clear()
    Step.send_keys('40')

    Sampling_Method=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_sampling > label > select')")
    Sampling_method=Select(Sampling_Method)
    Sampling_method.select_by_value('DPM++ 2M Karras')

    Cfg_scale=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_cfg_scale > div.w-full.flex.flex-col > div > input')")
    Cfg_scale.clear()
    Cfg_scale.send_keys('10.5')

    #GTA用
    # Step=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_steps > div.w-full.flex.flex-col > div > input')")
    # Step.clear()
    # Step.send_keys('40')
    #
    # Sampling_Method=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_sampling > label > select')")
    # Sampling_method=Select(Sampling_Method)
    # Sampling_method.select_by_value('DDIM')
    #
    # Cfg_scale=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_cfg_scale > div.w-full.flex.flex-col > div > input')")
    # Cfg_scale.clear()
    # Cfg_scale.send_keys('9')

    #修圖用
    # Script=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_script_container>#script_list > label > select')")
    # Script_select=Select(Script)
    # Script_select.select_by_value('SD upscale')
    #
    # time.sleep(2)
    # Scale=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#script_sd_upscale_scale_factor > div.w-full.flex.flex-col > div > input')")
    # Scale.clear()
    # Scale.send_keys('3')
    #
    # Upscaler=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#script_sd_upscale_upscaler_index > div.flex.flex-wrap.gap-2 > label:nth-child(6)')")
    # Upscaler.click()

    #inkpunkdiffusion用
    # Step=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_steps > div.w-full.flex.flex-col > div > input')")
    # Step.clear()
    # Step.send_keys('46')
    #
    # Sampling_Method=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_sampling > label > select')")
    # Sampling_method=Select(Sampling_Method)
    # Sampling_method.select_by_value('DPM++ 2M Karras')
    #
    # Cfg_scale=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_cfg_scale > div.w-full.flex.flex-col > div > input')")
    # Cfg_scale.clear()
    # Cfg_scale.send_keys('9.5')

    for name in file_name:
        Input_path=os.path.join(Input[1],name)
        Output_path=os.path.join(Output[1],name)
        Jpg_files = os.listdir(Input_path)
        Jpg_files.sort(key=lambda x:int(x.split("_")[0]))
        print(Jpg_files)
        for i in range(len(Jpg_files)):
            Path = os.path.join(Input_path, Jpg_files[i])
            print(Path)
            # 修圖用
            # img = cv2.imread(Path)
            # if img.shape[0] <= 425 and img.shape[1] <= 425:

            #上傳圖片
            Upload_picture = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_image > div.h-60 > div > input')")
            Upload_picture.send_keys(Path)
            time.sleep(3)

            #生成圖片
            Generate=Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_generate')")
            Generate.click()
            time.sleep(10)

            #取得圖片
            Download_picture = Wait.until(lambda Browser: Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_gallery > div.overflow-y-auto.h-full.p-2.min-h-\\\[350px\\\].max-h-\\\[55vh\\\].xl\\\:min-h-\\\[450px\\\] > div > button > img')"))
            Picture_src = Download_picture.get_attribute("src")
            print(Picture_src)
            Img=requests.get(Picture_src)
            print(Img)
            with open(os.path.join(Output_path,Jpg_files[i]),'wb') as f:
                f.write(Img.content)

            time.sleep(5)
            #關圖片
            Close_picture = Browser.execute_script("return document.querySelector('body > gradio-app').shadowRoot.querySelector('#img2img_image > div.h-60.bg-gray-200 > div > div > button:nth-child(2)')")
            Close_picture.click()

    time.sleep(5)
    Browser.quit()
