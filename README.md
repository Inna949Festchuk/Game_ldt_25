# Проект "Nerpa Games"

## Проект уже доступен для просмотра в браузере по адресу 
`http://79.174.94.234/`

---

## Разворачиваем проект на сервере через Docker и docker-compose.yml:
1. Создать папку и перейти в нее 
```bash
mkdir game && cd game 
```
2. Клонируем репозитлорий
```bash
git clone https://github.com/Inna949Festchuk/Game_ldt_25.git
```
3. Запускаем сервис
```bash
docker-compose up -d
```
4. Переходим в браузере `http://IP-адрес вашего сервера/`
   
5. Выгружаем сервис с удалением томов
```bash
docker-compose down -v
```

6. Удаляем старые контейнеры если что-то пошло совсем не так :
```bash
docker system prune -a --volumes --force
```

---

## Для доработки проекта запускаем проект локально в виртуальном окружении (Linux Ubuntu 24.04 LTS):

1. Создать папку и перейти в нее 
```bash 
mkdir game && cd game
```
2. Клонируем репозиторий
```bash
git clone https://github.com/Inna949Festchuk/Game_ldt_25.git
```
3. Создаем виртуальное окружение
```bash 
python -m venv venv
```
4. Активируем виртуальное окружение
```bash 
source venv/bin/activate
```
5. Устанавливаем необходимые зависимости
```bash 
python -m pip install -r requirements.txt
```
6. Запускаем сервер разработки (для доработки проекта)
```bash 
python manage.py runserver 0.0.0.0:8000
```
7. Останавливаем сервер `"Ctrl+C"`


## Копирование больших файлов (более 100 Мб на файл и более 1Гб на общий объем проекта) игры в .zip архиве через Google Drive на боевой сервер:
1. Загрузить на Google Drive и открыть общий доступ по ссылке к файлу `webgl.zip`
2. Открываем в браузере `https://drive.google.com/file/d/1bHoFrBRcjGANxRCedSol7co3KPnTCnDv/view?usp=share_link` и копируем id файла `1bHoFrBRcjGANxRCedSol7co3KPnTCnDv`
3. На сервере создаем папку `data`
```bash 
mkdir data && cd data
```
4. Создаем переменные окружения
```bash
export FILE_ID="1bHoFrBRcjGANxRCedSol7co3KPnTCnDv"
export FILE_NAME="webgl.zip"
```
5. Загружаем файл `
```bash 
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=${FILE_ID}" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=${FILE_ID}" -O ${FILE_NAME} && rm -rf /tmp/cookies.txt
```
6. Копируем архив в папку `/root/nerpa/Game_ldt_25/staticfiles`
```bash
cp data/${FILE_NAME} /root/nerpa/Game_ldt_25/staticfiles
```
7. Распаковываем архив (`sudo apt update && sudo apt install unzip`)
```bash
unzip ${FILE_NAME}
```
8. Удаляем архив
```bash
rm -rf ${FILE_NAME}
```