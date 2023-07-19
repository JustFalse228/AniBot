from AnimeTitles.db import get_titles_views, get_title_for_id
from database import Database
from buttons import removeToView, inlineView, views_title

db = Database()

warn = "<b><i>Не так быстро!</i></b>"
keyboard = "<b><i>⌨️ Открываю клавиатуру</i></b>"
profile_views_pic = 'AgACAgIAAxkBAAILq2Syc52PLBo5OEJCTiHGB_4tDFkKAAL2yDEbX66QSR32AgjbGX7JAQADAgADeQADLwQ'
start_pic = 'AgACAgUAAxkBAAILfWSxv1ZTt847krw4euKo0NcnMkAYAALTuDEbU06RVat1SMbinVolAQADAgADeQADLwQ'

start = """
<b>Приветствую, аниме-любитель! 🌟🌸</b>

Я - твой верный аниме-бот, готовый помочь тебе в поиске новых и захватывающих аниме-сериалов! 🎌📺

У меня есть несколько волшебных функций, которые сделают твой опыт просмотра аниме ещё более удивительным. 💫

> <i>Первое, я могу сгенерировать случайное аниме для тебя. Просто нажми на кнопку, и я предложу тебе увлекательный выбор для просмотра. 🎉✨</i>
> <i>Кроме того, ты можешь добавлять интересующие тебя аниме в свой список просмотренных. 📝🔖</i>
> <i>Ты также можешь в любой момент заглянуть в свой профиль, чтобы увидеть, что ты уже посмотрел. 📚👀</i>

Так давай начнем наше аниме-путешествие вместе! Просто скажи мне, что тебе нужно, и я с радостью помогу. 🌈
"""


def profile(id, reg_date, viewed, current_view):
    text = f"""
    👤 <b>Профиль пользователя</b>

🪪 ID: <code>{id}</code>
📅 Дата регистрации: <code>{reg_date}</code>

👀 Просмотрено Тайтлов: <code>{viewed}</code>
🔭 Смотрю: <code>{current_view}</code>

<i>"Говна поешь, мудила!" - Джайро Цеппели (JoJo)</i>
    """
    return text


def title(name_title, rating, type, status, genre, season, description, link):
    views = get_titles_views(name_title)
    text = f"""
<b><i>{name_title}</i></b>

<b>⭐️ Рейтинг AnimeGO:</b> <code>{rating}</code>
<b>🔎 Тип: </b><code>{type}</code>
<b>📊 Статус:</b> <code>{status}</code>
<b>💬 Жанр: </b> <code>{genre}</code>
<b>🌍 Сезон/Выпуск: </b><code>{season}</code>

<b>👀 Уже посмотрели:</b> <code>{views[1]} человек(а)</code>
<b>🔭 Сейчас смотрят:</b> <code>{views[0]} человек(а)</code>

➖➖➖➖➖➖➖➖➖➖➖➖➖➖
<i>{description}</i>..
➖➖➖➖➖➖➖➖➖➖➖➖➖➖

<a href="{link}">Смотреть на AnimeGO</a>
    """
    return text

def user_titles(id):
    try:
        #viewed titles
        titles = db.get_titles(id)
        titles_split = titles.split(';')
        title_array = []

        for xz in titles_split:
            split = xz.split("_")
            title_array.append(split)

        titles_formatted = "\n".join([f"> <b>{x[0]}.</b> <code>Добавлено: {x[1]}</code>" for x in title_array])

    except:
        titles_formatted = "<b>Список пуст. Не волнуйся, я буду ждать с нетерпением, когда ты пополнишь его новыми и захватывающими аниме-сериалами! 🎉✨</b>"

    #cur viewed titles
    try:
        cur_titles = db.get_cur_view(id)
        titles_cur_split = cur_titles.split(';')
        title_cur_array = []

        for xz in titles_cur_split:
            cur_split = xz.split("_")
            title_cur_array.append(cur_split)

        cur_view = "\n".join([f"> <b>{x[0]}.</b> <code>Добавлено: {x[1]}</code>" for x in title_cur_array])
    except:
        cur_view = "<b>Список пуст.</b>"
    

    text = f"""
🌟 <b>Привет, мой аниме-ценитель!</b>

<i>Я рад сообщить тебе о некоторых аниме-шедеврах, которые уже украшают твою коллекцию! Эти невероятные сериалы подарят тебе массу эмоций и незабываемых приключений. 🎉✨</i>

<b>🏆 Просмотрено:</b>
{titles_formatted}

<b>👀 Смотрю сейчас:</b>
{cur_view}

<i>Великолепный выбор! Ты настоящий ценитель искусства анимации. С нетерпением жду, как ты окунешься в увлекательные и захватывающие миры этих сериалов. 🌈🌍</i>

"""
    return text


def check_view(id, anime, title_id):
    try:
        titles = db.get_titles(id)
        cur_titles = db.get_cur_view(id)
        sep_cur_titles = cur_titles.split(';')
        sep_titles = titles.split(';')

        for sep in sep_titles:
            spp = sep.split("_")
            if spp[0] == anime:
                button = removeToView(id, title_id)
            else:
                button = inlineView(anime, id)
        for cur_sep in sep_cur_titles:
            split = cur_sep.split("_")
            if split[0] == anime:
                button = views_title(id, title_id)
    except:
        button = inlineView(anime, id)
    
    return button