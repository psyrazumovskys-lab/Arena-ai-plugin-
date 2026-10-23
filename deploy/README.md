# Как держать бота включённым

## Коротко

Бот «отключается» не из-за кода. Причин три, и все они про хостинг:

1. **Бесплатный worker на Render не работает вообще.** В бесплатном тарифе
   фоновых процессов нет — сервис типа `worker` просто не стартует. В
   `render.yaml` стоял именно `worker`.
2. **Бесплатный веб-сервис Render засыпает** после 15 минут без входящих
   HTTP-запросов. Пока в бота не писали — он спал; первое сообщение
   поднимало его 30–60 секунд, а иногда Telegram успевал получить ошибку.
3. **Два запущенных экземпляра с одним токеном** конфликтуют: Telegram
   разрешает только одно соединение, второй процесс падает с `409 Conflict`.
   Это типичная история, когда локальная копия осталась запущенной, а рядом
   работает хостинг.

## Вариант A. Render + внешний пинг (бесплатно, 5 минут работы)

В репозитории `render.yaml` уже переключён с `worker` на `web`. Дальше:

1. В Render удалить старый сервис-воркер и создать новый из репозитория —
   он прочитает `render.yaml`.
2. Проверить, что переменная `BOT_TOKEN` задана (Render → Environment).
   Значение в репозитории больше не хранится намеренно.
3. Открыть `https://<имя-сервиса>.onrender.com/healthz` — должно вернуться
   `Bot is running!`.
4. Завести бесплатный монитор в UptimeRobot или cron-job.org: URL
   `/healthz`, период 5 минут. Это не даёт сервису уснуть.

Ограничение: на бесплатном тарифе 750 часов в месяц, а в месяце 744.
Один сервис — влезает, но запаса почти нет. Если понадобится второй
сервис, лучше сразу вариант B.

## Вариант B. Свой сервер (надёжно, ~4–5 € в месяц)

Подходит любой VPS с Ubuntu. Бот работает через long polling, входящие
порты и домен не нужны.

```bash
sudo adduser --system --group psylab
sudo mkdir -p /opt/psylab-bot && sudo chown psylab:psylab /opt/psylab-bot

# код
sudo -u psylab git clone https://github.com/psyrazumovskys-lab/Arena-ai-plugin-.git /opt/psylab-bot

# окружение
sudo -u psylab python3 -m venv /opt/psylab-bot/venv
sudo -u psylab /opt/psylab-bot/venv/bin/pip install -r /opt/psylab-bot/bot/requirements.txt

# токен
sudo -u psylab cp /opt/psylab-bot/deploy/.env.example /opt/psylab-bot/.env
sudo -u psylab nano /opt/psylab-bot/.env     # вписать токен
sudo chmod 600 /opt/psylab-bot/.env
```

Затем служба:

```bash
sudo cp /opt/psylab-bot/deploy/psylab-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now psylab-bot
systemctl status psylab-bot --no-pager
journalctl -u psylab-bot -f          # живые логи
```

`Restart=always` в юните означает: упал — поднялся через 5 секунд, после
перезагрузки сервера — поднялся сам. Это и есть «не отключается».

Обновление кода:

```bash
sudo -u psylab git -C /opt/psylab-bot pull
sudo systemctl restart psylab-bot
```

## Вариант C. Платный Render

Тот же `render.yaml`, но `plan: starter`. Фоновый процесс не засыпает,
пинг не нужен. Около 7 $ в месяц.

## Правила, без которых всё равно отвалится

- **Один экземпляр.** Перед запуском на сервере остановить копию на Render
  (или наоборот). Два процесса с одним токеном = `409 Conflict`.
- **Токен только в переменной окружения.** Раньше он лежал прямо в
  `bot/main.py` и попал в публичную историю git. Такой токен надо
  перевыпустить: @BotFather → `/revoke` → выбрать бота → получить новый.
- **После перевыпуска** обновить `BOT_TOKEN` на хостинге и перезапустить.
- **Health-check не обязателен** для работы бота (он работает на long
  polling), но нужен Render, чтобы понимать, что сервис жив.

## Проверка, что бот действительно жив

```bash
curl -s https://<адрес>/healthz          # Bot is running!
```

И в Telegram: `/start` должен ответить сразу. Если отвечает через 30–60
секунд — сервис спит, пинг не настроен.
