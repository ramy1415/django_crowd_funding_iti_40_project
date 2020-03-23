from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .models import Category, Comment, Donation, Project, Picture, Rate, Tag, FeaturedProject, ReportProject
from Users.models import User
from .forms import AddProject, EditProject
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseServerError
from Users.models import Profile
from django.utils import timezone
from django.db.models import Max
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required
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
            project.user_id = request.user
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

            return HttpResponseRedirect('/projects')

    else:
        form = AddProject()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'Projects/add_project.html', {'form': form, 'submitted': submitted})


@login_required
def edit_project(request, _id):
    submitted = False
    if request.method == 'POST':
        project = Project.objects.get(id=_id)
        edit_form = EditProject(request.POST, instance=project)
        edit_form.save()

        return HttpResponseRedirect('/projects/' + str(_id))
    else:
        if 'submitted' in request.GET:
            submitted = True
        project = Project.objects.get(id=_id)
        edit_form = EditProject(instance=project)

    return render(request, 'Projects/edit_project.html', {'edit_form': edit_form, 'submitted': submitted})

@login_required
def project_details(request, _id):
    project = Project.objects.get(id=_id)
    print(project)
    pictures = Picture.objects.filter(project_id=_id)
    print(pictures)
    comments = Comment.objects.filter(project_id=_id).values('user_id', 'comment_body')
    commentsdict = []

    for comment in comments:
        print(comment)
        commentuserimags = Profile.objects.filter(user=comment['user_id']).values('profile_pic')
        if commentuserimags:
            commentuserimg = commentuserimags[0]
        else:
            commentuserimg = 0
        commentsdict.append(tuple([User.objects.get(id=comment['user_id']), commentuserimg, comment['comment_body']]))
    tags = project.tags.all()
    print("alaa", commentsdict)
    print(tags)
    donation = project.current_money / project.total_target
    picnum = []

    try:

        rate = Rate.objects.get(project_id=_id, user_id=request.user)
        ratenum = int(str(rate).split(":", 4)[3])
    except:
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
        "user": request.user,
    }
    return render(request, 'Projects/project_details.html', context)

@login_required
def project_comment(request):
    if request.is_ajax and request.method == "GET":
        comment = Comment()
        print("comment", request.GET['comment'])
        comment.comment_body = request.GET['comment']
        comment.project_id = Project.objects.get(id=request.GET['id'])
        comment.user_id = request.user
        comment.save()

    if comment:
        return JsonResponse({"done": "done"})
    else:
        return JsonResponse({"error": "error"})


@login_required
def project_rate(request):
    if request.is_ajax and request.method == "POST":

        result = Rate.objects.update_or_create(
            project_id=Project.objects.get(id=request.POST['id']), user_id=request.user,
            defaults={'rate': request.POST['rate']}, )

        if result:
            return JsonResponse({"done": "done"})
        else:
            return JsonResponse({"error": "error"})


@login_required
def delete_image(request):
    if request.is_ajax and request.method == "GET":
        result = Picture.objects.filter(project_id=request.GET['id'], pic_path=request.GET['img']).delete()

    if result:
        return JsonResponse({"done": "done"})
    else:
        return JsonResponse({"error": "error"})


@login_required
def add_image(request):
    if request.method == 'POST':
        # print("imffileeee", image_file)
        if request.FILES.getlist('images'):
            image_file = request.FILES.getlist('images')
            for i in image_file:
                fs = FileSystemStorage()
                filename = fs.save('images/projects/' + i.name, i)
                img = Picture()
                img.pic_path = filename
                project = Project.objects.get(id=request.POST['project'])
                img.project_id = project
                img.save()

                print(project)
    if img:
        return HttpResponseRedirect("/projects")
    else:
        return HttpResponseServerError


@login_required
def add_donation(request):
    if request.is_ajax and request.method == "GET":
        new_donation = int(request.GET['donation'])
        project = Project.objects.get(id=request.GET['id'])
        oldprojectdonation = project.current_money
        resulte = Project.objects.filter(id=request.GET['id']).update(current_money=oldprojectdonation + new_donation)
        try:
            donation = Donation.objects.get(user_id=request.user, project_id=Project.objects.get(id=request.GET['id']))
            old_donation = donation.amount
            new_donation += int(old_donation)
            res = Donation.objects.filter(user_id=request.user,
                                          project_id=Project.objects.get(id=request.GET['id'])).update(
                amount=new_donation)

            if res and resulte:
                return JsonResponse({"done": "done"})
            else:
                return JsonResponse({"error": "error"})

        except Donation.DoesNotExist:
            donation = Donation(user_id=request.user, project_id=Project.objects.get(id=request.GET['id']),
                                amount=new_donation)
            donation.save()

            if donation and resulte:
                return JsonResponse({"done": "done"})
            else:
                return JsonResponse({"error": "error"})


