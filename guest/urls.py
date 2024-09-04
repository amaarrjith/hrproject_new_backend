from django.urls import path
from guest import views

urlpatterns = [
    path('login',views.login,name="login"),
    path('login/<id>',views.login,name="login"),
    path('employees',views.employees,name="employees"),
    path('employees/<id>',views.employees,name="employees"),
    path('bonus',views.bonus,name="bonus"),
    path('reduction',views.reduction,name="reduction"),
    path('salary',views.salary,name="salary"),
    path('viewsalary',views.viewsalary,name="viewsalary")
    
]