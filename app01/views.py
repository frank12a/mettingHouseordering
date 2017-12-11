from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from django.forms import Form
from django.forms import fields
from django.forms import widgets


# Create your views here.
from . import models


def index(request):
    time_list = models.Bookings.time_pharse
    return render(request, "index.html", {"time_list": time_list})

def show(request):
    print(type(request.GET.get("date")))
    date=request.GET.get("date")
    time_list = models.Bookings.time_pharse
    # fetch_date = datetime.datetime.strptime(fetch_date, '%Y-%m-%d').date()#把时间从字符串变成时间对象格式。
    import datetime
    now_date = datetime.datetime.now().date()
    print(now_date,"***********")
    booking_list = models.Bookings.objects.filter(date=request.GET.get("date"))
    '''
    {
        1:{
             5:{'user_id':111,'user_username':Frank}
         }
    }
    '''
    booking_dict={}
    for item in booking_list:
        if item.room_id not in booking_dict:
            booking_dict[item.room_id] = {item.time_id: {'username': item.user.user, 'chosen': 'active','user_id':item.user.id}}
        else:
            booking_dict[item.room_id][item.time_id] = {'username': item.user.user, 'chosen': 'active','user_id':item.user.id}
    print(booking_dict,"整理数据结构")

    response = {"status": True, "errors": None, "data": None}
    # try:
    '''
        data=[
        [{'text':'天上人间',attrs({"chosen":active,'username':xxx})},{'text':},{},{}],
        [{},{},{},{}],
        [{},{},{},{}],
        [{},{},{},{}],

        ]
     '''
    data = []
    room_list = models.Room.objects.all()
    for item in room_list:
        tr_list = [{'text': item.name, "tr_id": item.id}]
        for time_item in time_list:
            td = {'text': None, 'tr_id': item.id, "time_id": time_item[0],'chosen': False}
            if item.id in booking_dict and time_item[0] in booking_dict[item.id]:
                td["text"]=booking_dict[item.id][time_item[0]].get("username")
                td["chosen"]='active'
                if booking_dict[item.id][time_item[0]]["user_id"] == request.session.get("user_id"):
                    td['disable']=True
            # tr_list.append(td)

            # for kk in booking_list:
            #     if (item.id == kk.room_id) and (time_item[0] == kk.time_id):
            #         print(kk.user.user)
            #         print(time_item[0])
            #         print(item.id)
            #         print("执行啦")
            #         td = {'username': kk.user.user ,'text': None, 'tr_id': item.id, "time_id": time_item[0],'chosen': 'active'}
            tr_list.append(td)
        data.append(tr_list)
    response["data"] = data
        # print(data,"返回的数据")
    # except Exception as e:
    #     response["status"] = False
    #     response["errors"] = e
    return JsonResponse(response)
class LoginForm(Form):
    user=fields.CharField(
        required=True,
        error_messages={"required":"名字不能为空"},
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'用户名'})
    )
    pwd=fields.CharField(
        required=True,
        error_messages={"required": "名字不能为空"},
        widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'密码',})
    )

def login(request):
    if request.method=="GET":
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    if request.method=="POST":
       form=LoginForm(data=request.POST)
       if form.is_valid():

           user_obj=models.Userinfo.objects.filter(**form.cleaned_data).first()
           request.session["user_id"]=user_obj.id
           return  redirect('/index/')
       else:
           return render(request,"login.html",{"form":form})






