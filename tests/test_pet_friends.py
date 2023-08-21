from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, no_email, no_password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверка на возврат  статус-кода 200 и содержание
    слова key при запросе API-ключа"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

#Автотест №1 для задания 24.7.2:
def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    """Проверка на запрос API-ключа с вводом некорректных данных"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

#Автотест №2 для задания 24.7.2:
def test_get_api_key_without_user_data(email=no_email, password=no_password):
    """Проверка на запрос API-ключа с вводом пустых значений вместо емайла и пароля"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter = ""):
    """Проверка на возврат непустого списка при запросе запрос всех питомцев.
       Для этого: 1) получаем API-ключ и сохраняем в переменную auth_key; 2) используя этот ключ,
       запрашиваем список всех питомцев; 3) проверяем что список не пустой.
       Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200

#Автотест №3 для задания 24.7.2:
def test_get_all_pets_without_key(filter = ""):
    """Проверка на запрос списка питомцев без API-ключа. Поскольку введены некорректные логин и пароль
    или не введены никакие данные, то API-ключ не был получен"""
    _, auth_key = pf.get_api_key(invalid_email or no_email, invalid_password or no_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200

def test_add_new_pet_with_valid_data(name = "Pesik", animal_type = "Dog",
                                     age = "10", pet_photo = "images\Pesik.jpg"):
    """Проверка на возможность добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name

#Автотест №4 для задания 24.7.2:
def test_add_new_pet_with_invalid_data(name = "Kotik", animal_type = "Cat",
                                     age = "10", pet_photo = "images\9.jpg"):
    """Проверка на возможность добавить питомца с некорректными данными (с несуществующим фото)"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result["name"] == name

#Автотест №5 для задания 24.7.2:
def test_successful_add_new_pet_without_photo(name = "Красавица", animal_type = "Жучка",
                                   age = "5"):
    """Проверка на возможность добавить питомца без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name

#Автотест №6 для задания 24.7.2:
def test_unsuccessful_add_new_pet_without_photo(name = "", animal_type = "",
                                   age = ""):
    """Проверка на возможность добавить питомца без фото. При этом на сервер
    не отправляются сведения об имени, породе и возрасте питомца.
    При запуске теста был выявлен баг - тест успешно проходит, и добавляется питомец без данных (пустая строка).
    Однако при попытке вручную добавить питомца без данных на сайте, как и положено, всплывает
    диалоговое окно с просьбой ввести данные питомца (имя, породу, возраст)"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 200
    assert result["name"] == name

#Автотест №7 для задания 24.7.2:
def test_successful_add_pet_photo(pet_photo = "images\Kotik.jpg"):
    """Проверка на возможность добавить фото питомцу"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
        assert result["pet_photo"] != ""
    else:
        raise Exception("There is no my pets")

#Автотест №8 для задания 24.7.2:
def test_unsuccessful_add_pet_photo(pet_photo = ""):
    """Проверка на возможность добавить питомцу вместо фото пустую строку"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.add_pet_photo(auth_key, my_pets["pets"][0]["id"], pet_photo)

        assert status == 200
    else:
        raise Exception("There is no my pets")

def test_successful_update_self_pet_info(name = "Misha", animal_type = "Pet", age = 5):
    """Проверка на возможность обновить сведения о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("There is no my pets")

#Автотест №9 для задания 24.7.2:
def test_unsuccessful_update_self_pet_info(name = "Misha", animal_type = "Pet", age = 5):
    """Проверка на возможность обновить сведения о несуществующем питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][6]["id"], name, animal_type, age)

        assert status == 200
        assert result["name"] == name
    else:
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверка на возможность удалить питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Дмитрий", "Пёсик", "Котик", "images/Dima.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()

#Автотест №10 для задания 24.7.2:
def test_unsuccessful_delete_self_pet():
    """Проверка на возможность удалить несуществующего питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Дмитрий", "Пёсик", "Котик", "images/Dima.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][6]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()