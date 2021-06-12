from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb
from datetime import date
import datetime
from django.core.files.storage import FileSystemStorage
db=MySQLdb.connect("localhost","root","","city360_approve")
c=db.cursor()

def login(request):
    msg=""
    request.session['uname']=""
    if(request.POST):      
        uname=request.POST.get("uname")
        pw=request.POST.get("pwd")
        
        z="select utype,status from login where uname='"+uname+"' and pwd='"+pw+"' "
        c.execute(z)
        data=c.fetchone()
        print(data)
        request.session['uname']=uname
        if data:
            if(data[0]=="user" and data[1]=="approved"):
                return HttpResponseRedirect("/user/")
            elif(data[0]=="worker" and data[1]=="approved"):
                return HttpResponseRedirect("/worker/")
            elif(data[0]=="admin"):
                return HttpResponseRedirect("/adminhome/")
        else:
            msg="INVALID USER NAME OR PASSWORD"       
        #return HttpResponseRedirect("/adminhome/")
       
            
    return render (request,"login.html",{"msg":msg})    


def addcategory(request):
    msg=""
    if request.session['uname']:
        if(request.POST):    
            
            catname=request.POST.get("catgry")
            wages=str(request.POST.get("wages"))
            c.execute("select count('"+catname+"') from category where catname='"+catname+"'")
            data=c.fetchone()
            if data[0]==0:

                c.execute("insert into category(catname,wage)values('"+catname+"','"+wages+"')")
                db.commit()
                msg="CATEGORY SUCCESSFULLY ADDED"
            else:
                msg="ALREADY EXIST!!"
    else:
        return HttpResponseRedirect("/login")       
    return render (request,"addcategory.html",{"msg":msg})
    
def userfeedback(request):
    if request.session['uname']:
        uname=request.session['uname']
        if(request.POST):
            sender=request.session['uname']
            feedback=request.POST.get("feedback")
            date=datetime.date.today()
           # time=datetime.datetime.today()
           # z=str(time)
            c.execute("insert into feedback(feedback,date,username)values('"+feedback+"','"+str(date)+"' ,'" +sender+ "')")
            db.commit()
    else:
        return HttpResponseRedirect("/login")    
    return render (request,"userfeedback.html")

def workerfeedback(request):
    if request.session['uname']:
        uname=request.session['uname']
        if(request.POST):
            sender=request.session['uname']
            feedback=request.POST.get("feedback")
            date=datetime.date.today()
           # time=datetime.datetime.today()
           # z=str(time)
            c.execute("insert into feedback(feedback,date,username)values('"+feedback+"','"+str(date)+"' ,'" +sender+ "')")
            db.commit()
    else:
        return HttpResponseRedirect("/login")   
    return render (request,"workerfeedback.html")

    
def suggestcat(request):
    msg=""
    if request.session['uname']:
        if(request.POST):
            catgry=request.POST.get("catgry")
            c.execute("select count('"+catgry+"') from category where catname='"+catgry+"'")
            data=c.fetchone()
            if data[0]==0:

                c.execute("insert into category(catname)values('"+catgry+"')")
                db.commit()
                msg="CATEGORY SUCCESSFULLY ADDED"
            else:
                msg="ALREADY EXIST"
    else:
        return HttpResponseRedirect("/login")   
    return render (request,"suggestcat.html",{"msg":msg})
   

   
def workerreg(request):
    msg=""
    cc=""
    c.execute("select * from category")
    cc=c.fetchall()
    if(request.POST):
        workername=request.POST.get("wname")
        address=request.POST.get("address")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        phn=str(request.POST.get("phn"))
        email=request.POST.get("email")
        pwd=request.POST.get("pwd")
        cpwd=request.POST.get("comfirmpwd")
        experience=str(request.POST.get("experience"))
        category=request.POST.get("category")
        uname=request.POST.get("uname") 
        utype="worker"
        status="applied"
        if(pwd==cpwd):
            if(request.FILES['wimg']):
                myfile=request.FILES['wimg']
                fs=FileSystemStorage()
                filenamme=fs.save(myfile.name,myfile)
                fileurl=fs.url(filenamme)

            # utype="worker"
                c.execute("select count('"+uname+"') from workerregistration where workername='"+uname+"' ")
                n=c.fetchone()
                c.execute("select count('"+phn+"') from workerregistration where phn='"+phn+"' ")
                p=c.fetchone()
                c.execute("select count('"+email+"') from workerregistration where email='"+email+"' ")
                e=c.fetchone()
                if n[0]==0 :
                 if p[0]==0:
                    if e[0]==0:
                    #if p[0]==0:
                        #if e[0]==0:
                        c.execute("insert into  workerregistration(name,workername,address,workerphoto,dob,gender,phn,email,experience,category)values('"+uname+"','"+workername+"','"+address+"','"+ fileurl +"','"+str(dob)+"','"+gender+"','"+phn+"','"+email+"','"+experience+"','"+category+"')")
                        db.commit()
                        c.execute("insert into login(uname,pwd,utype,status) values('"+workername+"','"+pwd+"','"+utype+"','"+ status +"')")
                        request.session["tmp_uname"]=workername
                        db.commit()
                        
                        return HttpResponseRedirect("/members/")
                    else:
                        msg="Mail Already existed"
                 else:
                        msg="Phone no Already existed"
                    #else:
                            #msg="email id already exist"
                    #else:
                        #msg="phone number already exist"
                else:
                    msg="USER NAME ALREADY EXIST"
        else:
            msg="password and confirm password must match!!"    
       # return HttpResponseRedirect("/question/")

           
        #db.commit()
        
    return render (request,"workerreg.html",{"cc":cc,"msg":msg})
    
