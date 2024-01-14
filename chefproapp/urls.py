from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='members'),
    path('signup/',views.signup,name="signup"),
    path('login/',views.signin,name="signin"),
    path('register/',views.register,name="register"),
    path('savesession',views.saveSession,name="savesession"),
    path('dashboard/',views.dashboard,name="user dashboard"),
    path('add/recipe/',views.addrecipeform,name="recipe form"),
    path('addrecipe/',views.addrecipe,name="Post recipe"),
    path('recipe/',views.recipeInfo,name="About the recipe"),
    path('manage/recipe/',views.manage_recipes,name="manage recipe"),
    path('deleterecipe/',views.delete_recipe,name="Delete recipe"),
    path('comments/<recipeid>',views.comments,name="comments"),
    path('rate/',views.raterecipe,name="RATING"),
    path('logout/',views.logout_view,name="logout")
]