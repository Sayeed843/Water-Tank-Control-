from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Motor, AboutMe, DailyStatus, BdWaterBoard, Sensor
from django.shortcuts import get_list_or_404, get_object_or_404


def index(request):
    motors = DailyStatus.objects.all()
    context = {'motors': motors}
    return render(request, 'index.html', context)


def motor_status(request):
    user = BdWaterBoard.objects.all()
    context = {'user': user}
    return render(request, 'motor_status.html', context)


def motor_details(request, user_id):
    try:
        motor = DailyStatus.objects.filter(mac_id_id=user_id)
    except DailyStatus.DoesNotExist:
        motor = None

    latest_status = DailyStatus.objects.filter(mac_id_id=user_id).order_by('-id')[0]
    # print("LOL")
    try:
        board_status = Motor.objects.get(mac_fk_id=user_id)
    except Motor.DoesNotExist:
        board_status = None

    try:
        user = BdWaterBoard.objects.get(pk=user_id)
    except BdWaterBoard.DoesNotExist:
        user = None
    if board_status.waterSupply:
        print(board_status.waterSupply)
        latest_status = latest_status
    else:
        latest_status = False
    context = {'motor': motor, 'latest_status': latest_status,
               'control_switch': board_status.waterSupply,
               'board_status': board_status,
               'user': user}
    return render(request, 'motor_details.html', context)


def decision(request, user_id):
    if request.method == "POST":
        motor = request.POST['motor']
    ch_motor_status = Motor.objects.get(pk=user_id)
    if motor != 'No':
        motor = 1
        print("Result: " + str(motor))
    else:
        motor = 0
        print("Result: " + str(motor))
    ch_motor_status.waterSupply = motor
    ch_motor_status.save()
    return HttpResponse('decision')


def about_me(request):
    details = AboutMe.objects.all()
    context = {"details": details}
    return render(request, 'AboutMe.html', context)