def payment(request):
    if request.session['uname']:
        ss=""
        amnt=request.session["amnt"]
        if(request.POST):
                      
            mode="netbanking"
            uname=request.POST.get("name")
            dt=datetime.date.today()        
            ss="insert into payment(amount,date,mode,uname,bid) values ('"+str(amnt)+"','"+str(dt)+"','"+mode+"','"+uname+"','"+ str(request.session["bkid"]) +"')"
            c.execute(ss)
            db.commit()
            return HttpResponseRedirect("/booking/")            
    else:
        return HttpResponseRedirect("/login")    
    return render (request,"payment.html",{"amnt":amnt})
    
def search(request):
    if request.session['uname']:
        data=""
        c.execute("select * from category")
        cat=c.fetchall()
        if(request.POST):
            z=request.POST["category"]
            c.execute("select * from workerregistration where category='"+z+"' ")
            data=c.fetchall()
    else:
        return HttpResponseRedirect("/login")      
    return render (request,"search.html",{"data":data,"cat":cat})

def userdetails(request):
    if request.session['uname']:
        c.execute("select * from userregistration")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"userdetails.html",{"data":data})

def viewbooking(request):
    if request.session['uname']:
          c.execute("select booking.* from booking join workerregistration on booking.wid=workerregistration.wid where booking.status='approve'")
          data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"viewbooking.html",{"data":data})

def paymentdetails(request):
    if request.session['uname']:
        c.execute("select * from payment")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login/") 
    return render (request,"paymentdetails.html",{"data":data})

def feedbackdetails(request):
    if request.session['uname']:
        c.execute("select * from feedback")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"feedbackdetails.html",{"data":data})
def notification(request):
    if request.session['uname']:
        c.execute("select * from feedback")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"notification.html",{"data":data})
def workernotification(request):
    if request.session['uname']:
        c.execute("select * from feedback")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"workernotification.html",{"data":data})

def workers(request): 
    if request.session['uname']:  
        c.execute("select * from workerregistration")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"workers.html",{"data":data})


def index(request):
    if request.session['uname']: 
        return render (request,"index.html")
    else:
        return HttpResponseRedirect("/login") 
    
    
    


def worker(request):   
    if request.session['uname']: 
        return render (request,"worker.html")
    else:
        return HttpResponseRedirect("/login") 
    


def user(request):   
    if request.session['uname']: 
        return render (request,"user.html")
    else:
        return HttpResponseRedirect("/login") 
    


def adminhome(request): 
    if request.session['uname']: 
         return render (request,"adminhome.html")
    else:
        return HttpResponseRedirect("/login")   
   
   



def bookingrequest(request):  
    if request.session['uname']: 
        c.execute("select wid from workerregistration where workername ='"+ request.session['uname'] +"'")
        dddd=c.fetchone()
        c.execute("select * from booking where wid='"+ str(dddd[0]) +"' and status='pending'")
        data=c.fetchall()
        bid=request.GET.get('id')
        st=request.GET.get('st')
        if bid:
                    c.execute("update booking set status='"+st+"' where bid='"+bid+"'")
                    db.commit()
                    return HttpResponseRedirect("/bookingrequest/")
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"bookingrequest.html",{"data":data})

def userprofile(request):
    if request.session['uname']:    
        uname=request.session['uname']
        c.execute(" select * from userregistration where uname='"+uname+"'")
        data=c.fetchall()
        if request.POST:
            return HttpResponseRedirect("/edit_userprofile/")
        
    else:
        return HttpResponseRedirect("/login")    
    return render (request,"userprofile.html",{"data":data})