# ========================================================================ramy's tasks==================================================================
# ramy
@login_required(login_url='/login')
def add_project_report(request):  # ajax report
    if request.method == 'POST':
        if request.POST.get('body') != "":
            report = ReportProject()
            report.project_id = Project.objects.get(id=request.POST.get('project_id'))
            report.user_id = request.user
            report.report_project_body = request.POST.get('body')
            report.save()
            if report.id:  # if the report was added send back to user the message
                return JsonResponse({"message": "Thanks for letting us know"})


# ramy
@login_required(login_url='/login')
def del_project_report(request):  # ajax remove report
    if request.method == 'POST':
        delete = ReportProject.objects.get(user_id=request.user, project_id=request.POST.get('project_id')).delete()
        if delete:  # if the report was deleted send back to user the message
            return JsonResponse({"message": "removed your report"})


# ramy
@login_required(login_url='/login')
def all_projects(request):
    if request.method == 'POST':  # ajax add comment
        if request.POST.get('comment') != "":
            comment = Comment()
            comment.comment_body = request.POST.get('comment')
            comment.project_id = Project.objects.get(id=request.POST.get('project_id'))
            comment.user_id = request.user
            comment.save()
            if comment.id:
                return JsonResponse({})

    all_projects = Project.objects.all()
    all_pictures = Picture.objects.all()
    all_comments = Comment.objects.all().order_by('-id')
    all_rates = Rate.objects.all()
    all_reports = ReportProject.objects.all()
    try:
        user_pic_url = Profile.objects.get(user=request.user).profile_pic.url  # getting the user pic who created this project
    except Profile.DoesNotExist as identifier:
        user_pic_url = "/static/images/profiles/default_profile.png"

    for i in all_projects:
        i.pics = [pic.pic_path.url for pic in
                  filter(lambda e: e.project_id_id == i.id, all_pictures)]  # getting this project pics
        if len(i.pics) == 0:
            i.pics = ["/static/images/projects/default_project.jpg"]

        if i.end_time > timezone.localtime(
                timezone.now()).date():  # getting the remainig time for the project till ending
            i.remaining = "Ends in " + str(i.end_time - timezone.localtime(timezone.now()).date()).split(",")[0]
        else:
            i.remaining = "Ended"

        i.progress = (i.current_money / i.total_target) * 100  # getting the amount of money donated

        project_rates = [project.rate for project in filter(lambda e: e.project_id_id == i.id,
                                                            all_rates)]  # a list of all ratings from all users on that project

        project_reports = [report.user_id for report in filter(lambda e: e.project_id_id == i.id,
                                                               all_reports)]  # a list of all reports from all users on that project
        i.project_reports = len(project_reports)

        if request.user in project_reports:  # checking if this user already reported this project
            i.is_reported = True
        else:
            i.is_reported = False

        i.comments = [{'body': comment.comment_body, 'user': comment.user_id} for comment in
                      filter(lambda e: e.project_id_id == i.id, all_comments)]
        # getting the comments on this project and the user who added it

        try:
            i.rate_percentage = ((sum(project_rates) / len(
                project_rates)) / 5) * 100  # getting the overall rating percentage
            i.rate = round(((sum(project_rates) / len(project_rates))), 1)  # getting the rating of 5 ex 4.7/5
        except ZeroDivisionError as identifier:
            i.rate_percentage = 0
            i.rate = 0

    return render(request, 'Projects/all_projects.html', {'all_projects': all_projects, 'user_pic_url': user_pic_url})


# ========================================================================end of ramy's tasks==================================================================


# esraa
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


# esraa
def project_list(request, id):
    project_list = []
    category_proj = Project.objects.filter(category=int(id)).values(('id'))
    for pro in category_proj:
        project_list.append(Picture.objects.filter(project_id=pro['id']))
    return render(request, 'Projects/project_list.html', {'project_list': project_list})


# esraa
def search_projects(request):
    # print(data)
    project_list = []
    if request.method == 'GET':
        query = request.GET.get('q')
        print(query)
        submitbutton = request.GET.get('submit')
        if query is not None:
            lookups = Q(title__icontains=query) | Q(tags__tag_name__icontains=query)
            results = Project.objects.filter(lookups).values('id').distinct()
            print(results)
            for pro in results:
                project_list.append(Picture.objects.filter(project_id=pro['id']))
            return render(request, 'Projects/project_list.html', {'project_list': project_list,
                                                                  })
        else:
            return render(request, 'Projects/project_list.html')
    else:
        return render(request, 'Projects/project_list.html')
