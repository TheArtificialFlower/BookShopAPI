from rest_framework.views import Response, APIView
from permissions import IsNotAuthenticated, SessionPermission
from rest_framework import status
from .serializers import UserRegisterSerializer, UserManagementSerializer, OtpSerializer
from utils import send_otp_email
from .models import User, OtpCode
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from datetime import datetime, timedelta
import pytz, random


class UserRegisterView(APIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (IsNotAuthenticated,)
    throttle_scope = "register"

    def post(self, request):
        serializer = self.serializer_class(data=request.POST)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            request.session["user"] = serializer.validated_data
            random_code = random.randint(1000, 9999)
            # send_mail function should be added here.
            OtpCode.objects.filter(code=random_code, email=email).delete()
            otp = OtpCode.objects.create(code=random_code, email=email)
            return Response({"temp_msg": f"{otp.code}"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OtpConfirmView(APIView):
    serializer_class = OtpSerializer
    permission_classes = (IsNotAuthenticated, SessionPermission)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_data = request.session.get("user")
        email, code = user_data["email"], serializer.validated_data["code"]
        otp = OtpCode.objects.filter(email=email, code=code).first()

        if not otp:
            return Response({"message": "Code is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.now(tz=pytz.timezone('Asia/Tehran'))
        if now > otp.created + timedelta(minutes=2):
            otp.delete()
            return Response({"message": "Code has expired, please try again."}, status=status.HTTP_400_BAD_REQUEST)

        user_data.pop("password2", None)
        User.objects.create_user(**user_data)
        otp.delete()
        user_data.pop("password", None)

        return Response(user_data, status=status.HTTP_201_CREATED)



class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserManagementSerializer

    def get_object(self):
        return self.request.user


