from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import Category, Comment, Donation, Project, Picture, Rate, Tag,FeaturedProject
from Users.models import User
from .forms import AddProject
from django.http import JsonResponse
from Users.models import Profile
from django.utils import timezone
from django.db.models import Max
from django.db.models import Q


def add_project(request):
    submitted = False
    if request.method == 'POST':
        form = AddProject(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            project = Project()
            project.title = cd['title']
            project.details = cd['Details']
            project.category = cd['Category']
            project.current_money = cd['CurrentMoney']
            project.total_target = cd['TotalTarget']
            project.end_time = cd['EndTime']
            project.user_id = cd['UserId']
            project.save()
            for tag in cd['Tags']:
                project.tags.add(tag)

            for file in request.FILES.keys():
                image_file = request.FILES.getlist(file)
                print("imffileeee", image_file)
                for i in image_file:
                    fs = FileSystemStorage()
                    filename = fs.save('images/projects/' + i.name, i)
                    img = Picture()
                    img.pic_path = filename
                    img.project_id = project
                    img.save()

            return render(request, "Projects/home_page.html")
    else:
        form = AddProject()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'Projects/add_project.html', {'form': form, 'submitted': submitted})



def project_details(request, _id):
    project = Project.objects.get(id=_id)
    print(project)
    pictures = Picture.objects.filter(project_id=_id)
    print(pictures)
    comments = Comment.objects.filter(project_id=_id).values('user_id', 'comment_body')
    commentsdict = []
    for comment in comments:
        print(comment)
        commentsdict.append(tuple([User.objects.get(id=comment['user_id']), comment['comment_body']]))
    tags = project.tags.all()
    print(commentsdict)
    print(tags)
    donation = project.current_money / project.total_target
    picnum = []

    if Rate.objects.get(project_id=_id, user_id=1):
        rate = Rate.objects.get(project_id=_id, user_id=1)
        ratenum = int(str(rate).split(":", 4)[3])
    else:
        ratenum = 0

    print(ratenum)
    for i in range(len(pictures)):
        picnum.append(i)
    context = {
        'project': project,
        'pictures': pictures,
        'picnum': picnum,
        'donationbar': donation,
        'comments': commentsdict,
        'tags': tags,
        'rate': ratenum,
        # must be get from session
        "user": User.objects.get(id=1)
    }
    return render(request, 'Projects/project_details.html', context)


def project_comment(request):
    if request.is_ajax and request.method == "GET":
        comment = Comment()
        print("comment", request.GET['comment'])
        comment.comment_body = request.GET['comment']
        comment.project_id = Project.objects.get(id=request.GET['id'])
        comment.user_id = User.objects.get(id=1)
        comment.save()

    if comment:
        return JsonResponse({"done": "done"})
    else:
        return JsonResponse({"error": "error"})


def project_rate(request):
    if request.is_ajax and request.method == "POST":

        result = Rate.objects.update_or_create(
            project_id=Project.objects.get(id=request.POST['id']), user_id=User.objects.get(id=1),
            defaults={'rate': request.POST['rate']}, )

        if result:
            return JsonResponse({"done": "done"})
        else:
            return JsonResponse({"error": "error"})


def all_projects(request):
    all_projects = Project.objects.all()
    all_pictures = Picture.objects.all()
    all_profiles = Profile.objects.all()
    all_rates = Rate.objects.all()
    for i in all_projects:
        i.pics = [pic.pic_path.url for pic in filter(lambda e: e.project_id_id == i.id, all_pictures)]
        if len(i.pics) == 0:
            i.pics = ["/static/images/projects/default_project.jpg"]
        try:
            i.user_pic = [pic.profile_pic.url for pic in filter(lambda e: e.user_id == i.user_id_id, all_profiles)][0]
        except IndexError as identifier:
            i.user_pic = "/static/images/profiles/default_profile.png"
        i.remaining = str(i.end_time - timezone.localtime(timezone.now()).date()).split(",")[0]
        i.progress = (i.current_money / i.total_target) * 100
        project_rates = [project.rate for project in filter(lambda e: e.project_id_id == i.id, all_rates)]
        try:
            i.rate_percentage = ((sum(project_rates) / len(project_rates)) / 5) * 100
            i.rate = round(((sum(project_rates) / len(project_rates))), 1)
        except ZeroDivisionError as identifier:
            i.rate_percentage = 0
            i.rate = 0
    return render(request, 'Projects/all_projects.html', {'all_projects': all_projects})

def home_page(request):
    top_rated = []
    top_rated = Rate.objects.values('project_id') \
                    .annotate(rate=Max('rate')) \
                    .order_by('-rate')[:5]
    projects = []
    latest_projects = []
    featured_projects = []
    for pro in top_rated:
        projects.append(Picture.objects.filter(project_id=pro['project_id'])[:1])
    latest = Project.objects.values('id').order_by('-start_time')[:5]
    for pro in latest:
        latest_projects.append(Picture.objects.filter(project_id=pro['id'])[:1])
    featured = FeaturedProject.objects.values('id')[:5]
    for pro in featured:
        featured_projects.append(Picture.objects.filter(project_id=pro['id']))
    categories = Category.objects.all()
    return render(request, "Projects/home_page.html", {'top_rated': projects,
                                                       'latest_projects': latest_projects,
                                                       'featured_projects': featured_projects,
                                                       'categories': categories})


def project_list(request, id):
    project_list = []
    category_proj = Project.objects.filter(category=int(id)).values(('id'))
    for pro in category_proj:
        project_list.append(Picture.objects.filter(project_id=pro['id']))
    return render(request, 'Projects/project_list.html', {'project_list': project_list})


def search_projects(request):
    # print(data)
    project_list=[]
    if request.method == 'GET':
        query = request.GET.get('q')
        print(query)
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(tags__tag_name__icontains=query)
            results=Project.objects.filter(lookups).values('id').distinct()
            print(results)
            for pro in results:
                project_list.append(Picture.objects.filter(project_id=pro['id']))
            return render(request, 'Projects/project_list.html', {'project_list': project_list,
                             })
        else:
            return render(request, 'Projects/project_list.html')
    else:
        return render(request, 'Projects/project_list.html')
