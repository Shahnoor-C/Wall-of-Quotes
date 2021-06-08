from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages

def home(request):
    return render (request,"home.html")

def register(request):
    print("****************")
    print(request.POST)
    print("****************")
    
    
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print("**********", errorsFromValidator)

    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request,value )
        return redirect("/")

    
    newUser= User.objects.create(firstName= request.POST['firstname'], lastName=request.POST['lastname'],email=request.POST['email'],password=request.POST['password'])
    
    request.session['loggedinUserid'] = newUser.id # The session variable is availble throught out the application

    return redirect("/quotes")

def quotes(request):
    
    if 'loggedinUserid'not in request.session:
        return redirect("/")

    context = {
        'loggedinUser': User.objects.get(id=request.session['loggedinUserid']),
        'allQuotes': Quote.objects.all()
    }
    
    
    return render(request, "quotes.html",context)
    
def logout(request):
    request.session.clear()
    return redirect("/")

def login(request):
    print(request.POST)
    errorsFromValidator = User.objects.loginValidator(request.POST)
    print("*******printing login error here",errorsFromValidator)
    if len(errorsFromValidator) > 0:
        for key,value in errorsFromValidator.items():
            messages.error(request,value )
        return redirect("/")
    matchingemail = User.objects.filter(email=request.POST['email'])
    request.session['loggedinUserid'] =matchingemail[0].id

    return redirect("/quotes")

def addQuote(request):
    print("***********")
    print(request.POST)
    print("***********")
    errorsFromValidator = Quote.objects.quoteValidator(request.POST)
    print("ERRORS HERE>>>>>>>>>>>", errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key,value in errorsFromValidator.items():
            messages.error(request,value)
        return redirect("/quotes")
    
    
    Quote.objects.create(author=request.POST['author'],description=request.POST['quote'],user_who_uploaded= User.objects.get(id=request.session['loggedinUserid']))

    return redirect("/quotes")

def quoteInfo(request,quoteid):
    context = {
        'quoteObj':Quote.objects.get(id=quoteid),
        'loggedinuser':User.objects.get(id=request.session['loggedinUserid'])
    }
    
    return render(request,"quote.html",context)


def deleteQuote(request,quoteid):
    quoteDelete= Quote.objects.get(id=quoteid)
    quoteDelete.delete()
    return redirect("/quotes")

def showUser(request,userwhouploadedid):
    context = {
        'user':User.objects.get(id=userwhouploadedid),
       
        
    }
    
    return render(request,"userdetails.html",context)

def edditAccount(request,loggedinuserid):
    
    context={
        "editUser":User.objects.get(id=loggedinuserid)
    }
    
    return render(request,"editAccount.html",context)

def updateAccount(request,loggedinuserid):
    print("***************")
    print(request.POST)
    print("***************")
    # errorsFromValidator = User.objects.edditAccountValidator(request.POST)
    
    # if len(errorsFromValidator)>0:
    #     for key,value in errorsFromValidator.items():
    #         messages.error(request,value)
    #     return redirect("/quotes")
    
    c = User.objects.get(id=loggedinuserid)
    c.firstName = request.POST['firstname']
    c.LastName = request.POST['lastname']
    c.email = request.POST['email']
    c.save()
    return redirect("/quotes")



