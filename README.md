# Скрипты для ВК
## Установка необходимых модулей
* `python -m venv VK_utils_venv`
* `VK_utils_venv/Scripts/activate`
* `pip install -r requirements.txt`  
## Создание файла с данными для авторизации
Нужно создать файл `login.json` в папке `LoginData` по примеру:  
```json
{
    "login": "ЛОГИН",
    "pass": "ПАРОЛЬ"
}
```
## Внимание
Запускать скрипты нужно из соответствующих директорий.
Например, чтобы запустить `VKMusicDownloader.py`, нужно сначала перейти в директорию `MusicDownloader`.
## Список скриптов
* [Загрузка музыки](MusicDownloader/VKMusicDownloader.py)  
**ВНИМАНИЕ** Данному скрипту нужен [ffmpeg](https://ffmpeg.org/download.html).  
Этот скрипт загружает музыку пользователя по его ID.  
Запуск: `python VKMusicDownloader.py OutputDirectory USER_ID`  
`OutputDirectory` &mdash; директория, в которую нужно сохранить аудио файлы.  
`USER_ID` &mdash; ID пользователя, у которого нужно скачать музыку.
* [Распознавание лиц](AlbumFaceRecognition/main.py)  
Этот скрипт находит знакомые лица в альбомах. Фотографии искомых людей нужно поместить в папку `known_people`.  
Запуск: `python main.py`.  
Настройка параметров происходит в `config.py`.  
Скрипт работает только в одном потоке, поэтому возможна низкая скорость работы, особенно при работе на CPU.