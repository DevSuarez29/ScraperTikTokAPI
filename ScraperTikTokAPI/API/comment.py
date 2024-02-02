import requests
import urllib.parse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json

class Comment:
    @staticmethod
    def comments(url):
        all_comments = []  # Lista para almacenar todos los comentarios
        has_more = 1
        cursor = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        while has_more:
            url_api = 'https://tiktok-signature.onrender.com/api/signature/' # API url
            video_id = urllib.parse.urlparse(url).path.split('/')[-1]
            data = {
                'url': f'https://www.tiktok.com/api/comment/list/?WebIdLastTime=1698876249&aid=1988&app_language=ja-JP&app_name=tiktok_web&aweme_id={video_id}&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F121.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=20&current_region=JP&cursor={cursor}&device_id=7296617830668862978&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=2&is_fullscreen=false&is_non_personalized=false&is_page_visible=true&os=windows&priority_region=CO&referer=&region=CO&screen_height=768&screen_width=1366&tz_name=America%2FBogota&webcast_language=en', # TikTok url want to sign
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36', # Paste your browser userAgent
                'version': '2', # choice 1 or 2
                'Token': 'main-CPO@Signature', # API Token
                'data': '', # TikTok request body
                'Bogus': True, # make True to generate
                'msToken': True, # ...
                '_signature': True # ...
            }
            response = requests.post(url=url_api, data=data).json()
            new_url = response['new_url']
            print(response)
            driver = webdriver.Chrome()
            driver.get(new_url)
            html_content = driver.page_source
            driver.quit()
            soup = BeautifulSoup(html_content, 'html.parser')
            pre_tag = soup.find('pre')
            content_inside_pre = pre_tag.text if pre_tag else {}
            
            # Parse content_inside_pre as JSON and get 'comments' array
            content_json = json.loads(content_inside_pre)
            comments = content_json.get('comments', [])

            # Agregar los comentarios a la lista acumulativa
            all_comments.extend(comments)

            # Incrementar el valor de count para la próxima iteración
            cursor += 20

            # Actualizar el valor de has_more
            has_more = content_json.get('has_more', 0)

        return all_comments
    
    def reply(comment_id):
        all_reply = []  # Lista para almacenar todos los comentarios
        has_more = 1
        cursor = 0
        while has_more:
            url = f"https://www.tiktok.com/api/comment/list/reply/?aid=1988&app_language=ja-JP&app_name=tiktok_web&browser_language=en-US&browser_name=Mozilla&browser_online=true&browser_platform=Win32&browser_version=5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F120.0.0.0%20Safari%2F537.36&channel=tiktok_web&comment_id={comment_id}&cookie_enabled=true&count=3&current_region=JP&cursor={cursor}&device_id=7296617830668862978&device_platform=web_pc&enter_from=tiktok_web&focus_state=true&fromWeb=1&from_page=video&history_len=2&is_fullscreen=false&is_page_visible=true&item_id=7302561785729617157&os=windows&priority_region=CO&referer=&region=CO&screen_height=768&screen_width=1366&tz_name=America%2FBogota&webcast_language=en"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            }
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()  # Lanza una excepción para códigos de estado no exitosos

                data = response.json()
                reply = data.get('comments', [])
                all_reply.extend(reply)

            except requests.exceptions.HTTPError as errh:
                all_reply.extend({})

            except requests.exceptions.ConnectionError as errc:
                all_reply.extend({})

            except requests.exceptions.Timeout as errt:
                all_reply.extend({})

            except requests.exceptions.RequestException as err:
                all_reply.extend({})

            cursor += 20

            has_more = data.get('has_more', 0)

        return all_reply