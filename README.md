# Скрипты для ВК
## Установка необходимых модулей
* `python -m venv VK_utils_venv`
* `VK_utils_venv/Scripts/activate`
* `pip install -r requirements.txt`  
## Создание файла с данными для авторизации
TODO
## Внимание
Запускать скрипты нужно из соответствующих директорий.
Например, чтобы запустить `VKMusicDownloader.py`, нужно сначала перейти в директорию `MusicDownloader`.
## Список скриптов
* [Загрузка музыки](MusicDownloader/VKMusicDownloader.py)  
**ВНИМАНИЕ** Данному скрипту нужен [ffmpeg](https://ffmpeg.org/download.html).  
Этот скрипт загружает музыку пользователя по его ID.  
`python VKMusicDownloader.py OutputDirectory USER_ID`  
`OutputDirectory` &mdash; директория, в которую нужно сохранить аудио файлы.  
`USER_ID` &mdash; ID пользователя, у которого нужно скачать музыку.
* TODO
