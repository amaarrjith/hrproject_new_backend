from django.urls import path
from guest import views

urlpatterns = [
    path('login',views.login,name="login"),
    path('login/<id>',views.login,name="login"),
    path('employees',views.employees,name="employees"),
    path('employees/<id>',views.employees,name="employees"),
    path('bonus',views.bonus,name="bonus"),
    path('bonus/<id>',views.bonus,name="bonus"),
    path('reduction',views.reduction,name="reduction"),
    path('reduction/<id>',views.reduction,name="reduction"),
    path('salary',views.salary,name="salary"),
    path('viewsalary',views.viewsalary,name="viewsalary"),
    path('viewsalary/<id>',views.viewsalary,name="viewsalary"),
    path('generatesalary/<id>',views.generatesalary,name="generatesalary"),
    path('generatesalary',views.generatesalary,name="generatesalary"),
    path('leaverequests/<id>',views.leaveRequest,name="leaveRequest"),
    path('leaverequests',views.leaveRequest,name="leaveRequest"),
    path('leaverequests/<id>',views.leaveRequest,name="leaveRequest"),
    path('approveleave/<id>/<leaveid>',views.approveLeave,name="approveleave"),
    path('declineleave/<id>',views.declineLeave,name="declineleave"),
    path('leavestatus',views.leaveStatus,name="leavestatus"),
    path('generatesalarymonth',views.generatesalarymonth,name="generatesalarymonth"),
    path('getallleavetype',views.getallleavetype,name="getallleavetype"),
    path('remainingleave/<id>',views.remainingleave,name="remainingleave"),
    path('leavereductions',views.leavereductions,name="leavereductions"),
    path('leavereductions/<id>',views.leavereductions,name="leavereductions"),
    path('forgetpassword',views.forgetPassword,name="forgetpassword"),
    path('otpvalidation/<id>',views.otpValidation,name="otpValidation"),
    path('changepassword/<id>',views.changePassword,name="changepassword"),
    path('contactform/<id>',views.contactAdmin,name="contactform"),
    path('contactform',views.contactAdmin,name="contactform"),
    path('checkpolicy',views.checkLeavePolicy,name="checkpolicy"),
    path('checkmonth',views.checkMonth,name="checkmonth"),
    path('checkstatus',views.checkStatus,name="checkstatus"),
    path('addpolicy',views.addpolicy,name="addpolicy"),
    path('blockemployee/<id>',views.blockemployee,name="blockemployee"),
    path('unblockemployee/<id>',views.unblockemployee,name="unblockemployee"),
    path('count',views.count,name="count")
    
    
]