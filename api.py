import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    """API-библиотека для тестового веб приложения PetFriends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод делает запрос к API сервера, возвращая статус запроса и результат
        в формате JSON с уникальными ключом пользователяб найденного по указанным email и паролю"""

        headers = {
            "email": email,
            "password": password
        }
        res = requests.get(self.base_url+"api/key", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера, возвращая статус запроса и результат
        в формате JSON со списком найденных питомцев, совпадающих с фильтром. На данный момент фильтр
        может иметь либо пустое значение - получать список всеп питомцев, либо 'my pets' - получать список
        собственных питомцев"""

        headers = {"auth_key": auth_key["key"]}
        filter = {"filter": filter}

        res = requests.get(self.base_url+"api/pets", headers=headers, params=filter)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце, возвращая статус
        запроса и результат в формате JSON со сведениями о добавленном питомце"""

        data = MultipartEncoder(
            fields={
            "name": name,
            "animal_type": animal_type,
            "age": age,
            "pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpeg")
            })

        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url + "api/pets", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Метод №1 для задания 24.7.2:
    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце, возвращая статус
        запроса и результат в формате JSON со сведениями о добавленном питомце.
        Отличие от метода add_new_pet состоит в том, что питомец, добавленный с помощью данного метода,
        не имеет фото"""

        data = MultipartEncoder(
            fields={
            "name": name,
            "animal_type": animal_type,
            "age": age
            })

        headers = {"auth_key": auth_key["key"], "Content-Type": data.content_type}

        res = requests.post(self.base_url + "api/create_pet_simple", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    #Метод №2 для задания 24.7.2:
    def add_pet_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемой фотограйии питомца, возвращая статус
        запроса и результат в формате JSON с обновленными сведениями о питомце"""

        headers = {"auth_key": auth_key["key"]}
        file = {"pet_photo": (pet_photo, open(pet_photo, "rb"), "image/jpeg")}

        res = requests.post(self.base_url + f"api/pets/set_photo/{pet_id}", headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос об обновлении данных питомуана сервер  по указанному ID и
              возвращает статус-код запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {"auth_key": auth_key["key"]}

        data = {
            "name": name,
            "age": age,
            "animal_type": animal_type
        }

        res = requests.put(self.base_url + f"api/pets/{pet_id}", headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID, возвращая
        статус-код запроса и результат в формате JSON с текстом уведомления об успешном удалении.
        На данный момент тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {"auth_key": auth_key["key"]}

        res = requests.delete(self.base_url + f"api/pets/{pet_id}", headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result