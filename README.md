# Config_keeper_v1
# запустить web сервер
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# обновить файл requirements.txt
pip freeze > requirements.txt

# Docker
[//]: # (клонировать проект)
git clone https://github.com/Barabinart/config_keeper_v1.git

[//]: # (не забыть сменить владельца)
chown -R art:art config_keeper_v1/

[//]: # ()
docker build . --tag config_keeper_v1

[//]: # (если занят 80 порт)
rm /etc/nginx/sites-enabled/default
service nginx reload

[//]: # (запустить докер контейнер с вольюмом для хранения БД)
docker run -v config_keeper_v1_volume:/db -p80:80 config_keeper_v1
