import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from collecting_information import write_msg
from database import insert_search_users
from configuration_file import token, list_filtered_users, offset


vk_token = vk_api.VkApi(token=token)


def search_users(message_id, user_dict, list_filtered_users):
    global offset
    users_found = vk_token.method('users.search', {'city': user_dict['city']['id'], 'sex': user_dict['sex'], 'status': 1 or 6, 'age_from': user_dict['age'], 'age_to': user_dict['age'], 'is_closed': False, 'offset': offset, 'count': 50, 'has_photo': 1, 'fields': 'id, first_name, last_name, city_name'})
    try:
        offset += 50
        list_users = users_found['items']
        for users_found_dict in list_users:
            if users_found_dict.get('is_closed') == False:
                list_filtered_users.append(users_found_dict)
        give_user(message_id, user_dict, list_filtered_users)
        return list_filtered_users
    except:
        write_msg(message_id, f"Ошибка, попробуйте еще раз.")


def give_user(message_id, user_dict, list_filtered_users):
    if len(list_filtered_users) == 0:
        search_users(message_id, user_dict, list_filtered_users)
    else:
        user_take = list_filtered_users[0]
        del list_filtered_users[0]
        first_name = user_take.get('first_name')
        last_name = user_take.get('last_name')
        vk_id = str(user_take.get('id'))
        vk_link = f"vk.com/id{vk_id}"
        insert_search_users(user_id_search=vk_id)
        photo_max_like = (get_photo_info(vk_id, message_id, user_dict, list_filtered_users))
        if len(photo_max_like) < 3:
            search_users(message_id, user_dict, list_filtered_users)
        else:
            write_msg(user_id=message_id, attachment=f"photo{photo_max_like[0]}")
            write_msg(user_id=message_id, attachment=f"photo{photo_max_like[1]}")
            write_msg(user_id=message_id, attachment=f"photo{photo_max_like[2]}")
            write_msg(message_id, f"{first_name} {last_name}")
            write_msg(message_id, f"Ссылка {vk_link}")
            write_msg(message_id, f"Для показа следующей анкеты введите 'далее'")
    return list_filtered_users


def get_photo_info(user_id, message_id, user_dict, list_filtered_users):
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
            list_search.append(f"{photo_user_id}_{list_of_ids[0][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[1][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[2][1]}")
        elif len(list_of_ids) == 4:
            list_of_ids.pop()
            list_search.append(f"{photo_user_id}_{list_of_ids[0][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[1][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[2][1]}")
        elif len(list_of_ids) == 3:
            list_search.append(f"{photo_user_id}_{list_of_ids[0][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[1][1]}")
            list_search.append(f"{photo_user_id}_{list_of_ids[2][1]}")
        return list_search
    except:
        write_msg(event.user_id, f"Ошибка, попробуйте еще раз")