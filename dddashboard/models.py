from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _

# Create your models here.

# class Customer(models.Model):
# 	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
# 	name = models.CharField(max_length=200, null=True)
# 	phone = models.CharField(max_length=200, null=True)
# 	email = models.CharField(max_length=200, null=True)
# 	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)

# 	def __str__(self):
# 		return self.name

class Dashboard_user(models.Model):

    # class UserGroup(models.TextChoices):
    #     admin = 'admin', _('admin')
    #     user = 'user', _('user')

    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    # name = User.objects.get('name')
    name = models.CharField(max_length=200, null=True)
    # company = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    # profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    company_name = models.ForeignKey('CompanyName', on_delete=models.CASCADE, null=True, blank=False)
    user_group = models.ForeignKey(Group, null=True, on_delete=models.CASCADE)
    # user_group = models.OneToOneField(null=True, on_delete=models.CASCADE, choices=UserGroup.choices)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Dashboard Users"






# class Tag(models.Model):
# 	name = models.CharField(max_length=200, null=True)

# 	def __str__(self):
# 		return self.name

# class Product(models.Model):
# 	CATEGORY = (
# 			('Indoor', 'Indoor'),
# 			('Out Door', 'Out Door'),
# 			) 

# 	name = models.CharField(max_length=200, null=True)
# 	price = models.FloatField(null=True)
# 	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
# 	description = models.CharField(max_length=200, null=True, blank=True)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	tags = models.ManyToManyField(Tag)

# 	def __str__(self):
# 		return self.name

# class Order(models.Model):
# 	STATUS = (
# 			('Pending', 'Pending'),
# 			('Out for delivery', 'Out for delivery'),
# 			('Delivered', 'Delivered'),
# 			)

# 	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
# 	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
# 	date_created = models.DateTimeField(auto_now_add=True, null=True)
# 	status = models.CharField(max_length=200, null=True, choices=STATUS)
# 	note = models.CharField(max_length=1000, null=True)

# 	def __str__(self):
# 		return self.product.name

class CompanyName(models.Model):
	name = models.CharField(max_length=200, null=True, blank=False)

	def __str__(self):
		return self.name


class CompanySize(models.Model):
    class sizes(models.TextChoices):
        small = 'small', _('small')
        medium = 'medium', _('medium')
        large = 'large', _('large')
        

    company_size = models.CharField(
        max_length=50,
        choices=sizes.choices,
        null=True,
        )


class CompanyData(models.Model):

    


    name = models.ForeignKey(
        'CompanyName',
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )

    size = models.ForeignKey(
        "CompanySize",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    class GenderCode(models.TextChoices):
        male = 'M', _('Male')
        female = 'F', _('Female')
        Other = 'O', _('Other')

    gender_code = models.CharField(
        max_length=1,
        choices=GenderCode.choices,
        null=True,
    )


    class AboriginalPeoples(models.TextChoices):
        yes = 'Y', _('Yes')
        no = 'N', _('No')

    aboriginal_peoples = models.CharField(
        max_length=1,
        choices=AboriginalPeoples.choices,
        null=True,
    )

    class VisibleMinorities(models.TextChoices):
        yes = 'Y', _('Yes')
        no = 'N', _('No')

    visible_minorities = models.CharField(
        max_length=1,
        choices=VisibleMinorities.choices,
        null=True,
    )
	
    class PersonWithDisabilities(models.TextChoices):
        yes = 'Y', _('Yes')
        no = 'N', _('No')

    person_with_disabilities = models.CharField(
        max_length=1,
        choices=PersonWithDisabilities.choices,
        null=True,
    )

    class PositionCategory(models.TextChoices):
        executive = 'Executive', _('Executive')
        senior_leader = 'Senior Leader', _('Senior Leader')
        manager_s_s = 'Manager/Supervisor/Superintendent', _('Manager/Supervisor/Superintendent')
        foreperson = 'Foreperson', _('Foreperson')
        individual_contributor = 'Individual Contributor', _('Individual Contributor')

    position_category = models.CharField(
        max_length=200,
        choices=PositionCategory.choices,
        null=True,
    )



		
