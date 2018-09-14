from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
class MyMiddleware(MiddlewareMixin):
    def process_request(self,request):
        if 'adress_page'in request.path:
            print(request.path)
            if request.session.get('user_name'):
                return
            else:
                request.session['logined']='1'
                return redirect('user_app:login_page')

