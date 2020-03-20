from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import Category, Comment, Donation, Project, Picture, Rate, Tag
from Users.models import User
from .forms import AddProject
from django.http import JsonResponse


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


def home_page(request):
    return render(request, "Projects/home_page.html")


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
    rate = Rate.objects.get(project_id=_id,user_id=1)
    ratenum=int(str(rate).split(":", 4)[3])
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
        'rate':ratenum,
        # must be get from session
        "user": User.objects.get(id=1)
    }
    return render(request, 'Projects/project_details.html', context)


def project_comment(request):
    if request.is_ajax and request.method == "GET":
        comment = Comment()
        print("comment",request.GET['comment'])
        comment.comment_body = request.GET['comment']
        comment.project_id =Project.objects.get(id= request.GET['id'])
        comment.user_id = User.objects.get(id=1)
        comment.save()

    if comment.save():
        return JsonResponse({"done": "done"})
    else:
        return JsonResponse({"error": "error"})


def project_rate(request):
    if request.is_ajax and request.method == "POST":

        Rate.objects.update_or_create(
            project_id=Project.objects.get(id=request.POST['id']), user_id=User.objects.get(id=1),
            defaults={'rate': request.POST['rate']}, )

        if True:
            return JsonResponse({"done": "done"})
        else:
            return JsonResponse({"error": "error"})
