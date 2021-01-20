from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import UserRegisterForm,UserUpdateForm,Note_PasswordForm,Note_Change_PasswordForm,Note_Confirm_PasswordForm,NoteForm,Share_the_PostForm
from .models import Note,Note_Password,Category
from django.contrib.auth.models import User
from django.template.defaultfilters import striptags
from .templatetags.blog_tags import markdown_format

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings 

from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView

from django.db.models import Q

from django.contrib import messages

item_dict={}

def register(request):
	if request.method == 'POST':
		user_from = UserRegisterForm(request.POST)
		if user_from.is_valid():
			user_from.save()
			username = user_from.cleaned_data.get('username')
			return redirect('login')

	else:
		user_from=UserRegisterForm()
	return render(request,'notes_register/register.html',{'form':user_from,'section':'Register'})

@login_required
def dashboard(request):
	return render(request,'noteshtmls/dashboard.html',{'section':'Dashboard'})

def intropage(request):
	return render(request,'noteshtmls/intro.html',{'section':'INRO'})

@login_required
def profile_page(request):
	if request.method == 'POST':
		user_edit_form = UserUpdateForm(data=request.POST,instance=request.user)
		
		if user_edit_form.is_valid():
			user_edit_form.save()
			messages.success(request, f'''Your Profile  <a href="{reverse('profile_page')}" class="alert-link">"{request.user.username}"</a> Updated  Successfully''')
			# messages.success(request,f'{ request.user.username } ACCOUNT HAS BEEEN UPPDATED !!')		
			return redirect('dashboard')
		# else:
	else:
		user_edit_form=UserUpdateForm(instance=request.user)
		context={
			'user_edit_form':user_edit_form,'section':'Profile Page'}
		
		return render(request,'noteshtmls/profile.html',context)



@login_required
def NoteCreateView(request):

	if request.method == 'POST':
	 	form=NoteForm(request.POST)
	 	if form.is_valid():
	 		cd=form.cleaned_data
	 		form=form.save(commit=False)
	 		form.author = request.user
	 		form.category=Category.objects.first()
	 		
	 		if cd.get('password_required'):
	 			item_dict['save_the_note']=form
	 			request.session['allow_if_password_is_confirm']=False
	 			return redirect('check_password')
	 		else:
	 			form.save()
	 			return redirect(Note.objects.filter(author=request.user).latest().get_absolute_url())



	else:
		form=NoteForm()
	return render(request,'noteshtmls/add_note.html',{'form':form})	

@login_required
def notes_by_user(request):
	all_notes=Note.objects.filter(author=request.user).filter(category=Category.objects.first())[::-1]
	return render(request,'noteshtmls/dashboard.html',{'all_notes':all_notes,'category':Category.objects.first().title})


@login_required
def NoteDetailView(request,pk):
	global item_dict
	note=Note.objects.filter(author=request.user).get(id=pk)
	if note.password_required:
		if request.session.get('allow_if_password_is_confirm'):
			request.session['allow_if_password_is_confirm']=False
			item_dict={}
			return render(request,'noteshtmls/note_view.html',{'note':note})
		else:
			item_dict['set_this_detail_view']=note.pk
			return redirect('check_password')
	else:
		return render(request,'noteshtmls/note_view.html',{'note':note})


@login_required
def NoteUpdateView(request,pk):
	obj = get_object_or_404(Note, id = pk)

	form = NoteForm(request.POST or None, instance = obj)

	if form.is_valid(): #send form
		cd=form.cleaned_data
		if cd.get('password_required') or  (obj.password_required):
			item_dict['update_the_note']=[form,pk]
			request.session['allow_if_password_is_confirm']=False
			return redirect('check_password')
		else:
			form.save()
			messages.success(request, f'''Note <a href="{reverse('note_update',args=[str(obj.pk)])}" class="alert-link">"{obj.heading}"</a> successfully''')
			return redirect(Note.objects.filter(author=request.user).get(id=pk).get_absolute_url())

	else:#want form
		if (not obj.password_required) or request.session.get('allow_if_password_is_confirm'):
			return render(request,'noteshtmls/note_update.html',{'form':form,'object':obj})	
		elif (obj.password_required):
			request.session['allow_if_password_is_confirm']=False
			item_dict['allow_update_form']=obj.pk
			return redirect('check_password')


	