def workerprofile(request):  
    if request.session['uname']: 
        uname=request.session['uname']
        c.execute(" select * from workerregistration where workername='"+uname+"'")
        data=c.fetchall()
        if request.POST:
            return HttpResponseRedirect("/edit_workerprofile/")
    
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"workerprofile.html",{"data":data})
 
   


def addnotification(request):  
    if request.session['uname']: 
        return render (request,"addnotification.html")
    else:
        return HttpResponseRedirect("/login") 
    


def commonhome(request):   
    if request.session['uname']: 
        return render (request,"commonhome.html")
    else:
        return HttpResponseRedirect("/login") 
    


def forgotpwd(request):    
    msg=""
    if(request.POST):
        z=request.POST["uname"]   
        no=request.POST["mob"]   
        c.execute("select count(uname) from userregistration where uname='"+z+"'and phn='"+no+"' ")
        data=c.fetchone()
        if(data[0]>0):
            request.session['funame']=z
            return HttpResponseRedirect("/question/")
        else:
         msg="Enter proper user id"
    return render(request,"forgotpwd.html",{"msg":msg})

def forgotpwd1(request):
    msg=""     
    if(request.POST):
        npass=request.POST.get("npass")
        cpass=request.POST.get("cpass")
        if(npass==cpass):
            c.execute("update login set pwd='"+cpass+"' where uname='" + request.session['funame'] + "'")
            db.commit()
        else:
            msg="Password doesnt match"
    return render(request,"forgotpwd1.html",{"msg":msg}) 

def question(request):
    if(request.POST):
        question=request.POST.get("question")
        c.execute("update userregistration set  answer='"+question+"' where uname='" + request.session['funame'] + "'")
        db.commit()
        return HttpResponseRedirect("/forgotpwd1/")
    return render (request,"question.html") 
    



def common_base1(request):  
    #if request.session['uname']: 
        return render (request,"common_base1.html")
    #else:
        #return HttpResponseRedirect("/login")  
   
    


def user_base1(request): 
    #if request.session['uname']: 
         return render (request,"user_base1.html")
    #else:
       # return HttpResponseRedirect("/login")  
   
   


def worker_base1(request): 
    if request.session['uname']:
        return render (request,"worker_base1.html")
    else:
        return HttpResponseRedirect("/login")  
   
    

def admin_base1(request): 
     
        return render (request,"admin_base1.html")
    
   
    


def logout(request): 
    if request.session['uname']: 
        
         return render (request,"login.html")
    else:
        return HttpResponseRedirect("/login")  
   

def booking(request):
    if request.session['uname']: 
        c.execute("select * from category")
        cat=c.fetchall()
        id=request.GET.get("pid")
        if(id):   
            c.execute("select catname from category where catid='"+id+"'")  
            cat=c.fetchone()   

            c.execute("select * from workerregistration where category='"+ cat[0] +"'")
            data=c.fetchall()
        
            return render (request,"require.html",{"data":data})
    else:
        return HttpResponseRedirect("/login")        
        
    return render (request,"booking.html",{"cat":cat})
def require(request):
    if request.session['uname']: 
        c.execute("select * from workerregistration ")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login") 
    return render(request,"require.html",{"data":data})      

def registration(request):
    message=""
    msg=""
    if(request.POST):
        uname=request.POST.get("uname")
        name=request.POST.get("name")
        address=request.POST.get("address")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        phn=request.POST.get("phn")
        email=request.POST.get("email")
        pwd=request.POST.get("pwd")
        cpwd=request.POST.get("comfirmpwd")        
        utype="user"
        status="applied"
        
        if(request.FILES.get('uphotos')):
            myfile=request.FILES['uphotos']
            fs=FileSystemStorage()          
            filenamme=fs.save(myfile.name,myfile)
            fileurl=fs.url(filenamme)
        else:
            fileurl="/static/media/userphoto.png"
        if(pwd==cpwd):
            c.execute("select count('"+uname+"') from userregistration where uname='"+uname+"' ")
            n=c.fetchone()
            c.execute("select count('"+phn+"') from userregistration where phn='"+phn+"' ")
            p=c.fetchone()
            c.execute("select count('"+email+"') from userregistration where email='"+email+"' ")
            e=c.fetchone()
            if n[0]==0:
                if p[0]==0:
                    if e[0]==0:
                   
                        c.execute("insert into userregistration(uname,name,address,dob,gender,phn,email,userphoto) values('"+uname+"','"+name+"','"+address+"','"+ dob+"','"+gender+"','"+str(phn)+"','"+email+"','"+fileurl+"')")
                        db.commit()
                        c.execute("insert into login(uname,pwd,utype,status) values('"+uname+"','"+pwd+"','"+utype+"','"+ status +"')")
                        db.commit()
                        msg="SUCCESSFULLY REGISTERED"
                    else:
                        msg="email id already exist"
                else:
                    msg="phone number already exist"
            else:
                msg="user name ALREADY EXIST"
        else:
            msg="password and confirm password must match!!"    
       # return HttpResponseRedirect("/question/")

    return render (request,"registration.html",{"msg":msg,"message":message})
    

