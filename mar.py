from selenium import webdriver
from variables import variables
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import shutil
import ast
import schedule

def download_episode():
    op = webdriver.ChromeOptions()
    op.add_argument('headless')

    refer = "https://www.fox.com.tr/Evlilik-Hakkinda-Her-Sey/bolumler"
    save_path = variables()[0]
    
    driver = webdriver.Chrome(options=op)
    driver.get("https://www.fox.com.tr/Evlilik-Hakkinda-Her-Sey/bolumler")
    body = driver.find_element(By.TAG_NAME,"body")
    main = body.find_element(By.TAG_NAME,"main")
    wrapper = main.find_element(By.CLASS_NAME, "wrapper")
    video_player = wrapper.find_element(By.CLASS_NAME,"video-player")
    v_inner = video_player.find_element(By.ID, "video-player-container-inner")
    api_html = v_inner.find_element(By.ID, "foxPlayer_html5_api")

    source_link_for_download = api_html.find_element(By.TAG_NAME,"source").get_attribute("src")
    
    columns = wrapper.find_element(By.CLASS_NAME, "columns")
    
    video = columns.find_element(By.CLASS_NAME, "video")
    
    description = video.find_element(By.TAG_NAME, "script").get_attribute('innerHTML')
    dictionary_description = ast.literal_eval(description)
    last_episode_number = dictionary_description['episodeNumber']
    episode_description = dictionary_description['description']
    


    hold = "hold.txt"
    list_episodes = os.path.join(save_path,hold)
    f = open(list_episodes,"r")
    episodes = (f.read()).split()
    f.close()


    source_link_for_download = "\'" + source_link_for_download + "\'"
    ar1 = "youtube-dl --referer https://www.fox.com.tr/Evlilik-Hakkinda-Her-Sey/bolumler "
    command =  ar1 + source_link_for_download
    os.chdir(save_path)
    count = 0
    for x in episodes:
        if x == last_episode_number:
            count = 1
            
    if count == 1:
        print("video is already downloaded, program is over")
        exit()
    else:
        os.system(command)
        

        current_path = variables()[1]
        home_path = variables()[2]

        file_name = last_episode_number+"_aciklama.txt"
        complete_name = os.path.join(save_path,file_name)
        f = open(complete_name,"a")
        f.write(episode_description)
        f.close()

        f = open(list_episodes,"a")
        f.write(last_episode_number)
        f.close()


        os.rename(save_path+"/playlist-playlist.mp4", current_path+ "/"+last_episode_number+".mp4")
        os.makedirs(current_path+"/"+last_episode_number,exist_ok=True)
        os.replace(current_path+"/"+last_episode_number+"_aciklama.txt",current_path+"/"+last_episode_number+"/"+last_episode_number+"_aciklama.txt")
        os.replace(current_path+"/"+last_episode_number+".mp4",current_path+"/"+last_episode_number+"/"+last_episode_number+".mp4")
        
        new_path =  current_path + "/series"
        
        try :
            os.makedirs(new_path,exist_ok=True)
        except OSError as error:
            print("fail for creating directory")


        os.replace(current_path+"/"+last_episode_number, new_path+"/"+last_episode_number)

    




download_episode()




