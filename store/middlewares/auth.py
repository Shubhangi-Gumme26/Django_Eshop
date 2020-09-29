from django.shortcuts import redirect

def auth_middleware(get_response):
    def middleware(request):
        returnUrl = request.META['PATH_INFO']          #/store/cart
        print(request.META['PATH_INFO'])
        if not request.session.get('customer_session_id'):
            return redirect(f'login?return_url={returnUrl}')        #insted of return_url word we can write anything, login is login page url
        #    return redirect(f'login?return_url={returnUrl')
        response = get_response(request)
        return response
    return middleware

# def auth_middleware(get_response):
#     def middleware(request):
#         print("hi middlewate")
#         print(request.session.get('customer_session_id'))
#         if not request.session.get('customer_session_id'):
#             return redirect('LoginPage')        #insted of return_url we can write anything
#         response = get_response(request)
#         return response
#     return middleware
