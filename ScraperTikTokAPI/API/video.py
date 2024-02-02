from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json


class Video:
    def VideoDetail(Url):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(Url)
            html_content = page.content()
            soup = BeautifulSoup(html_content, 'html.parser')
            script_content = soup.find('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'}).string
            browser.close()
        json_obj = json.loads(script_content)
        # Buscar las estadísticas específicas
        default_scope = json_obj.get('__DEFAULT_SCOPE__', {})
        video_detail = default_scope.get('webapp.video-detail', {})
        itemInfo = video_detail.get('itemInfo', {})
        itemStruct = itemInfo.get('itemStruct', {})
        id_video = itemStruct.get('id', "")
        desc_video = itemStruct.get('desc', "")
        desc_createTime = itemStruct.get('createTime', "")
        author = itemStruct.get('author', {})
        # Verificar si 'author' es un diccionario antes de intentar extraer claves
        if isinstance(author, dict):
            selected_author= {
                'id': author.get('id', ''),
                'shortId': author.get('shortId', ''),
                'uniqueId': author.get('uniqueId', ''),
                'nickname': author.get('nickname', ''),
                'avatarLarger': author.get('avatarLarger', ''),
                'avatarMedium': author.get('avatarMedium', ''),
                'avatarThumb': author.get('avatarThumb', ''),
                'signature': author.get('signature', ''),}
        else:
            selected_author = {
                'id': '', 
                'shortId': '', 
                'uniqueId': '', 
                'nickname': '', 
                'avatarLarger': '', 
                'avatarMedium': '', 
                'avatarThumb': '', 
                'signature': ''}
        music = itemStruct.get('music', {})
        # Verificar si 'music' es un diccionario antes de intentar extraer claves
        if isinstance(music, dict):
            selected_music= {
                'id': music.get('id', ''),
                'title': music.get('title', ''),
                'coverLarge': music.get('coverLarge', ''),
                'coverMedium': music.get('coverMedium', ''),
                'coverThumb': music.get('coverThumb', ''),
                'authorName': music.get('authorName', ''),
                'original': music.get('original', ''),
                'duration': music.get('duration', ''),
                }
        else:
            selected_music = {
                'id': '', 
                'title': '', 
                'coverLarge': '', 
                'coverMedium': '', 
                'coverThumb': '', 
                'authorName': '', 
                'original': '', 
                'duration': ''}
        stats = itemStruct.get('stats', {})
        data = {'data': {'id_video': id_video, 'desc_video': desc_video, 'desc_createTime': desc_createTime,
                     'author': selected_author, 'music': selected_music, 'metrics': stats}}   
        return data
    def restar(a,b):
        return a - b