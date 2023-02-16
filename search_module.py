import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from collecting_information import write_msg
from database import insert_search_users


def search_users(message_id, vk_token, user_dict, offset=0):
    users_found = vk_token.method('users.search', {'city': user_dict['city']['id'], 'sex': user_dict['sex'], 'status': 1 or 6, 'age_from': user_dict['age'], 'age_to': user_dict['age'], 'is_closed': False, 'offset': offset, 'count': 1, 'has_photo': 1, 'fields': 'id, first_name, last_name, city_name'})
    try:
        list_users = users_found['items']
        for users_found_dict in list_users:
            if users_found_dict.get('is_closed') == False:
                first_name = users_found_dict.get('first_name')
                last_name = users_found_dict.get('last_name')
                vk_id = str(users_found_dict.get('id'))
                vk_link = 'vk.com/id' + str(users_found_dict.get('id'))
                insert_search_users(user_id_search=vk_id)
                photo_max_size = (get_photo_info(vk_id, vk_token))
                write_msg(message_id, f"Фото 1 {photo_max_size[0]}")
                write_msg(message_id, f"Фото 2 {photo_max_size[1]}")
                write_msg(message_id, f"Фото 3 {photo_max_size[2]}")
                write_msg(message_id, f"Ссылка {vk_link}")
                write_msg(message_id, f"Для показа следующей анкеты введите 'далее'")
            else:
                write_msg(message_id, f"Произошел сбой, введите 'далее'")
        return
    except:
        write_msg(message_id, f"Ошибка, попробуйте еще раз.")


def get_photo_info(user_id, vk_token):
    photo_info = vk_token.method('photos.getAll', {'owner_id': user_id, 'extended': 1})
    try:
        photo_info = photo_info['items']
        dict_photos = dict()
        for photo in photo_info:
            photo_id = str(photo.get('id'))
            photo_likes = photo.get('likes')
            photo_user_id = photo.get('owner_id')
            if photo_likes.get('count'):
                likes = photo_likes.get('count')
                dict_photos[likes] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        list_search = []
        if len(list_of_ids) > 4:
            del list_of_ids[3:-1]
            list_of_ids.pop()
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[0][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[1][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[2][1]))
        elif len(list_of_ids) == 4:
            list_of_ids.pop()
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[0][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[1][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[2][1]))
        elif len(list_of_ids) == 3:
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[0][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[1][1]))
            list_search.append(get_photo_link(vk_token, photo_user_id, list_of_ids[2][1]))
        return(list_search)
    except:
        write_msg(event.user_id, f"Ошибка, попробуйте еще раз 22")


def get_photo_link(vk_token, user_id, photo_user_id):
    list_photo_get = vk_token.method('photos.getById', {'photos': f'{user_id}_{photo_user_id}', 'photo_sizes': 0})
    try:
        for elem in list_photo_get:
            list_photo_get_sizes = elem['sizes']
        list_keys = []
        for i in list_photo_get_sizes:
            list_keys.append(i['height'])
        height_max = max(list_keys)
        for n in list_photo_get_sizes:
            if n['height'] == height_max:
                photo_max_add = (n['url'])
        return photo_max_add
    except:
        write_msg(event.user_id, f"Ошибка, попробуйте еще раз")