from django.shortcuts import render
# from django.shortcuts import render_to_response
from django.template import loader,RequestContext
from django.http import HttpResponse,HttpResponseRedirect
# from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from . import database as db
from functools import wraps
import os
import re
from . import upload

def remove_newline_chars(input_str):
    return input_str.replace("\n", "")

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' not in request.session:
            login_url = f'/login/?next={request.path}'  # Add the 'next' parameter to the login URL
            return HttpResponseRedirect(login_url)
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def home(request):
  if 'id' not in request.session:
    template = loader.get_template('index.html')
    return HttpResponse(template.render())
  else:
    return HttpResponseRedirect('/dashboard/')

def signup(request):
  template = loader.get_template('signup.html')
  return HttpResponse(template.render())

def signin(request):
  template = loader.get_template('signin.html')
  return HttpResponse(template.render())

@csrf_exempt
def register(request):
  if request.method == 'POST':
    try:
      fullname = request.POST['full_name']
      username = request.POST['user_name']
      email = request.POST['email']
      country = request.POST['country']
      birthdate = request.POST['bdate']
      password = request.POST['password']
      db.register(fullname,username,email,country,birthdate,password)
      return HttpResponse("<script>alert('User successfully registered You can log in now!');location.href='/login';</script>")
    except db.pymysql.IntegrityError:
      return HttpResponse("<script>alert('username or email already taken');location.href='/signup';</script>")
    except:
      return HttpResponse("<script>alert('Unknown error occured while creating account');location.href='/signup';</script>")
  else:
    return HttpResponse("Method not allowed"),405
  
@csrf_exempt
def saveSession(request):
  if request.method == 'POST':
    email = request.POST['email']
    password = request.POST['password']
    userdata = db.login(email,password)
    if userdata:
      request.session['id'] = userdata[0]
      return HttpResponseRedirect("/dashboard/")
    else:
      return HttpResponse("<script>alert('Invalid credentials or user is not found');location.href='/login';</script>")
  else:
    return HttpResponse("Method not allowed"),405
  
@custom_login_required
def dashboard(request):
  userinfo = db.userinfo(request.session['id'])
  recipe_list = db.foodrecipes()
  context = {
    'info':userinfo,
    'recipes':recipe_list
  }
  return render(request,'dashboard.html',context)

def logout_view(request):
    request.session.flush()
    return HttpResponseRedirect("/")
    # Redirect to some page or return response

@custom_login_required
@csrf_exempt
def addrecipeform(request):
        userinfo = db.userinfo(request.session['id'])
        context = {
        'info':userinfo
      }
        return render(request,'add_recipe_form.html',context)

@custom_login_required
@csrf_exempt
def addrecipe(request):
   if request.method == "POST":
      title = request.POST['title']
      steps = request.POST['steps']
      ingredients = request.POST['ingredients']
      image = request.FILES['image']
      imgpath = upload.upload_image_to_imgbb(image)
      ingredients = remove_newline_chars(ingredients)
      db.addrecipes(title,steps,imgpath,request.session['id'],ingredients)
      return HttpResponse("<script>alert('Recipe added!');location.href='/';</script>")
   else:
      return HttpResponse("Method not allowed"),405
   

def recipeInfo(request):
   try:
      recipeid = request.GET.get('id')
      userinfo = db.userinfo(request.session.get('id'))
      if recipeid:
          recinfo = db.recipe_info(recipeid)
          context = {
            'recinfo':recinfo,
            'info':userinfo,
            'session':request.session.get('id'),
            'about_user':db.userinfo(recinfo[4]),
            'steps':recinfo[2].split(",")
          }
          return render(request,'recipe_info.html',context)
      else:
          return HttpResponse("<p>Recipe not found</p><a href='/'>Go back home</a>")
   except:
      return HttpResponse("<p>Recipe not found</p><a href='/'>Go back home</a>")
   

@custom_login_required
def manage_recipes(request):
  userinfo = db.userinfo(request.session['id'])
  recipe_list = db.foodrecipes(request.session['id'])
  context = {
    'info':userinfo,
    'recipes':recipe_list
  }
  return render(request,'manage_recipe.html',context)

@custom_login_required
@csrf_exempt
def delete_recipe(request):
   recipe_id = request.POST['recipe-id']
   db.deleterecipe(recipe_id)
   return HttpResponse("<script>alert('Recipe deleted!');location.href='/manage/recipe';</script>")


def comments(request,recipeid):
   try:
      userinfo = db.userinfo(request.session.get('id'))
      if recipeid:
          recinfo = db.recipe_info(recipeid)
          comment_list = db.comments(recipeid)
          context = {
            'recinfo':recinfo,
            'info':userinfo,
            'session':request.session.get('id'),
            'about_user':db.userinfo(recinfo[4]),
            'steps':recinfo[2].split(","),
            'comments':comment_list
          }
          return render(request,'comments.html',context)
      else:
          return HttpResponse("<p>Recipe not found</p><a href='/'>Go back home</a>")
   except:
      return HttpResponse("<p>Recipe not found</p><a href='/'>Go back home</a>")
   
@custom_login_required
@csrf_exempt
def raterecipe(request):
   recipe = request.POST['recipe']
   stars = int(request.POST['stars'])
   comment = request.POST['comment']
   status = db.rate_recipe(stars,comment,recipe,request.session['id'])
   if status == 'new':
      return HttpResponse("<script>alert('Comment shared with the owner!');location.href='/';</script>")
   else:
      return HttpResponse("<script>alert('You overwritten your previous comment');location.href='/';</script>")