from django.shortcuts import render
from .models import Picture,Project,Rate
from Users.models import Profile
from django.utils import timezone

def home_page(request):
    return render(request,"Projects/home_page.html")

# ==================================ramy's task====================================
def all_projects(request):
    all_projects=Project.objects.all()
    all_pictures=Picture.objects.all()
    all_profiles=Profile.objects.all()
    all_rates=Rate.objects.all()
    for i in all_projects:
        i.pics=[pic.pic_path.url for pic in filter(lambda e: e.project_id_id == i.id,all_pictures )]
        if len(i.pics)==0 :
            i.pics=["/static/images/projects/default_project.jpg"]
        try:
            i.user_pic=[pic.profile_pic.url for pic in filter(lambda e:e.user_id==i.user_id_id,all_profiles)][0]
        except IndexError as identifier:
            i.user_pic="/static/images/profiles/default_profile.png"
        i.remaining=str(i.end_time-timezone.localtime(timezone.now()).date()).split(",")[0]
        i.progress=(i.current_money/i.total_target)*100
        project_rates=[project.rate for project in filter(lambda e:e.project_id_id==i.id,all_rates)]
        try:
            i.rate_percentage=((sum(project_rates)/len(project_rates))/5)*100
            i.rate=round(((sum(project_rates)/len(project_rates))),1)
        except ZeroDivisionError as identifier:
            i.rate_percentage=0
            i.rate=0
    return render(request,'Projects/all_projects.html',{'all_projects':all_projects})
# ==================================ramy's task====================================