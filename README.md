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
Все скрипты содержат необязательный аргумент `login`, указывающий на путь к json файлу с данными для авторизации.  
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
* [Автостатус](AutoStatus/AutoStatus.py)  
Этот скрипт создает обратный отсчет до даты в статусе.  
Запуск: `python AutoStatus.py TEXT DATE`.  
`TEXT` &mdash; название события.  
`DATE` &mdash; дата события в формате `DD.MM.YYYY HH:MM`.  
Также присутствует необязательный аргумент `delay`, указывающий задрежку между обновлением таймера (по умолчанию, 10 секунд).  
* [Получить данные о лайках](GetLikes/GetLikes.py)  
Этот скрипт получает подробные данные о пользователях, лайкнувших пост, комментарий, фотографию или видео.  
Запуск: `python GetLikes.py URL OUTPUT`.  
`URL` &mdash; ссылка на пост, комментарий, фотографию или видео.  
`OUTPUT` &mdash; куда нужно сохранить таблицу.  
* [Получить ID пользователя](GetUserID/GetUserID.py)  
Этот скрипт возвращает ID пользователя по алиасу.  
Запуск: `python GetUserID.py screenName`.  
`screenName` &mdash; алиас пользователя.  
* [Получить дни рождения пользователей в чате](GetBirthdaysChat/GetBirthdaysChat.py)  
**ВНИМАНИЕ** Данный скрипт пока что не работает из-за ограничений ВК.  
Запуск: `python GetBirthdaysChat.py chatID`.  
`chatID` &mdash; ID чата.  
* [Получить данные о нахождении в сети пользователей](SpyOnline/SpyOnline.py)  
Этот скрипт позволяет собирать данные о нахождении в сети пользователей с периодом.  
Запуск: `python SpyOnline.py -u USERS --delay DELAY`.  
`USERS` &mdash; список ID пользователей, разделенных пробелом.  
`DELAY` &mdash; период между запросами (в секундах).  
* [Отправить аудио файл как голосовое сообщение](SendAudioAsVoice/SendAudioAsVoice.py)  
Этот скрипт позволяет отправить аудио файл как голосовое сообщение.  
Запуск: `python SendAudioAsVoice.py FILE`.  
`FILE` &mdash; путь к аудио файлу.  
Этот скрипт выводит ссылку на документ, при отправке ссылки пользователю, она превращается в голосовое сообщение. К сожалению из-за ограничений ВК, автоматическая отправка сообщений невозможна.