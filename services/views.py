from django.http import HttpResponse

# Временный список услуг вместо базы данных
SERVICES_LIST = [
    {'id': 1, 'name': 'Веб-разработка', 'description': 'Создание современных веб-сайтов', 'price': 5000},
    {'id': 2, 'name': 'SEO-оптимизация', 'description': 'Продвижение в поисковых системах', 'price': 3000},
    {'id': 3, 'name': 'Дизайн логотипа', 'description': 'Разработка уникального логотипа', 'price': 1500},
    {'id': 4, 'name': 'Контекстная реклама', 'description': 'Настройка и ведение рекламных кампаний', 'price': 4000},
]

def home_page(request):
    """Главная страница"""
    return HttpResponse("""
    <h1>Добро пожаловать в ServiceHub!</h1>
    <p>Лучший сервис по подбору услуг для вашего бизнеса</p>
    <nav>
        <ul>
            <li><a href="/catalog/">📋 Каталог услуг</a></li>
            <li><a href="/profile/">👤 Личный кабинет</a></li>
            <li><a href="/cart/">🛒 Корзина</a></li>
            <li><a href="/settings/">⚙️ Настройки</a></li>
            <li><a href="/about/">ℹ️ О нас</a></li>
        </ul>
    </nav>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        nav ul { list-style: none; padding: 0; }
        nav li { margin: 10px 0; }
        nav a { text-decoration: none; color: #007bff; font-size: 18px; }
        nav a:hover { color: #0056b3; }
    </style>
    """)

def catalog_page(request):
    """Страница каталога услуг"""
    services_html = """
    <h1>🎯 Каталог услуг</h1>
    <div style="display: grid; gap: 15px; margin: 20px 0;">
    """
    
    for service in SERVICES_LIST:
        services_html += f"""
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 8px;">
            <h3>{service['name']}</h3>
            <p>{service['description']}</p>
            <p><strong>Цена: {service['price']} руб.</strong></p>
            <a href="/service/{service['id']}/" style="background: #007bff; color: white; padding: 8px 15px; text-decoration: none; border-radius: 4px;">Подробнее</a>
        </div>
        """
    
    services_html += """
    </div>
    <a href="/">← На главную</a>
    """
    return HttpResponse(services_html)

def service_detail(request, service_id):
    """Страница просмотра услуги по ID"""
    service = next((s for s in SERVICES_LIST if s['id'] == service_id), None)
    
    if service is None:
        return HttpResponse("""
        <h1>❌ Услуга не найдена</h1>
        <p>Запрошенная услуга не существует.</p>
        <a href="/catalog/">Вернуться в каталог</a>
        """, status=404)
    
    html_response = f"""
    <h1>{service['name']}</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <p><strong>📝 Описание:</strong> {service['description']}</p>
        <p><strong>💰 Цена:</strong> {service['price']} руб.</p>
        <p><strong>🆔 ID услуги:</strong> {service['id']}</p>
    </div>
    <button style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer;">Добавить в корзину</button>
    <br><br>
    <a href="/catalog/">← Назад в каталог</a> | <a href="/">На главную</a>
    """
    return HttpResponse(html_response)

def user_profile(request):
    """Страница личного кабинета"""
    return HttpResponse("""
    <h1>👤 Личный кабинет</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>Ваши данные:</h3>
        <p><strong>Имя:</strong> Иван Иванов</p>
        <p><strong>Email:</strong> ivan@example.com</p>
        <p><strong>Телефон:</strong> +7 (999) 999-99-99</p>
    </div>
    <h3>История заказов:</h3>
    <ul>
        <li>Веб-разработка - 5000 руб. (12.12.2023)</li>
        <li>SEO-оптимизация - 3000 руб. (10.12.2023)</li>
    </ul>
    <a href="/">← На главную</a>
    """)

def cart_page(request):
    """Страница корзины"""
    return HttpResponse("""
    <h1>🛒 Корзина</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>Ваши выбранные услуги:</h3>
        <ul>
            <li>Дизайн логотипа - 1500 руб. <button style="margin-left: 10px; background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Удалить</button></li>
            <li>Контекстная реклама - 4000 руб. <button style="margin-left: 10px; background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Удалить</button></li>
        </ul>
        <hr>
        <h4>Итого: 5500 руб.</h4>
        <button style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px;">Оформить заказ</button>
    </div>
    <a href="/catalog/">← Продолжить покупки</a> | <a href="/">На главную</a>
    """)

def settings_page(request):
    """Страница настроек"""
    return HttpResponse("""
    <h1>⚙️ Настройки</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; max-width: 500px;">
        <h3>Настройки аккаунта:</h3>
        <form>
            <label style="display: block; margin: 10px 0;">
                <strong>Имя:</strong><br>
                <input type="text" value="Иван" style="padding: 8px; width: 100%; margin-top: 5px;">
            </label>
            <label style="display: block; margin: 10px 0;">
                <strong>Email:</strong><br>
                <input type="email" value="ivan@example.com" style="padding: 8px; width: 100%; margin-top: 5px;">
            </label>
            <label style="display: block; margin: 10px 0;">
                <strong>Уведомления:</strong><br>
                <input type="checkbox" checked> Email-уведомления
                <input type="checkbox" checked> SMS-уведомления
            </label>
            <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px;">Сохранить изменения</button>
        </form>
    </div>
    <a href="/">← На главную</a>
    """)

def about_page(request):
    """Дополнительная страница О нас"""
    return HttpResponse("""
    <h1>ℹ️ О нас</h1>
    <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3>ServiceHub - ваш надежный партнер</h3>
        <p>Мы предоставляем качественные услуги для бизнеса с 2020 года.</p>
        <p><strong>Наши преимущества:</strong></p>
        <ul>
            <li>✅ Более 1000 довольных клиентов</li>
            <li>✅ Гарантия качества услуг</li>
            <li>✅ Круглосуточная поддержка</li>
            <li>✅ Гибкая система скидок</li>
        </ul>
        <p><strong>Контакты:</strong></p>
        <p>📞 Телефон: +7 (495) 123-45-67</p>
        <p>📧 Email: info@servicehub.ru</p>
        <p>📍 Адрес: Москва, ул. Примерная, д. 123</p>
    </div>
    <a href="/">← На главную</a>
    """)