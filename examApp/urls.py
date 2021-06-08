#from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path("",views.home),
    path("register",views.register),
    path("quotes",views.quotes),
    path("logout",views.logout),
    path("login",views.login),
    path("addQuote",views.addQuote),
    path("quotes/<int:quoteid>",views.quoteInfo),
    path("quotes/<int:quoteid>/delete",views.deleteQuote),
    
    path("showUser/<int:userwhouploadedid>",views.showUser),
    
    path("user/<int:loggedinuserid>",views.edditAccount),
    path("user/edit/<int:loggedinuserid>",views.updateAccount),
    
]