@login_required
def set_note_password(request):
	try:
		request.user.note_password
		return redirect('set_change_password')


	except:
		if request.method=='POST':
			note_password_form=Note_PasswordForm(request.POST)
			if note_password_form.is_valid():
				cd=note_password_form.cleaned_data
				note_password_form=note_password_form.save(commit=False)
				note_password_form.author = request.user
				note_password_form.save()
				if request.session.get('confirm_password'):
					return redirect('check_password')	
				else:
					messages.success(request, f'''Your Password Has Been Successfully Set <a href="{reverse('set_change_password')}" class="alert-link">"Click Here"</a> To Change it  ''')
					return redirect('dashboard')
		else:
			note_password_form=Note_PasswordForm()
		return render(request,'noteshtmls/password_set_for_lock_notes.html',{'note_password_form':note_password_form})	

@login_required
def set_note_password_change(request):
	request.user.note_password

	if request.method == 'POST':
		change_password_form=Note_Change_PasswordForm(request.POST)
		if change_password_form.is_valid():
			cd=change_password_form.cleaned_data
			if request.user.note_password.password == cd.get('password'):
				new_password=cd.get('password1')
				Ouruser=User.objects.get(username=request.user.username)
				Ouruser.note_password.password=new_password
				Ouruser.note_password.save()
				messages.success(request, f'''Your Password Changed Has Been Successfully Set <a href="{reverse('set_change_password')}" class="alert-link">"Click Here"</a> To Change it Again ''')

				return redirect('dashboard')
			else:
				messages.error(request, f'''Make Sure You Enter Correct Password ''')
				return redirect(reverse('set_change_password'))
	else:
		change_password_form=Note_Change_PasswordForm()

	return render(request,'noteshtmls/password_change_form.html',{'change_password_form':change_password_form})

@login_required
def confirm_password_view(request):
	try:
		request.user.note_password
		if request.method == 'POST':
			check_password_form=Note_Confirm_PasswordForm(request.POST)
			if check_password_form.is_valid():
				cd=check_password_form.cleaned_data
				if cd.get('password')== request.user.note_password.password:
					if not request.session.get('allow_if_password_is_confirm'):
						if  item_dict.get('save_the_note'):
							item_dict['save_the_note'].save()
							request.session['allow_if_password_is_confirm']=True
							del item_dict['save_the_note']
							return redirect(Note.objects.filter(author=request.user).latest().get_absolute_url())

						elif item_dict.get('set_this_detail_view'):
							request.session['allow_if_password_is_confirm']=True
							return redirect(Note.objects.filter(author=request.user).get(id=item_dict['set_this_detail_view']).get_absolute_url())

						elif item_dict.get('update_the_note'):
							request.session['allow_if_password_is_confirm']=True
							item_dict['update_the_note'][0].save()
							return redirect(Note.objects.filter(author=request.user).get(id=item_dict['update_the_note'][1]).get_absolute_url())
						elif item_dict.get('allow_update_form'):
							request.session['allow_if_password_is_confirm']=True
							return redirect(reverse('note_update',args=[str(item_dict.get('allow_update_form'))]))
						elif item_dict.get('allow_share_form'):
							request.session['allow_if_password_is_confirm']=True
							return redirect(reverse('share_note_by_email',args=[str(item_dict.get('allow_share_form'))]))

							

				else:
					messages.error(request, f'''Make Sure You Enter Correct Password ''')


					
			
		else:
			check_password_form=Note_Confirm_PasswordForm()
		return render(request,'noteshtmls/check_set_password.html',{'check_password_form':check_password_form})

	except:
		request.session['confirm_password']=True
		return redirect('set_password')

@login_required
def SearchResultsListView(request):
	query = request.GET.get('q')
	all_notes=Note.objects.filter(author=request.user).filter(Q(heading__icontains=query)|Q(description__icontains=query))
	return render(request,'noteshtmls/search_results.html',{'all_notes':all_notes,'query':query})

@login_required
def move_to_trash(request,pk):
	obj=Note.objects.filter(author=request.user).get(id=pk)
	trash_category=Category.objects.get(title='Trash')
	obj.category=trash_category
	obj.save()
	messages.success(request, f'''Your Note <a href="{reverse('note_detail',args=[str(pk)])}" class="alert-link">"{obj.heading}"</a> Has Been Move Trash''')
	return redirect('dashboard')

