from django.db import models
import re

class UserManager(models.Manager):
    def registrationValidator(self,formInfo):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        emailTaken= User.objects.filter(email = formInfo['email']) 
    
        errors = {}
        if len(formInfo['firstname']) == 0:
            errors['firstnamereq'] = "Please provide a first name!"
        elif len(formInfo['firstname']) < 2:
            errors['lenfirstname'] = "First name must be at least 2 characters long!"
        
        if len(formInfo['lastname']) == 0:
            errors['lastnamereq'] = "Please provide a last name!"
        elif len(formInfo['lastname']) < 2:
            errors['lenlastname'] = "First name must be at least 2 characters long!"
        
        if len(formInfo['email']) == 0:
            errors['emailreq'] = "Please provide an email!"
        elif not EMAIL_REGEX.match(formInfo['email']):
            errors['emailerror'] = "Email must be valid!"
        
        elif len(emailTaken) > 0:
            errors['emailtaken'] = "The email provided is already associated with another account please try again"
        
        if len(formInfo['password']) == 0:
            errors['passwordreq'] = "Please provide a password"
        elif len(formInfo['password']) < 8:
            errors['lenpassword'] = "Password must be at least 8 characters long!"        
        
        if formInfo['password']!= formInfo['cpw']:
            errors['pwnomatch'] = "Passwords do not match please try again!"

        return errors
    
    
    def loginValidator(self,forminfo):
        errors = {}
        matchingEmail = User.objects.filter(email=forminfo['email'])
        if len(matchingEmail) == 0:
            errors['emailnotfound'] = "This email is not found please register first"
        elif len(forminfo['email']) == 0:
            errors['len_emailerror'] =  "This email is not found please register first"
        # print( "Matching meail here!!",matchingEmail)
        
        elif matchingEmail[0].password != forminfo['password']:
            errors['pwIncorrect'] = "Incorrect password please try again"
        return errors
    
    # def edditAccountValidator(self,formInfo):
    #     errors = {}
    #     if len(formInfo['firstname']) == 0:
    #         errors['firstnamereq'] = "Please provide a first name!"
    #     return errors


class QuoteManager(models.Manager):
    def quoteValidator(self,formInfo):
        errors={}
        if len(formInfo['author']) == 0:
            errors['authorReq'] = "An author is required!"
        elif len(formInfo['author']) < 3:
            errors['lenAuthorReq'] = "Author must be at least 3 characters long!"
        if len(formInfo['quote']) == 0:
            errors['quoteReq'] = "A quote is required!"
        elif len(formInfo['quote']) < 10:
            errors['lenQuoteReq'] = "Quote must be at least 10 characters long!"

        return errors

class User(models.Model):
    firstName = models.CharField(max_length = 255)
    lastName = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Quote(models.Model):
    author = models.CharField(max_length=255)
    description = models.CharField(max_length = 255)
    user_who_uploaded= models.ForeignKey(User, related_name="quotes_uploaded" ,on_delete=models.CASCADE)
    users_who_like =models.ManyToManyField(User,related_name="liked_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()


