# Sample_Code_python
1. Python  Register is a module developed to provide basic user authentication.
2. Python Register can only be used to register users with the following information:
    1. CompanyName
    2. Firstname
    3. Email
    4. Country code
    5. Phone
    6. Password
    7. Address
3. How to Use.
    1. Create a user
        a. The creation of a user is quite simple.
        b. This line is used to create user
        (customer_obj = theuser.objects.create(user = user_obj, firstname = firstname_val,
        email = email_val, countrycode = countrycode_val, phone = phone_val, emailverificationlink = baselink))
    2. User Properties
        a. The User object now has some accessible properties. These are the CompanyName, Firstname, Email, Countrycode, and Password properties. These can be called variables to the object so
        # Call User Information
        customer_obj.firstname
        customer_obj.email
        customer_obj.countrycode
    3. User Validation
      a. Check if a user exists
      #Code
      customer_emailverified_obj = theuser.objects.filter(user = user_obj, emailverified = True)
      #if already registered email return User already exist
      if customer_emailverified_obj:
        return JsonResponse({'status_code': 409, 'status_message': 'User already exists.'})
      b. Above line check user email already registered or not

    4. Create a user unique id
      a. Create a user unique id so that it can be accessed and interacted with.