@login_required
def move_to_archive(request,pk):
	obj=Note.objects.filter(author=request.user).get(id=pk)
	archive_category=Category.objects.get(title='Archive')
	obj.category=archive_category
	obj.save()
	messages.success(request, f'''Your Note <a href="{reverse('note_detail',args=[str(pk)])}" class="alert-link">"{obj.heading}"</a> Has Been Move Archive''')
	return redirect('dashboard') 

@login_required
def move_to_untagged(request,pk):
	obj=Note.objects.filter(author=request.user).get(id=pk)
	untagged_category=Category.objects.get(title='Un taged')
	obj.category=untagged_category
	obj.save()
	messages.success(request, f'''Your Note <a href="{reverse('note_detail',args=[str(pk)])}" class="alert-link">"{obj.heading}"</a> Has Been Move Un-tagged''')
	return redirect('dashboard') 


@login_required
def show_objects_category(request,category):
	category=Category.objects.get(title=category)
	all_notes=Note.objects.filter(author=request.user).filter(category=category)[::-1]

	return render(request,'noteshtmls/dashboard.html',{'all_notes':all_notes,'category':category})


@login_required
def show_favorites_notes(request):
	all_notes=Note.objects.filter(author=request.user).filter(add_to_fav=True)[::-1]
	return render(request,'noteshtmls/dashboard.html',{'all_notes':all_notes,'category':'Favorites'})


@login_required
def show_lock_notes(request):
	all_notes=Note.objects.filter(author=request.user).filter(password_required=True)[::-1]
	return render(request,'noteshtmls/dashboard.html',{'all_notes':all_notes,'category':'Lock Notes'})
	
@login_required
def remove_all_notes_trash_to_untagged(request):
	trash_category=Category.objects.get(title='Trash')
	untagged_category=Category.objects.get(title='Un taged')
	all_notes=Note.objects.filter(author=request.user).filter(category=trash_category)
	for note in all_notes:
		note.category = untagged_category
		note.save()
	messages.success(request, f'''All Notes From Trash Successfully Restore !! <a href="{reverse('dashboard')}" class="alert-link">"Go To DashBoard"</a>''')
	return redirect('dashboard') 

@login_required
def delete_notes_from_trash(request,pk=None):
	trash_category=Category.objects.get(title='Trash')
	if pk :
		note=Note.objects.filter(author=request.user).filter(category=trash_category).get(id=pk)	
		messages.error(request, f''' The "{note.heading}" is  Permanently Deleted Successfully''')
		note.delete()
	else:
		all_notes=Note.objects.filter(author=request.user).filter(category=trash_category)
		all_notes.delete()
		messages.error(request, f'''All Notes From Trash Are Permanently Deleted Successfully !! <a href="{reverse('dashboard')}" class="alert-link">"Go To DashBoard"</a>''')
	return redirect('dashboard') 

@login_required
def share_note_by_email(request,pk):
	if request.method == 'POST':
		Share_Form=Share_the_PostForm(request.POST)
		if Share_Form.is_valid():
			cd=Share_Form.cleaned_data
			cd['username']=request.user.username
			sub=cd['subject']
			subject=f'{request.user.username} Send You Note of Subject {sub} !!'
			html_message = render_to_string('share_email.html', {'cd': cd,})
			plain_message = strip_tags(html_message)
			from_email = settings.EMAIL_HOST_USER
			to = [cd.get('email')]
			t=send_mail(subject, plain_message, from_email,to,html_message=html_message)
			try:
				if t:
					messages.success(request, f'''Your Mail Has Been Successfully send''')
			except :
				messages.error(request, f'''Your Mail Has Been <b>Not Send</b>''')
			return redirect('dashboard')

	else:
		obj=Note.objects.filter(author=request.user).get(id=pk)
		if (not obj.password_required) or request.session.get('allow_if_password_is_confirm'):
			initial_dict = { 
		        "subject" : obj.heading, 
		        "content":striptags(markdown_format(obj.description))}
			Share_Form=Share_the_PostForm(initial = initial_dict)
			return render(request, "noteshtmls/share_note.html",{'Share_Form':Share_Form}) 
			
		elif (obj.password_required):
			request.session['allow_if_password_is_confirm']=False
			item_dict['allow_share_form']=obj.pk
			return redirect('check_password')

@login_required
def sort_by_color(request,color):
	all_notes=Note.objects.filter(author=request.user).filter(colour_of_notes=color)[::-1]
	return render(request,'noteshtmls/dashboard.html',{'all_notes':all_notes,'category':color.upper()+' colors Notes'})












		




    



