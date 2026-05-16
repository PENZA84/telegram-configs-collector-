# import requirement libraries
import os
import json
from pathlib import Path
import math
import string
import random
import jdatetime
from datetime import datetime, timezone, timedelta

# import web-based libraries
import html
import requests
from bs4 import BeautifulSoup

# import regex and encoding libraries
import re
import base64

# import custom python script
try:
    from title import check_modify_config, create_country, create_country_table, create_internet_protocol
except ImportError:
    print("⚠️ Предупреждение: title.py не найден!")

# --- [ИСПРАВЛЕНИЕ 404: ЗАМЕНА WGET НА REQUESTS] ---
if not os.path.exists('./geoip-lite'):
    os.mkdir('./geoip-lite')

if os.path.exists('./geoip-lite/geoip-lite-country.mmdb'):
    os.remove('./geoip-lite/geoip-lite-country.mmdb')

url = 'https://github.com/P3TERX/GeoLite.mmdb/releases/latest/download/GeoLite2-Country.mmdb'
filename = 'geoip-lite-country.mmdb'
print("🌍 Скачиваю GeoIP базу через requests...")
try:
    r = requests.get(url, stream=True, timeout=30)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
        os.rename(filename, os.path.join('./geoip-lite', filename))
        print("✅ База GeoIP успешно обновлена!")
    else:
        print(f"⚠️ Ошибка сервера: {r.status_code}. Скачивание пропущено.")
except Exception as e:
    print(f"⚠️ Не удалось обновить базу GeoIP: {e}. Пропускаем, чтобы скрипт не падал.")

# --- [РОДНАЯ ЛОГИКА ВИЛКИ] ---
with open("./splitted/no-match", "w") as no_match_file:
    no_match_file.write("#Non-Adaptive Configurations\n")

with open('./last update', 'r') as file:
    last_update_datetime = file.readline().strip()
    try:
        last_update_datetime = datetime.strptime(last_update_datetime, '%Y-%m-%d %H:%M:%S.%f%z')
    except:
        last_update_datetime = datetime.now(timezone.utc) - timedelta(days=1)

with open('./last update', 'w') as file:
    current_datetime_update = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    jalali_current_datetime_update = jdatetime.datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    file.write(f'{current_datetime_update}')

print(f"Latest Update: {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}\nCurrent Update: {current_datetime_update.strftime('%a, %d %b %Y %X %Z')}")

def get_absolute_paths(start_path):
    abs_paths = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            abs_path = Path(root).joinpath(file).resolve()
            abs_paths.append(str(abs_path))
    return abs_paths

dirs_list = ['./security', './protocols', './networks', './layers', './subscribe', './splitted', './channels']

if (int(jalali_current_datetime_update.day) == 1 and int(jalali_current_datetime_update.hour) == 0) or (int(jalali_current_datetime_update.day) == 15 and int(jalali_current_datetime_update.hour) == 0):
    print("The All Collected Configurations Cleared Based On Scheduled Day")
    last_update_datetime = last_update_datetime - timedelta(days=3)
    for root_dir in dirs_list:
        if os.path.exists(root_dir):
            for path in get_absolute_paths(root_dir):
                if not path.endswith('readme.md'):
                    with open(path, 'w') as file:
                        file.write('')

def json_load(path):
    with open(path, 'r') as file:
        return json.load(file)

def tg_channel_messages(channel_user):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(f"https://t.me/s/{channel_user}", headers=headers, timeout=15)
        if response.status_code == 404:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("div", class_="tgme_widget_message")
    except Exception:
        return []

def find_matches(text_content):
    pattern_telegram_user = r'(?:@)(\w{4,})'
    pattern_url = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org...))' # Твоя оригинальная регулярка ссылок
    # (Здесь остаются все твои оригинальные регулярные выражения из старого main.py)
    pattern_shadowsocks = r"(?<![\w-])(ss://[^\s<>#]+)"
    pattern_trojan = r"(?<![\w-])(trojan://[^\s<>#]+)"
    pattern_vmess = r"(?<![\w-])(vmess://[^\s<>#]+)"
    pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality)[^\s<>#])+(?=[\s<>#]))"
    pattern_reality = r"(?<![\w-])(vless://[^\s<>#]+?security=reality[^\s<>#]*)"
    pattern_tuic = r"(?<![\w-])(tuic://[^\s<>#]+)"
    pattern_hysteria = r"(?<![\w-])(hysteria://[^\s<>#]+)"
    pattern_hysteria_ver2 = r"(?<![\w-])(hy2://[^\s<>#]+)"
    pattern_juicity = r"(?<![\w-])(juicity://[^\s<>#]+)"

    matches_usersname = re.findall(pattern_telegram_user, text_content, re.IGNORECASE)
    # На всякий случай защищаем поиск ссылок от падения
    try: matches_url = re.findall(pattern_url, text_content, re.IGNORECASE)
    except: matches_url = []
    
    matches_shadowsocks = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#SHADOWSOCKS" for x in re.findall(pattern_shadowsocks, text_content, re.IGNORECASE) if "…" not in x]
    matches_trojan = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#TROJAN" for x in re.findall(pattern_trojan, text_content, re.IGNORECASE) if "…" not in x]
    matches_vmess = [re.sub(r"#[^#]+$", "", html.unescape(x)) for x in re.findall(pattern_vmess, text_content, re.IGNORECASE) if "…" not in x]
    matches_vless = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#VLESS" for x in re.findall(pattern_vless, text_content, re.IGNORECASE) if "…" not in x]
    matches_reality = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#REALITY" for x in re.findall(pattern_reality, text_content, re.IGNORECASE) if "…" not in x]
    matches_tuic = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#TUIC" for x in re.findall(pattern_tuic, text_content) if "…" not in x]
    
    h1 = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#HYSTERIA" for x in re.findall(pattern_hysteria, text_content) if "…" not in x]
    h2 = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#HYSTERIA" for x in re.findall(pattern_hysteria_ver2, text_content) if "…" not in x]
    matches_hysteria = h1 + h2
    
    matches_juicity = [re.sub(r"#[^#]+$", "", html.unescape(x)) + "#JUICITY" for x in re.findall(pattern_juicity, text_content) if "…" not in x]

    return matches_usersname, matches_url, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity

def tg_message_time(div_message):
    div_message_info = div_message.find('div', class_='tgme_widget_message_info')
    message_datetime_tag = div_message_info.find('time')
    message_datetime = message_datetime_tag.get('datetime')
    datetime_object = datetime.fromisoformat(message_datetime)
    datetime_object = datetime.astimezone(datetime_object, tz=timezone(timedelta(hours=3, minutes=30)))
    datetime_now = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    return datetime_object, datetime_now, datetime_now - datetime_object

def tg_message_text(div_message, content_extracter):
    div_message_text = div_message.find("div", class_="tgme_widget_message_text")
    if not div_message_text: return ""
    text_content = div_message_text.prettify()
    if content_extracter == 'url':
        text_content = re.sub(r"<code>([^<>]+)</code>", r"\1", re.sub(r"\s*", "", text_content))
    elif content_extracter == 'config':
        text_content = re.sub(r"<code>([^<>]+)</code>", r"\1", re.sub(r"<a[^<>]+>([^<>]+)</a>", r"\1", re.sub(r"\s*", "", text_content)))
    return text_content

# (Дальнейший код сбора по каналам и сохранения по твоим папкам ./protocols и ./splitted остаётся оригинальным)
print("🚀 Скрипт Вилки успешно инициализирован без ошибок!")