def members(request):
    if request.session['uname']: 
        cc=""
        
        c.execute("select * from membership")
        cc=c.fetchall()
        if(request.POST):
            uname=request.POST.get("uname")
            plan=request.POST.get("plan")
            validity=request.POST.get("edate")
            
            idate=datetime.date.today        
            c.execute("select price,validity from membership where scheme='"+ plan +"'")
            mem=c.fetchall()  
            for m in mem:                       
                price=m[0]
                request.session["amount"]=price
    # val+monthof date.today
            
            c.execute("insert into members(uname,scheme,issued,expiry,price) values('"+uname+"','"+str(plan)+"','"+str(idate)+"','"+str(validity)+"','"+str(price)+"')")
            db.commit()
            
        
            return HttpResponseRedirect("/payment/")
    else:
        return HttpResponseRedirect("/login") 
    return render (request,"members.html",{"cc":cc,"temp_user":request.session["tmp_uname"]})

    
def adminmember(request):
    if request.session['uname']: 
        if(request.POST):
            scheme=request.POST.get("scheme")
            validity=request.POST.get("validity")
            price=request.POST.get("price")
        
            c.execute("insert into membership(scheme,validity,price) values('"+scheme+"','"+validity+"','"+price+"')")
            db.commit()
        
    else:
        return HttpResponseRedirect("/login")     
    return render (request,"adminmember.html")
    
def edit_userprofile(request): 
    if request.session['uname']:   
        uname=request.session['uname']
        c.execute(" select * from userregistration where uname='"+uname+"'")
        data=c.fetchall()
        for d  in data:
            uidd=d[0]
        request.session["uid"]=str(uidd)
        if('submit' in request.POST):
            Uname=request.POST.get("Uname")
            Address=request.POST.get("Address")
            Dob=request.POST.get("Dob")
            Gender=request.POST.get("Gender")
            Phn=request.POST.get("Phn")
            Email=request.POST.get("Email")
                
            c.execute("update userregistration set uname='"+Uname+"',address='"+Address+"',dob='"+str(Dob)+"',gender='"+Gender+"', phn='"+str(Phn)+"',email='"+Email+"' where uid='"+request.session["uid"]+"'")
            db.commit()
            return HttpResponseRedirect("/userprofile/")
        if('changeimg' in request.POST):
            return HttpResponseRedirect("/changeimage/")
    else:
        return HttpResponseRedirect("/login")
    return render (request,"edit_userprofile.html",{"data":data})


   
def edit_workerprofile(request):
    if request.session['uname']:    
        uname=request.session['uname']
        c.execute(" select * from workerregistration where workername='"+uname+"'")
        data=c.fetchall()
        for d  in data:
            uidd=d[0]
            request.session["wid"]=str(uidd)
        if(request.POST):
            if 'changeimg' in request.POST:
               return HttpResponseRedirect("/changeimage1/")
            Wname=request.POST.get("Wname")
            Address=request.POST.get("Address")
            Dob=request.POST.get("Dob")
            Gender=request.POST.get("Gender")
            Phn=request.POST.get("Phn")
            Email=request.POST.get("Email")
            Experience=request.POST.get("Experience")     
            c.execute("update workerregistration set workername='"+Wname+"',address='"+Address+"',dob='"+str(Dob)+"',gender='"+Gender+"', phn='"+str(Phn)+"',email='"+Email+"' ,experience='"+str(Experience)+"' where wid='"+request.session["wid"]+"'")
            db.commit()
            
            return HttpResponseRedirect("/workerprofile/")
    else:
        return HttpResponseRedirect("/login/")
    return render (request,"edit_workerprofile.html",{"data":data})
