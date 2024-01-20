from accounts.models import UserTokens
from datetime import timedelta, timezone
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate 
from rest_framework import status
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserTokens




class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            email = validated_data['email']
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                return Response({"error": "User with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create(email=email)

            user.set_password(validated_data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email and password:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                print("Authentication failed. Invalid credentials.")
        
        return Response({'detail': 'Authentication failed. Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "You have been logged out successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"message": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        #take email from request
        email = request.data.get('email')

        # check if user with the email exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        # generate token
        token = default_token_generator.make_token(user)
        user_token = UserTokens(password_reset_token=token,user=user)
        user_token.save()

        # send mail
        mail_subject = "Reset your password"
        message = f"This token will work as the old password while password resetting : {token}"
        send_mail(
            mail_subject,
            message,
            "from@example.com",
            email,
            fail_silently=False,
        )
        return Response({"detail": "Password reset email sent successfully."}, status=status.HTTP_200_OK)

class SetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        token_from_request = request.data.get('token')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')

        if new_password == confirm_new_password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            # Check if the token is valid 
            UserTokens.objects.get()
            if user.password_reset_token and default_token_generator.check_token(user, token):
                token_creation_time = user.password_reset_token_created_at
                expiration_time = token_creation_time + timedelta(minutes=5)

                if timezone.now() <= expiration_time:
                    # Token is valid and within the 5-minute window.
                    user.set_password(new_password)
                    user.save()
                    return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
            
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"new passowrd and confirm new password dosen't match"}, status=status.HTTP_400_BAD_REQUEST)
            
class SetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        confirm_new_password = request.data.get('confirm_new_password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if new_password == confirm_new_password:
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"new passowrd and confirm new password dosen't match"}, status=status.HTTP_400_BAD_REQUEST)
        
# class PasswordResetView(APIView):
#     def post(self, request):
#         token = request.data.get('token')
#         password = request.data.get('password') 
#         email = request.data.get("email")
#         # Send email
#         subject = 'Forgot password reset password now'
#         message = f'A new student named {user.name} with email {student.email} has been created.'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = ['n.pradip101@gmail.com']

#         # send mail with template
#         context = {"name":f"{student.name}","email":f"{student.email}","roll_no": f"{student.roll_number}"}
#         html_content = render_to_string('student_creation_email.html',context)
#         text_content = strip_tags(html_content)

#         email = EmailMultiAlternatives(
#             subject,
#             text_content,
#             settings.EMAIL_HOST_USER,
#             recipient_list,
#         )
#         email.attach_alternative(html_content,'text/html')
#         email.send()

class GenerateVerificationLink(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=400)

        # Generate a verification token
        token = default_token_generator.make_token(user)

        # Save the token to the UserTokens model
        user_token, created = UserTokens.objects.get_or_create(user=user)
        user_token.password_reset_token = token
        user_token.save()

        # Create a verification link with the token
        verification_url = reverse('verify-email')
        params = urlencode({'email': email, 'token': token})
        full_verification_url = f"{verification_url}?{params}"

        # Send the verification link in an email
        subject = "Email Verification Link"
        message = f"Click the following link to verify your email: {full_verification_url}"
        from_email = "n.pradip101@gmail.com"  
        recipient_list = ['n.pradip101@gmail.com']

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({"detail": "Verification link sent to your email."}, status=200)
    
class VerifyEmail(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        token = request.query_params.get('token')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User with this email does not exist."}, status=400)

        user_token = UserTokens.objects.get(user=user)
        
        # Check if the token matches
        if user_token.password_reset_token and default_token_generator.check_token(user, token):
            # Token is valid, mark the user as email verified
            user.is_email_verified = True
            user.save()
            return Response({"detail": "Email verification successful."}, status=200)
        else:
            return Response({"detail": "Invalid or expired token."}, status=400)