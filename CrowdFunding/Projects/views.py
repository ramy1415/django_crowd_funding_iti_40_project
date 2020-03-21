from django.shortcuts import render
from Projects.models import Rate
from Projects.models import Picture
from Projects.models import Project
from Projects.models import FeaturedProject
from Projects.models import Category
from django.db.models import Max
from django.db.models import Q


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
# if request.method == 'GET':
#     query= request.GET.get('q')
#
#     submitbutton= request.GET.get('submit')
#
#     if query is not None:
#         lookups= Q(title__icontains=query) | Q(content__icontains=query)
#
#         results= Post.objects.filter(lookups).distinct()
#
#         context={'results': results,
#                  'submitbutton': submitbutton}
#
#         return render(request, 'search/search.html', context)
#
#     else:
#         return render(request, 'search/search.html')
#
# else:
#     return render(request, 'search/search.html')
