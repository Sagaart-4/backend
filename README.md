
# Бэкэнд сайта для онлайн-галереи Sagaart

## Обзор
Проект представляет собой минимально жизнеспособный продукт (MVP) сайта для онлайн-галереи Sagaart. Это платформа, где пользователи могут регистрироваться в качестве продавцов или покупателей произведений искусства. На сайте можно просматривать произведения искусства, покупать и продавать их. Также на платформе есть сервис оценки арт-объектов современного искусства. Он работает на основе анализа больших данных с помощью авторского алгоритма.


## Стек технологий
![Python](https://img.shields.io/badge/-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-009688?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/-Postgres-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/-Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)

## URL-адреса проекта:
- Проект: https://xaverd.hopto.org

## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: https://docs.docker.com/get-docker/ и https://docs.docker.com/compose/install/

### Установка и запуск

1. Клонируйте репозиторий на локальный компьютер:
   ```
   git clone git@github.com:Sagaart-4/backend.git
   cd backend/infra
   ```

2. Запустите контейнеры с помощью Docker Compose:
   ```
   docker compose -f docker-compose.local.yml up
   ```

   Теперь приложение должно быть доступно по адресу:

   http://localhost

   А документация доступна по адресу:

   http://localhost/api/v1/swagger/

</details>


## Над проектом работали
- [**Владислав Шкаровский**](https://github.com/0z0nize)
- [**Владислав Суворов**](https://github.com/XaverD1992)
- [**Дмитрий Истомин**](https://github.com/vhg860)
