from aiogram import Bot, Dispatcher, executor, types
import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto
import buttons
import request
from database import Database
from datetime import datetime
import AnimeTitles.db
import pytz


TOKEN = "YOUR TOKEN"

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode="html", disable_web_page_preview=True)
dp = Dispatcher(bot=bot, storage=storage)
db = Database()

try:
    AnimeTitles.db.create_titles()
except:
    pass

tz = pytz.timezone("Europe/Moscow")


class AnimeFind(StatesGroup):
    title = State()

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await bot.send_photo(message.from_user.id, photo=config.start_pic, caption=config.start, reply_markup=buttons.mainMarkup)
    current_datetime = datetime.now(tz)
    fix_date = current_datetime.strftime("%d.%m.%Y %H:%M")
    try:
        db.add_user(message.from_user.id, fix_date)
        print(f"Пользователь {message.from_user.full_name} зарегистрировался и был успешно добавлен в базу данных! ID: {message.from_user.username}. Time: {fix_date}")
    except:
        pass


@dp.message_handler(state=AnimeFind.title)
async def find_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()

    search_title = "+".join(data["title"].split())
    kb = request.search_request(search_title=search_title)

    await bot.send_message(message.from_user.id, f"📝 Результат по запросу: {data['title']}", reply_markup=kb)
    await state.finish()


@dp.callback_query_handler(text_startswith="search_anime/")
async def process_button_2_press(event: types.CallbackQuery):
    try:
        title_id = event.data.split("/")[1]
        url = AnimeTitles.db.get_url(title_id)
        current_title = request.anime_request(url=f"{url}")

        await bot.send_photo(event.from_user.id, photo=f"{current_title[2]}", caption=config.title(name_title=current_title[0],rating=current_title[6], type=current_title[1], status=current_title[3], genre=current_title[4], season=current_title[5], description=current_title[7], link=current_title[8].url), 
                             reply_markup=config.check_view(event.from_user.id, current_title[0], AnimeTitles.db.get_title_id(current_title[0])))
        await bot.delete_message(event.from_user.id, event.message.message_id)
    except Exception as e:
        await bot.send_message(event.from_user.id, e)
        print(e)

@dp.message_handler(content_types=['photo'])
async def check_photo(message: types.Message):
    id_photo = message.photo[-1].file_id
    print(id_photo)

@dp.message_handler()
async def random_title(message: types.Message):
    if db.check_user_db(message.from_user.id) is False:
        await bot.send_message(message.from_user.id, '✋ Вас нет в базе данных, <b>отправьте команду "/start"</b>')
        return
    else:
        pass

    #random anime
    if message.text == buttons.button_random:
        random_anime = request.anime_request(url="https://animego.org/anime/random")
        #try:
        try:
            AnimeTitles.db.add_title(str(random_anime[0]), random_anime[8].url)
        except Exception as _ex:
            print(_ex)

        await bot.send_photo(message.chat.id, photo=f"{random_anime[2]}", caption=config.title(name_title=random_anime[0], rating=random_anime[6], type=random_anime[1], status=random_anime[3], genre=random_anime[4], season=random_anime[5], description=random_anime[7], link=random_anime[8].url),
                                 reply_markup=config.check_view(message.from_user.id, random_anime[0], AnimeTitles.db.get_title_id(random_anime[0])))
            

    elif message.text == buttons.button_profile:
        profile = db.check_user(message.from_user.id)
        user_photo = await bot.get_user_profile_photos(message.from_user.id)
        await bot.send_photo(message.from_user.id, photo=user_photo.photos[0][0].file_id, caption=config.profile(id=message.from_user.id, reg_date=profile[1], viewed=profile[2], current_view=profile[3]), reply_markup=buttons.profileBtn())


    elif message.text == buttons.button_find:
        await bot.send_message(message.from_user.id, "✍️ Введите название Тайтла", reply_markup=buttons.mainMarkup)
        await AnimeFind.title.set()
    else:
        await bot.send_message(message.from_user.id, config.keyboard, reply_markup=buttons.mainMarkup)

