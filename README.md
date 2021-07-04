# Доп. документация к Api

Удобный интерфейс для тестирования api на главной странице:
    Swagger url '/'
    Redoc url '/redoc/'
    
    Там есть примеры запрсов  get/post/put и все что вам нужно )
    
Warning: 
  Если хотите протестить api/v1/interview/{id}/interview/ в swagger или redoc !
    Это url для теста опроса в нем именно в post нужно будет писать json ручками по техническим причинам 
    
    

# Важные моменты и примеры запросов 

1) api/v1/interview/{id}/interview/ - url Прохождения опроса

        Пример запроса:
            {
                "user": 1,
                "anonymously": false,
                "answers": [
                    {
                       
                        "choices": [1]  (id варианта ответа),

                        "question": {
                                    "id": 1,
                                    "question_type": 1 (0-ответ текстом, 1-ответ с выбором одного варианта, 2-ответ с выбором нескольких вариантов)

                                     },
                   },
  
              ]
            }
            
        
- Один обьект answer один в данном случае т.е ответ на один вопрос
- question_type нужно передавать для того чтобы запросы не клонировались


2) /api/v1/user/ - url Для регистрации пользователей
3) /api/v1/rest-auth/  login/logout  Для входа и выхода из системы
  Пример запроса: 
  {
    "username": "string",
    "password": "string"
  }
  
  В ответ получите обьект пользователя и токен
 
4) также после добавления start_time в интервью 
  create/update/delete его запросов пропадает


# Инструкция по разворачиванию проекта у себя на компьютере
    
    1) В проекте используется база данных postgresql поэтому надо ее создать
        CREATE DATABASE test_task_db;
    
    2) Провести миграции:
        Приложения указать обязательно !
        python manage.py makemigrations interview user
        python manage.py migrate
    
    3) Создать пользователя:
        python manage.py createsuperuser 
        
    4) Запустить проект
        python manage.py runserver
        
Наслждайтесь :)
