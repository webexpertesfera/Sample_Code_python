#Create a Class-based views for user registration
class userRegistration(TemplateView):
	template_name = 'userRegistration.html'

	def post(self, request, *args, **kwargs):
		'''This class saves the registration details of customer or company users'''
		try:
			companyName_val = request.POST.get('companyName')
			if not companyName_val:
				companyName_val=''
			firstname_val = request.POST.get('firstname')
			if not firstname_val:
				return JsonResponse({'status_code': 0, 'status_message': 'First Name is required'})
			lastname_val = request.POST.get('lastname')
			if not lastname_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Last Name is required'})
			email_val = request.POST.get('email')
			if not email_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Email Address is required'})
			countrycode_val = request.POST.get('countrycode')
			if not countrycode_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Countrycode is required'})
			if '+' not in countrycode_val:
				countrycode_val = '+' + countrycode_val
			phone_val = request.POST.get('phone')
			if not phone_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Phone number is required'})
			password_val = request.POST.get('password')
			if not password_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Password is required'})
			address_val = request.POST.get('address')
			if not address_val:
				return JsonResponse({'status_code': 0, 'status_message': 'Address is required'})
			user_obj = User.objects.filter(username = email_val).first()

      #Check user email already registered or not.
			if user_obj:
				try:
					customer_emailverified_obj = theuser.objects.filter(user = user_obj, emailverified = True)
          #if already registered email return User already exist
					if customer_emailverified_obj:
						return JsonResponse({'status_code': 409, 'status_message': 'User already exists.'})

					customer_emailnotverified_obj = company.objects.filter(user = user_obj, emailverified = False)
					if customer_emailnotverified_obj:
						return JsonResponse({'status_code' : 200, 'status_message' : 'A verification link has been sent to your email address earlier. Please search your mail inbox.'})
					else:
						return JsonResponse({'status_code': 409, 'status_message': 'A user with this email address already exists.'})
				except Exception as e:
					print(e)
					return JsonResponse({'status_code': 409, 'status_message': 'User exists.'})
			else:
				user_obj = User.objects.create_user(username = email_val, email = email_val, password = password_val)
        #Create a unique link for verify account
				st = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
				baselink = '/user/' + 'user' + '/verify/' + str(user_obj.email) + '/' + st
				completelink = str(settings.WEB_BASE_URL) + baselink
				message = "\nVerify your account through following link:\n" + completelink

        #Send verification link to user email id for verify account
				try:
					subject='Registeration'
					message = render_to_string('registerationVerificationLinkMail.html', {
						'name': str(firstname_val),
						'url': str(completelink),
						})
					fromEmail = str(settings.EMAIL_HOST_USER)
					toEmail = str(email_val)
					message = EmailMessage(subject, message, fromEmail, [toEmail])
					message.content_subtype = 'html'
					message.send()
				except Exception as e:
					print(e)

				beforeNameOfCompany=request.POST.get('firstname')
				beforeNameOfCompany=beforeNameOfCompany.replace(' ','')
				name3Letter=beforeNameOfCompany[0:3]
				name3Letter=name3Letter.upper()
				latExt=theuser.objects.all().last()
        #create a user unique id
				if latExt:
					lastId=latExt.userID
					last5Number=lastId[3:]
					last5Number=int(last5Number)
					new5Number=last5Number+1
					new5Number=str(new5Number)
					new5Number = new5Number.zfill(5)
					theUniqueID=str(name3Letter)+str(new5Number)
				else:
					theUniqueID=str(name3Letter)+str('00001')
        #create customer
				customer_obj = theuser.objects.create(user = user_obj, firstname = firstname_val, email = email_val, countrycode = countrycode_val, phone = phone_val, emailverificationlink = baselink)
				if customer_obj:
        #if customer created update below fields
					customer_obj.lastname=lastname_val
					customer_obj.companyname=companyName_val
					customer_obj.userID=theUniqueID
					customer_obj.address=address_val
					customer_obj.save()

				try:
					from datetime import datetime
					now = datetime.now() # current date and time
					dat = now.strftime("%b %d,%Y")
					tim = now.strftime("%H:%M %p")
					theSuperObject=superadmin.objects.all().first()
          #Create notification for admin
					if theSuperObject:
						message='A new user '+str(customer_obj.firstname)+' has been registered.'
						adminnotifications.objects.create(admin=theSuperObject,title='User Register',message=message,date=dat,time=tim)
				except Exception as e:
					print(e)

				return JsonResponse({'status_code' : 200, 'status_message' : 'A verification link has been sent to your email address.'})
		except Exception as e:
			print(e)
			return JsonResponse({'status_code': 0, 'status_message': 'Internal Server Error'})
