from django.shortcuts import redirect


def renter_required(view_func):
 def wrapper(request, *args, **kwargs):
  if hasattr(request.user, "renter"):
   return view_func(request, *args, **kwargs)
  return redirect('renter_login')
 return wrapper


