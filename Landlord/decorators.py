from django.shortcuts import redirect


def landlord_required(view_func):
 def wrapper(request, *args, **kwargs):
  if hasattr(request.user, "landlord"):
   return view_func(request, *args, **kwargs)
  return redirect("landlord_login")
 return wrapper