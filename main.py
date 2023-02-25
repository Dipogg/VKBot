import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import collecting_information
import search_module
import database
from configuration_file import list_filtered_users


for event in collecting_information.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:
            request = event.text

            if request.lower() == "привет":
                collecting_information.write_msg(event.user_id, f"Хай, {event.user_id}. Для старта поиска введите 'поиск': ")
            elif request.lower() == "поиск":
                database.create_table_search_users()
                user_dict = collecting_information.get_user_info(event.user_id)
                search_module.search_users(event.user_id, user_dict, list_filtered_users)
            elif request.lower() == "далее":
                if len(list_filtered_users) == 0:
                    search_module.search_users(event.user_id, user_dict, list_filtered_users)
                else:
                    search_module.give_user(event.user_id, user_dict, list_filtered_users)
            elif request.lower() == "пока":
                collecting_information.write_msg(event.user_id, "Пока((")
            else:
                collecting_information.write_msg(event.user_id, "Не поняла вашего ответа...")