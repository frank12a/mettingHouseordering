from django.shortcuts import render, HttpResponse,redirect
from django.http import JsonResponse
from django.forms import Form
from django.forms import fields
from django.forms import widgets
import time
import json


# Create your views here.
from . import models


def index(request):
    time_list = models.Bookings.time_pharse
    return render(request, "index.html", {"time_list": time_list})

def show(request):
    if request.method=="GET":
        time.sleep(1)
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
        try:
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
                tr_list = [{'text': item.name, "attrs":{'tr_id': item.id}}]
                for time_item in time_list:

                    if item.id in booking_dict and time_item[0] in booking_dict[item.id]:
                        td={'text':'','attrs':{}}
                        td["text"]=booking_dict[item.id][time_item[0]].get("username")
                        td['attrs']["chosen"]=True
                        if booking_dict[item.id][time_item[0]]["user_id"] == request.session.get("user_id"):
                            td = { 'text':booking_dict[item.id][time_item[0]].get("username"),"attrs": {'tr_id': item.id, "time_id": time_item[0], 'class': 'chosen'}}

                        else:
                            td = {'text':booking_dict[item.id][time_item[0]].get("username"),"attrs": {'tr_id': item.id, "time_id": time_item[0], 'class': 'chosen'}}
                            td['attrs']['disable'] = 'true'
                    else:
                        td = {'text': '', "attrs": {'tr_id': item.id, "time_id": time_item[0],}}
                    tr_list.append(td)
                data.append(tr_list)
            response["data"] = data
            print(data,"返回数据结构")
            # print(data,"返回的数据")
        except Exception as e:
            response["status"] = False
            response["errors"] = e
        return JsonResponse(response)
    else:
        response = {"status": True, "errors": None, "data": None}
        # try:
        data=json.loads(request.body.decode("utf-8"))["data"]
        print(data,"dat")
        response_date=json.loads(request.body.decode("utf-8")).get("date")

        print(response_date,"传回的时间")
        # print(json.loads(request.body.decode("utf-8")),'前端传的数据')
        #判断删除
        for room_id,time_list in data['del'].items():
            if room_id not in data["add"]:
                continue
            else:
               for i in list(time_list):
                   if  i in data['add'][room_id]:
                        data["del"][room_id][i].remove()
                        data["add"][room_id][i].remove()
        #增加数据
        book_obj_list=[]
        for room_id,time_list in data["add"].items():
            print(room_id,time_list)
            for time_id in time_list:
                print(time_id,"********")
                bookingList_obj=models.Bookings.objects.create(user_id=request.session.get("user_id"),room_id=room_id,time_id=time_id,date=response_date)
                print(bookingList_obj)
        #         book_obj_list.append(bookingList_obj)
        # print(book_obj_list)
        # models.Bookings.objects.bulk_create(book_obj_list)
        #删除数据
        from django.db.models import Q
        removeing_list=Q()
        for room_id,time_list in data["del"].items():
            for time_id in time_list:
                temp=Q()
                temp.connector="AND"
                temp.children.append(("user_id",request.session.get("user_id")))
                temp.children.append(("room_id",room_id))
                temp.children.append(("time_id",time_id))
                temp.children.append(("date",response_date))
                removeing_list.add(temp,'OR')
        if removeing_list:
            models.Bookings.objects.filter(removeing_list).delete()

        # except Exception as e:
        # response["status"] = False
        # response["errors"] = str(e)
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






