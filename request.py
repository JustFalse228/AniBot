import requests
from bs4 import BeautifulSoup
from aiogram import types
from AnimeTitles.db import add_title, get_title_id

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
}
cookies = {
}


def anime_request(url):
    random_title_response = requests.get(url, cookies=cookies, headers=headers)
    randomt_html = BeautifulSoup(random_title_response.content, "html.parser")

    anime_title = randomt_html.select("#content > div > div.media.mb-3.d-none.d-block.d-md-flex > div.media-body > div.anime-title > div > h1")[0].text
    anime_type = randomt_html.select(".anime-info > .row > dd.col-6")[0].text
    anime_image_link = randomt_html.select(".anime-poster > div > img")[0]
    anime_image = anime_image_link.get("src")
    anime_status = randomt_html.select(".anime-info > .row > dd.col-6 > a")[0]
    anime_status1 = anime_status.get("title")
    anime_genre = randomt_html.select(".anime-info > .row > dd.col-6")[3].text.strip()
    anime_genre_sort = " ".join(anime_genre.split())
    anime_season = randomt_html.select(".anime-info > .row > dd.col-6")[5].text

    try:
        anime_rating = (randomt_html.select(".itemRatingBlock > div.pr-2 > div > span.rating-value")[0].text + "/10")
    except:
        anime_rating = "Нет оценок"

    anime_description = randomt_html.select("main.content > div > div.description")[0].text.strip()
    anime_description_sort = " ".join(anime_description.split())[:700]

    if anime_status1 != "Вышел" and anime_status1 != "Онгоинг":
        anime_status1 = "Вышел"
        anime_genre = randomt_html.select("div.anime-info > .row > dd.col-6")[1].text.strip()
        anime_genre_sort = " ".join(anime_genre.split())
        anime_season = randomt_html.select(".anime-info > .row > dd.col-6")[3].text

    if anime_type == "OVA" or anime_type == "ONA":
        anime_status1 = "Вышел"
        anime_genre = randomt_html.select("div.anime-info > .row > dd.col-6")[2].text.strip()
        anime_genre_sort = " ".join(anime_genre.split())
        anime_season = randomt_html.select(".anime-info > .row > dd.col-6")[4].text
    elif anime_type == "Спешл":
        anime_season = randomt_html.select("#content > div > div.media.mb-3.d-none.d-block.d-md-flex > div.media-body > div.anime-info > dl > dd:nth-child(10) > span > span")[0].text

    return [anime_title, anime_type, anime_image, anime_status1, anime_genre_sort, anime_season, anime_rating, anime_description_sort, random_title_response]


def search_request(search_title):
    search_title_url = f"https://animego.org/search/anime?q={search_title}"
    response = requests.get(url=search_title_url)
    response_get = BeautifulSoup(response.content, "html.parser")
    anime_title = response_get.select("div.h5 > a")

    for title in anime_title:
        try:
            add_title(title.text, title.get("href"))
        except:
            pass

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    button_list = [types.InlineKeyboardButton(text=x.text[:50], callback_data=f"search_anime/{get_title_id(x.text)}") for x in anime_title]
    keyboard.add(*button_list)

    return keyboard
