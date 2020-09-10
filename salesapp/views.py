from django.shortcuts import render, redirect
from .models import Transaction
from django.contrib.auth.models import User, auth
from django.contrib import messages


##
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Create your views here.

########spreadsheet
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("static/sales-d29e5d122639.json", scope)

client = gspread.authorize(creds)

sheet = client.open("salesrecord").sheet1 
####
def home(request):
    return render(request, 'home.html')

def data(request):
    if request.method == 'POST':
        x = request.POST
        brought_from = x['brought']
        sold_to = x['sold']
        quantity = float(x['quantity'])
        c_rate = float(x['crate'])
        s_rate = float(x['srate'])
        cp = c_rate * quantity
        sp = s_rate * quantity
        profit = sp - cp

        print('Working')
        
        t = Transaction.objects.create(brought_from=brought_from,sold_to=sold_to,quantity=quantity,                               c_rate=c_rate,s_rate=s_rate,cp=cp,sp=sp,profit=profit)
    
        t.save()
        
        ###googe sheets
        
        row = [str(t.id),t.brought_from, t.sold_to, t.quantity, t.c_rate, t.s_rate, t.cp,t.sp,t.profit]
        sheet.insert_row(row,2)
        
        print(sheet.get_all_values())
        
        
        ###
    
    return redirect('/')

def show(request):
    
    if request.user.is_authenticated:    
        t=[]
        t = Transaction.objects.all()
        context = {
            'items':t
        }
        return render(request, 'show.html', context)
    return redirect('/')

def update(request, num):  
    if request.user.is_authenticated:
        if request.method == 'POST':
            t = Transaction.objects.filter(id=num)[0]
            x = request.POST
       

            ##change in the spreadsheet
            row=0
            datas = sheet.get_all_values()
            for data in datas:
                if data[0] == str(num):
                    row = datas.index(data)+1
                    sheet.delete_row(row)

                    break
             ##       

            t.brought_from = x['brought']
            t.sold_to = x['sold']
            t.quantity = float(x['quantity'])
            t.c_rate = float(x['crate'])
            t.s_rate = float(x['srate'])
            t.cp = t.c_rate * t.quantity
            t.sp = t.s_rate * t.quantity
            t.profit = t.sp - t.cp
            t.save()
            ##render data in sheets 
            new_row = [str(t.id),t.brought_from, t.sold_to, t.quantity, t.c_rate, t.s_rate, t.cp,t.sp,t.profit]
            sheet.insert_row(new_row,row)
            ##
            return redirect('/show')
        t = Transaction.objects.filter(id=num)[0]
        context = {
            'item': t
        }
        return render(request, 'update.html', context)
    else:
        return redirect('/')
    
def delete(request, code):
        t = Transaction.objects.filter(id=code)[0]
        t.delete()
        ##speadsheet delete
        datas = sheet.get_all_values()
        for data in datas:
            if data[0] == str(code):
                x = datas.index(data)
                sheet.delete_row(x+1)
                break
            
        ##    
        return redirect('/show')
        
def login(request):
    if request.method == 'POST':
        username = request.POST['username']     
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials! ')
            return redirect('/login')
            
    else:
        
        return render(request, 'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/')
    