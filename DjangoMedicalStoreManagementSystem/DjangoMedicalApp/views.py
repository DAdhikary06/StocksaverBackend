from datetime import datetime, timedelta
from django.db.models import Sum, F
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from DjangoMedicalApp.models import Bill, BillDetails, Company, CompanyAccount, CustomerRequest, Employee, EmployeeBank, EmployeeSalary, MedicalDetails, Medicine
from DjangoMedicalApp.serializers import BillDetailsSerializer, BillSerializer, CompanyAccountSerializer, CompanySerliazer, CustomerRequestSerializer, CustomerSerializer, EmployeeBankSerializer, EmployeeSalarySerializer, EmployeeSerializer, MedicalDetailsSerializer, MedicalDetailsSerializerSimple, MedicineSerliazer
from DjangoMedicalApp.models import CompanyBank
from DjangoMedicalApp.serializers import CompanyBankSerializer

# Create your views here.

# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all()
#     serializer_class = CompanySerliazer

class CompanyViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self,request):
        company=Company.objects.all()
        serializer=CompanySerliazer(company,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company List Data","data":serializer.data}
        return Response(response_dict)
    
    def create(self,request):
        try:
            serializer=CompanySerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Data"}
        return Response(dict_response)
    
    def retrieve(self, request, pk=None):
        queryset = Company.objects.all()
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerliazer(company, context={"request": request})

        serializer_data = serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        company_bank_details = CompanyBank.objects.filter(company_id=serializer_data["id"])
        companybank_details_serializers = CompanyBankSerializer(company_bank_details, many=True)
        serializer_data["company_bank"] = companybank_details_serializers.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})
    
    def update(self,request,pk=None):
        try:
            queryset=Company.objects.all()
            company=get_object_or_404(queryset,pk=pk)
            serializer=CompanySerliazer(company,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Company Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Company Data"}
        return Response(dict_response)
    
    
class CompanyBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def create(self,request):
        try:
            serializer=CompanyBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Bank Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Bank Data"}
        return Response(dict_response)

    def list(self,request):
        companybank=CompanyBank.objects.all()
        serializer=CompanyBankSerializer(companybank,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=CompanyBank.objects.all()
        companybank=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companybank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})


class CompanyNameViewSet(generics.ListAPIView):
    serializer_class = CompanySerliazer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Company.objects.filter(name=name)
    

class MedicineByNameViewSet(generics.ListAPIView):
    serializer_class = MedicineSerliazer
    def get_queryset(self):
        name=self.kwargs["name"]
        return Medicine.objects.filter(name__contains=name)
    
    
class CompanyOnlyViewSet(generics.ListAPIView):
    serializer_class = CompanySerliazer
    def get_queryset(self):
        return Company.objects.all()
    
    
class MedicineViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=MedicineSerliazer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

            medicine_id=serializer.data['id']
            #Access The Serializer Id Which JUSt SAVE in OUR DATABASE TABLE
            #print(medicine_id)

            #Adding and Saving Id into Medicine Details Table
            medicine_details_list=[]
            for medicine_detail in request.data["medicine_details"]:
                print(medicine_detail)
                #Adding medicine id which will work for medicine details serializer
                medicine_detail["medicine_id"]=medicine_id
                medicine_details_list.append(medicine_detail)
                print(medicine_detail)

            serializer2=MedicalDetailsSerializer(data=medicine_details_list,many=True,context={"request":request})
            serializer2.is_valid()
            serializer2.save()

            dict_response={"error":False,"message":"Medicine Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Medicine Data"}
        return Response(dict_response)

    def list(self,request):
        medicine=Medicine.objects.all()
        serializer=MedicineSerliazer(medicine,many=True,context={"request":request})

        medicine_data=serializer.data
        newmedicinelist=[]

        #Adding Extra Key for Medicine Details in Medicine
        for medicine in medicine_data:
            #Accessing All the Medicine Details of Current Medicine ID
            medicine_details=MedicalDetails.objects.filter(medicine_id=medicine["id"])
            medicine_details_serializers=MedicalDetailsSerializerSimple(medicine_details,many=True)
            medicine["medicine_details"]=medicine_details_serializers.data
            newmedicinelist.append(medicine)

        response_dict={"error":False,"message":"All Medicine List Data","data":newmedicinelist}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerliazer(medicine,context={"request":request})

        serializer_data=serializer.data
        # Accessing All the Medicine Details of Current Medicine ID
        medicine_details = MedicalDetails.objects.filter(medicine_id=serializer_data["id"])
        medicine_details_serializers = MedicalDetailsSerializerSimple(medicine_details, many=True)
        serializer_data["medicine_details"] = medicine_details_serializers.data

        return Response({"error":False,"message":"Single Data Fetch","data":serializer_data})

    def update(self,request,pk=None):
        queryset=Medicine.objects.all()
        medicine=get_object_or_404(queryset,pk=pk)
        serializer=MedicineSerliazer(medicine,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        #print(request.data["medicine_details"])
        for salt_detail in request.data["medicine_details"]:
            if salt_detail["id"]==0:
                #For Insert New Salt Details
                del salt_detail["id"]
                salt_detail["medicine_id"]=serializer.data["id"]
                serializer2 = MedicalDetailsSerializer(data=salt_detail,context={"request": request})
                serializer2.is_valid()
                serializer2.save()
            else:
                #For Update Salt Details
                queryset2=MedicalDetails.objects.all()
                medicine_salt=get_object_or_404(queryset2,pk=salt_detail["id"])
                del salt_detail["id"]
                serializer3=MedicalDetailsSerializer(medicine_salt,data=salt_detail,context={"request":request})
                serializer3.is_valid()
                serializer3.save()
                print("UPDATE")

        return Response({"error":False,"message":"Data Has Been Updated"})


#Company Account Viewset
class CompanyAccountViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=CompanyAccountSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Company Account Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Company Account Data"}
        return Response(dict_response)

    def list(self,request):
        companyaccount=CompanyAccount.objects.all()
        serializer=CompanyAccountSerializer(companyaccount,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Company Account List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=CompanyAccount.objects.all()
        companyaccount=get_object_or_404(queryset,pk=pk)
        serializer=CompanyAccountSerializer(companyaccount,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=CompanyAccount.objects.all()
        companyaccount=get_object_or_404(queryset,pk=pk)
        serializer=CompanyBankSerializer(companyaccount,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})


#Employee Viewset
class EmployeeViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Data"}
        return Response(dict_response)

    def list(self,request):
        employee=Employee.objects.all()
        serializer=EmployeeSerializer(employee,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=Employee.objects.all()
        employee=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSerializer(employee,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})
    
    
#Employee Bank Viewset
class EmployeeBankViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeBankSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Bank Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Bank"}
        return Response(dict_response)

    def list(self,request):
        employeebank=EmployeeBank.objects.all()
        serializer=EmployeeBankSerializer(employeebank,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Bank List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeBank.objects.all()
        employeebank=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeBankSerializer(employeebank,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})
    
   
#Employee Salary Viewset
class EmployeeSalaryViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            serializer=EmployeeSalarySerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Employee Salary Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Employee Salary"}
        return Response(dict_response)

    def list(self,request):
        employeesalary=EmployeeSalary.objects.all()
        serializer=EmployeeSalarySerializer(employeesalary,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Employee Salary List Data","data":serializer.data}
        return Response(response_dict)

    def retrieve(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,context={"request":request})
        return Response({"error":False,"message":"Single Data Fetch","data":serializer.data})

    def update(self,request,pk=None):
        queryset=EmployeeSalary.objects.all()
        employeesalary=get_object_or_404(queryset,pk=pk)
        serializer=EmployeeSalarySerializer(employeesalary,data=request.data,context={"request":request})
        serializer.is_valid()
        serializer.save()
        return Response({"error":False,"message":"Data Has Been Updated"})
    
 
class EmployeeBankByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeBankSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeBank.objects.filter(employee_id=employee_id)      
   
class EmployeeSalaryByEIDViewSet(generics.ListAPIView):
    serializer_class = EmployeeSalarySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        employee_id=self.kwargs["employee_id"]
        return EmployeeSalary.objects.filter(employee_id=employee_id)
    

class GenerateBillViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        #try:
            # First Save Customer Data
        serializer = CustomerSerializer(data=request.data, context={"request": request})
        serializer.is_valid()
        serializer.save()

        customer_id = serializer.data['id']

        # Save Bill Data
        billdata={}
        billdata["customer_id"]=customer_id

        serializer2 = BillSerializer(data=billdata, context={"request": request})
        serializer2.is_valid()
        serializer2.save()
        bill_id = serializer2.data['id']

        # Adding and Saving Id into Medicine Details Table
        medicine_details_list = []
        for medicine_detail in request.data["medicine_details"]:
            print(medicine_detail)
            medicine_detail1={}
            medicine_detail1["medicine_id"] = medicine_detail["id"]
            medicine_detail1["bill_id"] = bill_id
            medicine_detail1["qty"] = medicine_detail["qty"]

            medicine_deduct=Medicine.objects.get(id=medicine_detail["id"])
            medicine_deduct.in_stock_total=int(medicine_deduct.in_stock_total)-int(medicine_detail['qty'])
            medicine_deduct.save()

            medicine_details_list.append(medicine_detail1)
            #print(medicine_detail)

        serializer3 = BillDetailsSerializer(data=medicine_details_list, many=True,
                                               context={"request": request})
        serializer3.is_valid()
        serializer3.save()

        dict_response = {"error": False, "message": "Bill Generate Successfully"}
        #except:
            #dict_response = {"error": True, "message": "Error During Generating BIll"}
        return Response(dict_response)


class CustomerRequestViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        customer_request=CustomerRequest.objects.all()
        serializer=CustomerRequestSerializer(customer_request,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Customer Request Data","data":serializer.data}
        return Response(response_dict)

    def create(self,request):
        try:
            serializer=CustomerRequestSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Customer Request Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Customer Request Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = CustomerRequest.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = CustomerRequestSerializer(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self,request,pk=None):
        try:
            queryset=CustomerRequest.objects.all()
            customer_request=get_object_or_404(queryset,pk=pk)
            serializer=CustomerRequestSerializer(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Customer Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Data"}

        return Response(dict_response)
    
    
class CustomerRequestViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self,request):
        customer_request=CustomerRequest.objects.all()
        serializer=CustomerRequestSerializer(customer_request,many=True,context={"request":request})
        response_dict={"error":False,"message":"All Customer Request Data","data":serializer.data}
        return Response(response_dict)

    def create(self,request):
        try:
            serializer=CustomerRequestSerializer(data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Customer Request Data Save Successfully"}
        except:
            dict_response={"error":True,"message":"Error During Saving Customer Request Data"}
        return Response(dict_response)

    def retrieve(self, request, pk=None):
        queryset = CustomerRequest.objects.all()
        customer_request = get_object_or_404(queryset, pk=pk)
        serializer = CustomerRequestSerializer(customer_request, context={"request": request})

        serializer_data = serializer.data

        return Response({"error": False, "message": "Single Data Fetch", "data": serializer_data})

    def update(self,request,pk=None):
        try:
            queryset=CustomerRequest.objects.all()
            customer_request=get_object_or_404(queryset,pk=pk)
            serializer=CustomerRequestSerializer(customer_request,data=request.data,context={"request":request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            dict_response={"error":False,"message":"Successfully Updated Customer Data"}
        except:
            dict_response={"error":True,"message":"Error During Updating Customer Data"}

        return Response(dict_response)
    
    
class HomeApiViewset(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customer_request = CustomerRequest.objects.all()
        customer_request_serializer = CustomerRequestSerializer(customer_request, many=True, context={"request": request})

        bill_count = Bill.objects.all()
        bill_count_serializer = BillSerializer(bill_count, many=True, context={"request": request})

        medicine_count = Medicine.objects.all()
        medicine_count_serializer = MedicineSerliazer(medicine_count, many=True, context={"request": request})

        company_count = Company.objects.all()
        company_count_serializer = CompanySerliazer(company_count, many=True, context={"request": request})

        employee_count = Employee.objects.all()
        employee_count_serializer = EmployeeSerializer(employee_count, many=True, context={"request": request})

        # Calculate total buy and sell amounts for all bill details
        bill_details = BillDetails.objects.all()
        profit_amt = 0
        sell_amt = 0
        buy_amt = 0

        for bill in bill_details:
            qty = int(bill.qty)
            buy_price = float(bill.medicine_id.buy_price) if bill.medicine_id.buy_price else 0
            sell_price = float(bill.medicine_id.sell_price) if bill.medicine_id.sell_price else 0

            buy_amt += buy_price * qty
            sell_amt += sell_price * qty

        profit_amt = sell_amt - buy_amt

        customer_request_pending = CustomerRequest.objects.filter(status=False)
        customer_request_pending_serializer = CustomerRequestSerializer(customer_request_pending, many=True, context={"request": request})

        customer_request_completed = CustomerRequest.objects.filter(status=True)
        customer_request_completed_serializer = CustomerRequestSerializer(customer_request_completed, many=True, context={"request": request})

        # Get today's date
        current_date = datetime.today().date()

        # Query for bill details added today
        bill_details_today = BillDetails.objects.filter(added_on__date=current_date)

        # Initialize today's profit, sell, and buy amounts
        profit_amt_today = 0
        sell_amt_today = 0
        buy_amt_today = 0

        # Calculate buy and sell amounts for today's bills
        for bill in bill_details_today:
            qty = int(bill.qty)
            buy_price = float(bill.medicine_id.buy_price) if bill.medicine_id.buy_price else 0
            sell_price = float(bill.medicine_id.sell_price) if bill.medicine_id.sell_price else 0

            buy_amt_today += buy_price * qty
            sell_amt_today += sell_price * qty

        # Calculate profit amount for today
        profit_amt_today = sell_amt_today - buy_amt_today

        # Get medicines expiring in the next 7 days
        current_date_7days = current_date + timedelta(days=7)
        medicine_expire = Medicine.objects.filter(expire_date__range=[current_date, current_date_7days])
        medicine_expire_serializer = MedicineSerliazer(medicine_expire, many=True, context={"request": request})

        # Get distinct dates from BillDetails for charts
        bill_dates = BillDetails.objects.values("added_on__date").distinct()

        profit_chart_list = []
        sell_chart_list = []
        buy_chart_list = []

        # Loop through each unique date
        for billdate in bill_dates:
            access_date = billdate["added_on__date"]

            # Calculate total buy and sell amounts for each date
            bill_data = BillDetails.objects.filter(added_on__date=access_date)

            # Initialize amounts
            buy_amt_inner = 0
            sell_amt_inner = 0

            # Calculate buy and sell amounts for each bill on that date
            for billsingle in bill_data:
                qty = int(billsingle.qty)
                buy_price = float(billsingle.medicine_id.buy_price) if billsingle.medicine_id.buy_price else 0
                sell_price = float(billsingle.medicine_id.sell_price) if billsingle.medicine_id.sell_price else 0

                buy_amt_inner += buy_price * qty
                sell_amt_inner += sell_price * qty

            # Calculate profit amount for that date
            profit_amt_inner = sell_amt_inner - buy_amt_inner

            # Append results to the respective lists
            profit_chart_list.append({"date": access_date, "amt": profit_amt_inner})
            sell_chart_list.append({"date": access_date, "amt": sell_amt_inner})
            buy_chart_list.append({"date": access_date, "amt": buy_amt_inner})

        # Prepare the response dictionary
        dict_response = {
            "error": False,
            "message": "Home Page Data",
            "customer_request": len(customer_request_serializer.data),
            "bill_count": len(bill_count_serializer.data),
            "medicine_count": len(medicine_count_serializer.data),
            "company_count": len(company_count_serializer.data),
            "employee_count": len(employee_count_serializer.data),
            "sell_total": sell_amt,
            "buy_total": buy_amt,
            "profit_total": profit_amt,
            "request_pending": len(customer_request_pending_serializer.data),
            "request_completed": len(customer_request_completed_serializer.data),
            "profit_amt_today": profit_amt_today,
            "sell_amt_today": sell_amt_today,
            "medicine_expire_serializer_data": len(medicine_expire_serializer.data),
            "sell_chart": sell_chart_list,
            "buy_chart": buy_chart_list,
            "profit_chart": profit_chart_list,
        }

        return Response(dict_response)
    
       
company_list=CompanyViewSet.as_view({"get":"list"})
company_creat=CompanyViewSet.as_view({"post":"create"})
company_update=CompanyViewSet.as_view({"put":"update"})

# ***********************************
# For User Registration 
# ***********************************
# from rest_framework import generics, status
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
# from rest_framework.response import Response
from DjangoMedicalApp.utils import send_normal_email, send_password_reset_confirmation_email
from DjangoMedicalApp.serializers import SuperuserSerializer, PasswordResetRequestSerializer, \
    PasswordResetConfirmSerializer

class SuperuserCreateView(generics.CreateAPIView):
    serializer_class = SuperuserSerializer

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uidb64']))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, serializer.validated_data['token']):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                # email_body = f"Hi {user.username}, your password has been reset successfully."
                context = {
                    'username': user.username,
                }
                data = {
                'to_email': user.email,
                'email_subject': 'Password reset successful',
                'context': context
                }
                # send_normal_email(data)
                send_password_reset_confirmation_email(data)
                return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            pass
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    

# ***********************************
# For Custom Token Obtain Pair View
# ***********************************

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# ***********************************
# For Stripe
# ***********************************

import stripe
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from DjangoMedicalApp.models import CompanyAccount, Payment

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@api_view(['POST'])
def create_payment_intent(request):
    try:
        amount = int(float(request.data.get('amount')))
        company_id = int(request.data.get('company_id'))
        
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            metadata={'company_id': company_id}
        )
        
        return Response({
            'clientSecret': intent.client_secret,
            'payment_intent_id': intent.id
        })
    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['POST'])
def handle_payment_success(request):
    try:
        payment_intent_id = request.data.get('paymentIntentId')
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if payment_intent.status == 'succeeded':
            company_id = payment_intent.metadata.get('company_id')
            amount = payment_intent.amount / 100  # Convert from cents to rupees
            
            # Create CompanyAccount entry
            company_account = CompanyAccount.objects.create(
                company_id_id=company_id,
                transaction_type='Credit',
                transaction_amt=str(amount),
                transaction_date=datetime.now().date(),
                payment_mode='Card'
            )
            
            # Create Payment entry
            Payment.objects.create(
                payment_intent_id=payment_intent_id,
                company_account=company_account,
                amount=amount,
                status='success'
            )
            
            return Response({'status': 'success'})
    except Exception as e:
        return Response({'error': str(e)}, status=400)