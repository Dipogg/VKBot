import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
import datetime
from configuration_file import comm_token, user_dict


vk = vk_api.VkApi(token=comm_token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message=None, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment, 'random_id': randrange(10 ** 7)})


def get_user_info(user_id):
    user_info = vk.method('users.get', {'user_ids': user_id, 'fields': 'sex, bdate, city, relation'})
    try:
        user_info_dict = user_info[0]
        converting_dict(user_info_dict)
        return user_dict
    except:
        write_msg(event.user_id, f"Ошибка, попробуйте еще раз")


def converting_dict(user_info_dict):
    user_dict['user_id'] = user_info_dict['id']
    user_dict['first_name'] = user_info_dict['first_name']
    user_dict['last_name'] = user_info_dict['last_name']
    user_dict['relation'] = user_info_dict['relation']
    if user_info_dict['sex'] > 0:
        if user_info_dict['sex'] == 1:
            user_dict['sex'] = 2
        else:
            user_dict['sex'] = 1
    else:
        write_msg(user_dict['user_id'], 'Введите ваш пол, мужской 1 или женский 2: ')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                gender_user = event.text
                try:
                    gender_user = int(gender_user)
                    user_dict['sex'] = gender_user
                except:
                    write_msg(user_dict['user_id'], 'Пол введен не верно. Введите целое число: ')

    if 'bdate' in user_info_dict:
        user_dict['bdate'] = user_info_dict['bdate']
        get_user_age(user_dict)
    else:
        user_dict['bdate'] = '0.0'
        get_user_age(user_dict)

    if 'city' in user_info_dict:
        user_dict['city'] = user_info_dict['city']
    else:
        get_city(user_dict)
    return user_dict


def get_user_age(user_dict):
    date = user_dict.get('bdate')
    date_list = date.split('.')
    if len(date_list) == 3:
        year = datetime.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))
        year_now = datetime.date.today()
        age_user = int((year_now - year).days / 365)
        user_dict['age'] = age_user
    elif len(date_list) == 2:
        write_msg(user_dict['user_id'], 'Введите ваш возраст: ')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_user = event.text
                try:
                    age_user = int(age_user)
                    user_dict['age'] = age_user
                    return user_dict
                except:
                    write_msg(user_dict['user_id'], 'Возраст введен не привильно. Введите целое число: ')
                    for event in longpoll.listen():
                        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                            age_user = event.text
                            try:
                                age_user = int(age_user)
                                user_dict['age'] = age_user
                                return user_dict
                            except:
                                write_msg(user_dict['user_id'], 'Не хочешь, не надо. Пока. Передумаешь, напишешь возраст правильно.')


def get_city(user_dict):
    write_msg(user_dict['user_id'], 'Введите ваш город: ')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            city_user = event.text
            user_dict['city'] = city_user
            get_city_list(user_dict)
            return user_dict


def get_city_list(user_dict):
    list_city = vk_token.method('database.getCities', {'need_all': 1})
    try:
        list_cities = list_city['items']
        for city_id in list_cities:
            found_city_name = city_id.get('title')
            if found_city_name == user_dict['city']:
                found_city_id = city_id.get('id')
                user_dict['city'] = {'id': int(found_city_id), 'title': found_city_name}
                return user_dict
    except:
        write_msg(user_dict['user_id'], 'Название города введено не привильно. Попробуйте еще раз: ')