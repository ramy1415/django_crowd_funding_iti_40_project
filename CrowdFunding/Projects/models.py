from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=50)
    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    def __str__(self):
        return self.tag_name

class Project(models.Model):
    title = models.CharField(max_length=50,blank=False,null=False)
    details = models.TextField(blank=False,null=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    current_money = models.IntegerField(default=0)
    total_target = models.IntegerField(blank=False, null=False)
    tags = models.ManyToManyField(Tag)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField()
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class ReportProject(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_project_body = models.TextField()
    def __str__(self):
        return self.project_id.title

class Picture(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    pic_path = models.ImageField(
        upload_to='images/projects/')

class Comment(models.Model):
    project_id = models.ForeignKey(Project,on_delete=models.CASCADE)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    comment_body = models.TextField()
    def __str__(self):
        return self.comment_body

class ReportComment(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_comment_body = models.TextField()
    def __str__(self):
        return self.comment_id.comment_body

class Donation(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    def __str__(self):
        return str(self.user_id) +" : donated : "+ str(self.project_id) +" : "+ str(self.amount)

class Rate(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    project_rates = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5")
    )
    rate = models.IntegerField(choices=project_rates, default=1)
    class Meta:
        unique_together = ('project_id', 'user_id')

    def __str__(self):
        return str(self.user_id) +" : rated : "+ str(self.project_id) +" : "+ str(self.rate)

class FeaturedProject(models.Model):
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_id.title