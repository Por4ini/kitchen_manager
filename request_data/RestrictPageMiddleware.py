from django.shortcuts import HttpResponse, redirect


class RestrictPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # перевіряємо, чи є користувач автентифікованим
        if request.user.is_authenticated:
            # перевіряємо, чи має користувач зі значенням last_name='provider' доступ до поточної сторінки
            if request.user.last_name == 'Provider' and request.path != '/provider/personal_office'\
                    and request.path != '/users/login/' and request.path != '/users/logout/':
                return redirect('office')

        # якщо користувач пройшов перевірку, передаємо запит до view
        response = self.get_response(request)

        return response
