import json
import base64
import razorpay
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from Interior_design.agent import Agent, Task, InputType, OutputType
from Interior_design.openai_model import OpenAIModel
from Interior_design.arch import SequentialFlow
from .database import SQLiteDB
from django.contrib.auth.models import User

load_dotenv()
db = SQLiteDB()

expertise = "Interior Designer"
task = Task("Image Generation")
input_type = InputType("Text")
output_type = OutputType("Image")
agent = Agent(expertise, task, input_type, output_type)

def checkQuota(user):
    user_details = db.get_user_data(user)
    quota = user_details[1]
    count = user_details[2]
    if quota != 'FREE':
        return True, count, quota
    else:
        if 0 < count <= 10:
            return True, count, quota
        else:
            return False, count, quota

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "username": username})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        if password1 != password2:
            return JsonResponse({"error": "Passwords do not match"}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return JsonResponse({"message": "Registration successful", "username": username})

    return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def genAIPrompt2(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            api_key = data.get("api_key")
            model = OpenAIModel(api_key=api_key, model="dall-e-2")
            sequential_flow = SequentialFlow(agent, model)
            
            selected_style = data.get("selected_style")
            selected_room_color = data.get("selected_room_color")
            selected_room_type = data.get("selected_room_type")
            # number_of_room_designs = data.get("number_of_room_designs")
            additional_instructions = data.get("additional_instructions")

            if not (selected_style and selected_room_color and selected_room_type ):
                return JsonResponse({"error": "Missing required fields"}, status=400)
            
            prompt = f"Generate a Realistic looking Interior design with the following instructions: style: {selected_style}, Room Color: {selected_room_color}, Room type: {selected_room_type}, Instructions: {additional_instructions}"
            image_url = sequential_flow.execute(prompt)
            return JsonResponse({"image": image_url, "status": "Success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def generateImage(request):
    if request.method == "POST":
        try:
            api_key = request.POST.get("api_key")
            model = OpenAIModel(api_key=api_key, model="dall-e-2")
            sequential_flow = SequentialFlow(agent, model)
            
            selected_style = request.FILES.get("selected_style")
            selected_room_color = request.FILES.get("selected_room_color")
            selected_room_type = request.FILES.get("selected_room_type")
            
            if not (selected_style and selected_room_color and selected_room_type):
                return JsonResponse({"error": "Missing required files"}, status=400)
            
            s_style = base64.b64encode(selected_style.read()).decode('utf-8')
            s_room_c = base64.b64encode(selected_room_color.read()).decode('utf-8')
            s_room_t = base64.b64encode(selected_room_type.read()).decode('utf-8')
            
            prompt = f"Generate a final Image based on the 3 input images provided: Image_1={s_style}, Image_2={s_room_c}, Image_3={s_room_t}"
            image_url = sequential_flow.execute(prompt)
            return JsonResponse({"image": image_url, "status": "Success"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# Initialize Razorpay client
client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_KEY_SECRET"))

@csrf_exempt
def donate(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        amount = data.get('amount')
        # Create a new payment order
        order = client.order.create({
            'amount': amount * 100,  # amount in paise
            'currency': 'INR',
            'payment_capture': 1
        })
        return JsonResponse({"order_id": order['id'], "amount": amount, "status": "Order created successfully"})

