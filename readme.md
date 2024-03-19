# Запуск
```
git clone https://github.com/ruha02/gmail-clean
cd gmail-clean
pip install -r req.txt
```
После подготовки, необходимо получить [Google API Client ID](https://developers.google.com/identity/oauth2/web/guides/get-google-api-clientid)

Файл credentials.json положить в корень с программой.

Сформировать файл spamlist.txt, которые будет содержать адреса электронных почт, письма от которых, необходимо удалить.

Например:
```
letsencrypt.org
calendar-notification@google.com
...
```
