from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .models import Programs, Signature, Student, Clearance, StudentClearance, ClearanceSignature
from .serializers import ClearanceSignatureSerializer, StudentClearanceSerializer, ClearanceCreateSerializer, ProgramsSerializer, ClearanceSerializer, UserRegistrationSerializer, SignatureSerializer, UserSerializer, StudentSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class GetUserByIdView(APIView):
    permission_classes = [AllowAny]  # ✅ Works in class-based views like this

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class ProgramsListAPIView(generics.ListAPIView):
    queryset = Programs.objects.all().order_by('created_at')
    serializer_class = ProgramsSerializer
    permission_classes = [AllowAny]


class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SignatureUploadView(generics.CreateAPIView):
    queryset = Signature.objects.all()
    serializer_class = SignatureSerializer


    
class SignatureDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, staff_id):
        try:
            signature = Signature.objects.get(staff_id=staff_id)
            serializer = SignatureSerializer(signature)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Signature.DoesNotExist:
            return Response({'detail': 'No signature found for this staff.'}, status=status.HTTP_404_NOT_FOUND)
        

class StudentDetailByUserIdView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, user_id):
        try:
            student = Student.objects.select_related('user').get(user__id=user_id)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        
class ClearanceListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Clearance.objects.all()
    serializer_class = ClearanceSerializer
    
    
class LatestClearanceView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        latest_clearance = Clearance.objects.order_by('-created_at').first()
        if not latest_clearance:
            return Response({'detail': 'No clearance found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ClearanceSerializer(latest_clearance)
        return Response(serializer.data, status=status.HTTP_200_OK)    


class ClearanceCreateView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ClearanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            clearance = serializer.save()
            return Response({
                'message': 'Clearance created with all programs.',
                'clearance': ClearanceCreateSerializer(clearance).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClearanceDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            clearance = Clearance.objects.get(id=id)
            serializer = ClearanceSerializer(clearance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Clearance.DoesNotExist:
            return Response({'error': 'Clearance not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class RequestLatestClearanceView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        student_id = request.data.get("student_id")
        try:
            student = User.objects.get(id=student_id)
        except User.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

        latest_clearance = Clearance.objects.order_by('-created_at').first()

        if not latest_clearance:
            return Response({"error": "No clearance available."}, status=status.HTTP_404_NOT_FOUND)

        exists = StudentClearance.objects.filter(student=student, clearance=latest_clearance).exists()
        if exists:
            return Response({"message": "Already requested."}, status=status.HTTP_400_BAD_REQUEST)

        student_clearance = StudentClearance.objects.create(
            student=student,
            clearance=latest_clearance,
        )
        serializer = StudentClearanceSerializer(student_clearance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
class StudentClearanceByStudentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, student_id):
        # Get the latest clearance based on created_at
        latest_clearance = Clearance.objects.order_by('-created_at').first()
        if not latest_clearance:
            return Response({'detail': 'No clearance records found.'}, status=status.HTTP_404_NOT_FOUND)

        # Filter student clearances matching latest clearance's academic year and semester
        student_clearances = StudentClearance.objects.filter(
            student_id=student_id,
            clearance__academic_year=latest_clearance.academic_year,
            clearance__semester=latest_clearance.semester
        )

        if not student_clearances.exists():
            return Response({'detail': 'No clearance records found for this student matching the latest clearance.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentClearanceSerializer(student_clearances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentClearanceListView(APIView):
    permission_classes = [AllowAny]  

    def get(self, request):
        student_clearances = StudentClearance.objects.select_related('student', 'clearance').order_by('-clearance__created_at')
        serializer = StudentClearanceSerializer(student_clearances, many=True)
        return Response(serializer.data)
    
    
class UpdateStudentClearanceStatus(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, pk):
        try:
            clearance = StudentClearance.objects.get(pk=pk)
        except StudentClearance.DoesNotExist:
            return Response({"error": "Clearance not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in ["Approved", "Pending", "Rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        clearance.status = new_status
        clearance.save()
        return Response(StudentClearanceSerializer(clearance).data)
    
    
class ClearanceSignatureCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, student_id, program_id):
        try:
            student = User.objects.get(id=student_id)
            program = Programs.objects.get(id=program_id)
        except User.DoesNotExist:
            return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)
        except Programs.DoesNotExist:
            return Response({"error": "Program not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Find the latest StudentClearance for this student
            student_clearance = StudentClearance.objects.filter(student=student).latest('id')
        except StudentClearance.DoesNotExist:
            return Response({"error": "Student clearance not found."}, status=status.HTTP_404_NOT_FOUND)

        signature_id = request.data.get("signature_id")
        signature = None
        if signature_id:
            try:
                signature = Signature.objects.get(id=signature_id)
            except Signature.DoesNotExist:
                return Response({"error": "Signature not found."}, status=status.HTTP_404_NOT_FOUND)

        clearance_signature = ClearanceSignature.objects.create(
            student=student,
            clearance=student_clearance,
            programs=program,
            signature=signature,
            status=request.data.get("status", "Pending"),
            feedback=request.data.get("feedback", "")
        )

        serializer = ClearanceSignatureSerializer(clearance_signature)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    

class GetClearanceSignatureView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, student_id, program_id):
        try:
            student = User.objects.get(id=student_id)
            program = Programs.objects.get(id=program_id)
        except User.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Programs.DoesNotExist:
            return Response({"error": "Program not found"}, status=status.HTTP_404_NOT_FOUND)

        signature = ClearanceSignature.objects.filter(student=student, programs=program).first()

        if not signature:
            return Response({"message": "No signature yet"}, status=status.HTTP_200_OK)

        serializer = ClearanceSignatureSerializer(signature)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class ClearanceSignatureListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        signatures = ClearanceSignature.objects.all()
        serializer = ClearanceSignatureSerializer(signatures, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class UpdateClearanceSignatureStatusView(APIView):
    permission_classes = [AllowAny]

    def patch(self, request, signature_id):
        try:
            clearance_signature = ClearanceSignature.objects.get(id=signature_id)
        except ClearanceSignature.DoesNotExist:
            return Response({"error": "ClearanceSignature not found."}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        staff_id = request.data.get("staffId")

        if new_status not in ["Approved", "Pending", "Rejected"]:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == "Approved":
            if not staff_id:
                return Response({"error": "staffId is required when approving."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                staff_signature = Signature.objects.get(staff__id=staff_id)
            except Signature.DoesNotExist:
                return Response({"error": "Staff signature not found."}, status=status.HTTP_404_NOT_FOUND)

            # Check if signature has changed
            if clearance_signature.signature != staff_signature:
                clearance_signature.signature = staff_signature

        clearance_signature.status = new_status
        clearance_signature.save()

        return Response({
            "message": "ClearanceSignature updated successfully.",
            "status": clearance_signature.status,
            "signature_id": clearance_signature.signature.id if clearance_signature.signature else None
        }, status=status.HTTP_200_OK)