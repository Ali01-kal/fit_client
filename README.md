# fitClient (Fitness Client Management System)

`fitClient` — Django-проект для управления фитнес-клиентами, тренерами, программами тренировок, абонементами, отзывами и отчётами.

Важно: домен/хостинг/HTTPS и доступность до `01.06.2026` выполняются вручную при деплое. В этом репозитории подготовлена кодовая база и инструкции для публикации.

## Что реализовано

- Django-проект с `DEBUG` через env, `include + namespace` в `urls.py`
- 13 приложений (`core`, `accounts`, `clients`, `trainers`, `programs`, `memberships`, `attendance`, `payments`, `appointments`, `nutrition`, `reviews`, `reports`, `api`)
- Базовый layout (`base.html`), header/footer, навигация, кастомные `404/500`
- Регистрация, логин/логаут, профиль, смена/восстановление пароля (console email backend для dev)
- CRUD-формы: клиенты, программы, тарифы, подписки, отзывы
- ORM-модели (20+), связи `FK/M2M`, `slug`, валидация модели, индексы, `select_related/prefetch_related`
- Отчёты (`annotate`, `Count`, `Avg`)
- Админка: регистрация моделей, `list_display/search_fields/list_filter`, `inline`, `actions`, `fieldsets`, `prepopulated_fields`
- JSON API (7 endpoints) + фильтры + защищённые `POST/PUT/DELETE` для программ
- Статика/медиа, кастомный CSS/JS, адаптивность и UI-эффекты
- `seed_fitclient` команда для тестовых данных

## Быстрый старт (локально)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_fitclient
python manage.py runserver
```

## Тестовые логины

- `manager` (создайте пароль вручную через admin/createsuperuser)
- Тестовые клиенты из `seed` — доменные записи, не всегда пользователи auth

## API (мини-документация)

Базовый префикс: `/api/`

- `GET /api/clients/?search=&status=active&trainer=1&ordering=-created_at&page=1`
- `GET /api/clients/<slug>/`
- `GET /api/programs/?search=&category=1&difficulty=beginner&trainer=1&ordering=name`
- `POST /api/programs/` (только `staff` или группа `manager`)
- `GET|PUT|DELETE /api/programs/<slug>/`
- `GET /api/subscriptions/?status=active&client=1`
- `GET /api/reviews/?rating=5&program=1`
- `GET /api/stats/`

Формат ошибок:

```json
{"error":{"code":"forbidden","message":"Authentication required"}}
```

## Роли

- `member`
- `trainer`
- `manager`
- `staff/admin` (Django admin)

### Группы и permissions (автонастройка)

- После `python manage.py migrate` автоматически создаются группы `member`, `trainer`, `manager` (через `post_migrate`)
- Для `trainer` и `manager` назначается базовый набор permissions (`clients/programs/memberships/reviews`)
- Проверить можно в Django admin: `Authentication and Authorization -> Groups`

## Статика и медиа

- `STATIC_URL`, `STATIC_ROOT`, `STATICFILES_DIRS` настроены
- `MEDIA_URL`, `MEDIA_ROOT` настроены
- На сервере выполните: `python manage.py collectstatic --noinput`
- Для аватаров и изображений используется `ImageField`; в шаблонах добавлены placeholder-ы при отсутствии файла
- На проде нужно настроить отдачу `MEDIA_URL` веб-сервером/хостингом (Nginx/static media mapping)

## Деплой (домен + хостинг + PostgreSQL)

Для полного соответствия заданию:

1. Развернуть проект на хостинге
2. Подключить PostgreSQL
3. Настроить env (`DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `DATABASE_URL`)
4. Привязать домен (например `fitclient.kz`)
5. Включить HTTPS
6. Проверить доступность проекта онлайн до конца 7-й недели курса

Для восстановления пароля по email на продакшене настройте SMTP (`EMAIL_BACKEND`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`).

## Логи / рестарт / диагностика

- Логи: stdout/stderr (`gunicorn`, панель хостинга, `journalctl`)
- Рестарт (пример VPS):
  - `sudo systemctl restart fitclient`
  - `sudo journalctl -u fitclient -n 200`

## Резервное копирование

- Ежедневный `pg_dump`
- Бэкап `media/`
- Хранить несколько последних копий

## Free Template (обязательное условие преподавателя)

В проекте используется и интегрирован бесплатный HTML/CSS шаблон:

- Template: `Zacson` (Colorlib)
- Source/Preview: `https://colorlib.com/wp/template/zacson/`
- Локальный исходник пользователя: `C:\Users\alika\Downloads\zacson-master\zacson-master`
- Author: `Colorlib`
- License / usage notes: см. `readme.txt` в шаблоне (copyright template info нельзя удалять без лицензии)

Что доработано под `fitClient`:

- HTML страницы переведены в Django templates (`{% url %}`, `{% static %}`, динамические блоки)
- Навигация привязана к разделам проекта (`clients`, `programs`, `memberships`, `reviews`, `reports`)
- Главная страница наполняется данными из БД (программы, категории, отзывы, статистика)
- Футер и контент адаптированы под тему фитнес CRM/клиентов
- Добавлены переключатели языка (RU/KZ) и темы (Light/Dark)
- Добавлено простое ограничение частоты входа (login rate-limit через session)
- `Оформить` в карточке тарифа открывает форму с предвыбранным тарифом
- Добавлены breadcrumbs на ключевых страницах и блок “мои действия” в профиле

## Чеклист перед сдачей

1. Сгенерировать и закоммитить миграции
2. Задеплоить на хостинг и домен
3. Включить HTTPS
4. Заполнить реальный URL в README
5. Проверить доступность сайта `01.06.2026`
6. Обновить страницу `/about/` реальными именами участников и ролями команды