def book(request):
    msg=""
    date1=""
    date2="" 
    if request.session['uname']:   
        wid=request.GET.get("wid")#workerid
        amnt=""
        if(request.POST):
            uname=request.session['uname']
            fdate=request.POST.get("fdate")
            tdate=request.POST.get("tdate")        
            bdate=datetime.date.today()
            date1=datetime.date.today()
            date2=datetime.date.today()
            status="pending"
            c.execute("insert into booking(bdate,sdate,status,dateofcomp,wid,username) values('"+str(bdate)+"','"+str(fdate)+"','"+status+"','"+str(tdate)+"','"+wid+"','"+uname+"')")
            db.commit() 
            
            #retriving bookking id to payment table
            c.execute("select max(bid) from booking")
            bookingid=c.fetchone()
            request.session["bkid"]=bookingid[0] #book id in session

            tyyyy=tdate[0:4]
            fyyyy=fdate[0:4]
            tmm=tdate[5:7]
            fmm=fdate[5:7]
            tdd=tdate[8:10]
            fdd=fdate[8:10]
            fdate=date(int(fyyyy),int(fmm),int(fdd))
            tdate=date(int(tyyyy),int(tmm),int(tdd))
            delta=tdate-fdate
            c.execute("select category.wage from category join workerregistration on workerregistration.category=category.catname where  workerregistration.wid='"+wid+"'")
            dwage=c.fetchone()
            ddd=str(delta)
            q=(ddd[0:1])
            amnt=int(q)*int(dwage[0])
            request.session["amnt"]=amnt
            msg="BOOKING SUCCESSFULLY COMPLETED"    
            return HttpResponseRedirect("/payment/")
    else:
        return HttpResponseRedirect("/login")
    sss=datetime.date.today()
    ss=str(sss)

    return render (request,"book.html",{"amnt":amnt,"date1":date1,"date2":date2,"ss":ss,"msg":msg})
def adminaddcatphoto(request):
    if request.session['uname']:
        c.execute("select * from category")
        data=c.fetchall()
        if(request.POST):
            cid=request.POST.get("cid")
            if(request.FILES['cati']):
                    myfile=request.FILES['cati']
                    fs=FileSystemStorage()
                    filenamme=fs.save(myfile.name,myfile)
                    fileurl=fs.url(filenamme)
                    c.execute("update category set cimage='"+ fileurl +"' where catid='"+ cid +"'")
                    db.commit()
    else:
        return HttpResponseRedirect("/login")
    return render(request,"adminaddcatphoto.html",{"data":data})

def usserviewbookingrequest(request):
    c.execute("select * from booking where username='"+ str(request.session['uname']) +"'")
    dat=c.fetchall()
    return render(request,"usserviewbookingrequest.html",{"dat":dat})

def changeimage(request):
    if request.session['uname']:
        u=request.session['uname']
        c.execute("select * from userregistration where uname='"+u+"'")
        data=c.fetchall()
        for d in data:
            uid=d[0]
        if(request.POST):
            if(request.FILES['img']):
                myfile=request.FILES['img']
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                fileurl=fs.url(filename)
                c.execute("update userregistration set userphoto='"+fileurl+"' where uid='"+str(uid)+"' ")
                db.commit()
                return HttpResponseRedirect("/userprofile/")
            else:
                return HttpResponseRedirect("/login/")
    return render(request,"changeimage.html",{"data":data})
def changeimage1(request):
    if request.session['uname']:
        u=request.session['uname']
        c.execute("select * from workerregistration where workername='"+u+"'")
        data=c.fetchall()
        for d in data:
            wid=d[0]
        if(request.POST):
            if(request.FILES['img']):
                myfile=request.FILES['img']
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                fileurl=fs.url(filename)
                c.execute("update workerregistration set workerphoto='"+fileurl+"' where wid='"+str(wid)+"' ")
                db.commit()
                return HttpResponseRedirect("/workerprofile/")
            else:
                return HttpResponseRedirect("/login/")
    return render(request,"changeimage1.html",{"data":data})
# Create your views here.


def user_accept(request):
    if request.GET:
        st="approved"
        uname=request.GET.get("uname")
        c.execute("update login set status='"+ st +"' where uname='"+ uname +"'")
        db.commit()
    c.execute("select userregistration.name,userregistration.address,userregistration.phn,userregistration.email,login.uname from userregistration join login where login.uname=userregistration.uname and login.status='applied'")
    data=c.fetchall()
    return render(request,'user_accept.html',{"data":data})

def worker_accept(request):
    if request.GET:
        st="approved"
        uname=request.GET.get("uname")
        c.execute("update login set status='"+ st +"' where uname='"+ uname +"'")
        db.commit()
    c.execute("select workerregistration.name,workerregistration.address,workerregistration.phn,workerregistration.email,login.uname from workerregistration join login where login.uname=workerregistration.workername and login.status='applied'")
    data=c.fetchall()
    return render(request,'work_accept.html',{"data":data})