"""ДОБАВЛЕНИЕ ТАЙЛТА В ПРОСМОТРЫ ЮЗЕРУ"""
@dp.callback_query_handler(text_startswith="ud_")
async def process_button_2_press(event: types.CallbackQuery):
    current_datetime = datetime.now(tz)
    fix_date = current_datetime.strftime("%d/%m/%Y")
    data = event.data.split("_")

    if data[3] == "1":
        name = AnimeTitles.db.get_title_for_id(data[1])
        title_name = f"{name}_{fix_date}"
        print(title_name)

        db.add_to_viewed(title_name, event.from_user.id)
        db.add_view_title(event.from_user.id)
        AnimeTitles.db.add_viewed(data[1])

        await bot.edit_message_reply_markup(event.message.chat.id, event.message.message_id, reply_markup=buttons.removeToView(event.from_user.id, data[1]))
        print(f"[INFO] Тайтл {title_name} был успешно добавлен юзеру {data[2]} в 'Просмотренные' {current_datetime} #1, {event.from_user.username}")

    else:
        name = AnimeTitles.db.get_title_for_id(data[1])
        print(name)
        title_name = f"{name}_{fix_date}"
        titles = db.get_cur_view(event.from_user.id)
        sep_titles = titles.split(';')
        cur_title = []

        for sepz in sep_titles:
            spp = sepz.split("_")
            if spp[0] != name:
                print(spp[0])
                cur_title.append(sepz)
            else:
                pass

        fin_cur_titles = ';'.join(cur_title)
    
        db.remove_cur_title(event.from_user.id, fin_cur_titles)
        db.minus_cur_view(event.from_user.id)
        db.add_to_viewed(title_name, event.from_user.id)
        db.add_view_title(event.from_user.id)

        await bot.edit_message_reply_markup(event.message.chat.id, event.message.message_id, reply_markup=buttons.removeToView(event.from_user.id, data[1]))
        print(f"[INFO] Тайтл {title_name} был успешно добавлен юзеру {data[2]} в 'Просмотренные' {current_datetime} #2, {event.from_user.username}")

"""ДОБАВЛЕНИЕ ТАЙЛТА В 'СМОТРЮ СЕЙЧАС' ЮЗЕРУ"""
@dp.callback_query_handler(text_startswith="uw_")
async def process_button_2_press(event: types.CallbackQuery):
    current_datetime = datetime.now(tz)
    fix_date = current_datetime.strftime("%d/%m/%Y")
    sep = event.data.split("_")

    name = AnimeTitles.db.get_title_for_id(sep[1])
    title_name = f"{name}_{fix_date}"

    db.add_cur_view(title_name, event.from_user.id)
    db.add_current_profile(event.from_user.id)
    AnimeTitles.db.add_view(sep[1])

    await bot.edit_message_reply_markup(event.message.chat.id, event.message.message_id, reply_markup=buttons.views_title(event.from_user.id, sep[1]))
    print(f"[INFO] Тайтл {title_name} был успешно добавлен юзеру {sep[2]} в 'Смотрю сейчас' {current_datetime}, {event.from_user.username}")


@dp.callback_query_handler(text="profile_titles")
async def profile_btn(event: types.CallbackQuery):
    await bot.edit_message_media(chat_id=event.message.chat.id, message_id=event.message.message_id, media=InputMediaPhoto(media=config.profile_views_pic, caption=config.user_titles(event.from_user.id)), reply_markup=buttons.backToProfile())

@dp.callback_query_handler(text="back_to_profile")
async def back_to_profile(event: types.CallbackQuery):
    profile = db.check_user(event.from_user.id)
    user_photo = await bot.get_user_profile_photos(event.from_user.id)
    await bot.edit_message_media(chat_id=event.message.chat.id, message_id=event.message.message_id, media=InputMediaPhoto(media=user_photo.photos[0][0].file_id, caption=config.profile(id=event.from_user.id, reg_date=profile[1], viewed=profile[2], current_view=profile[3])), reply_markup=buttons.profileBtn())

"""УДАЛЕНИЕ ТАЙТЛА ИЗ ПРОСМОТРОВ ЮЗЕРА"""
@dp.callback_query_handler(text_startswith="rmve_")
async def remove_title(event: types.CallbackQuery):
    data = event.data.split("_")
    if data[3] == "1":
        title_name = AnimeTitles.db.get_title_for_id(data[1])

        titles = db.get_titles(event.from_user.id)
        sep_titles = titles.split(';')
        current_titles = []

        for sep in sep_titles:
            spp = sep.split("_")
            if spp[0] != title_name:
                current_titles.append(sep)
            else:
                pass

        finally_titles = ';'.join(current_titles)
    
        db.remove_title(event.from_user.id, finally_titles)
        db.minus_viewed_titles(event.from_user.id)

        await bot.edit_message_reply_markup(event.message.chat.id, event.message.message_id, reply_markup=buttons.inlineView(title_name, event.from_user.id))
    else:
        title_name = AnimeTitles.db.get_title_for_id(data[1])
        titlez = db.get_cur_view(event.from_user.id)
        cur_titles = titlez.split(';')
        cur_title = []

        for sepz in cur_titles:
            sppz = sepz.split("_")
            if sppz[0] != title_name:
                cur_title.append(sepz)
            else:
                pass

        fin_cur_titles = ';'.join(cur_title)
    
        db.remove_cur_title(event.from_user.id, fin_cur_titles)
        db.minus_cur_view(event.from_user.id)
    
        await bot.edit_message_reply_markup(event.message.chat.id, event.message.message_id, reply_markup=buttons.inlineView(title_name, event.from_user.id))

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
