from django.shortcuts import render, get_object_or_404
from .models import Post,Category
from django.http import  HttpResponseRedirect
from .forms import PostForm,UpdateForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView,
)

def CategoryView(request,cats):
	category_values = Post.objects.filter(category=cats.replace('-',' '))
	cat_menu = Category.objects.all()
	context = {'cats':cats,'category_values':category_values,'cat_menu':cat_menu}
	return render(request, 'blog/category.html',context)
	ordering = ['-posted']

def LikeView(request,pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		liked = False
	else:
		post.likes.add(request.user)
		liked = True
	return HttpResponseRedirect(reverse('post-detail',args=[str(pk)]))
	

class HomeView(ListView):
	model = Post
	template_name = 'blog/home.html'
	cats = Category.objects.all()
	ordering = ['-posted']

	def get_context_data(self,*args,**kwargs):
		cat_menu = Category.objects.all()
		context = super(HomeView,self).get_context_data(*args,**kwargs)
		context['cat_menu'] = cat_menu
		return context

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/detail_post.html'
	ordering = ['posted']

	def get_context_data(self,*args,**kwargs):
		cat_menu = Category.objects.all()
		stuff = get_object_or_404(Post, id = self.kwargs['pk'])
		total_likes = stuff.total_llikes()
		liked = False
		if stuff.likes.filter(id=self.request.user.id).exists():
			liked = True
		context = super(PostDetailView,self).get_context_data(*args,**kwargs)
		context['cat_menu'] = cat_menu
		context['total_likes'] = total_likes
		context['liked'] = liked
		return context


class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/add_post.html'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostCategoryView(CreateView):
	model = Category
	template_name = 'blog/add_category.html'
	fields = '__all__'

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
	model = Post
	template_name = 'blog/update_post.html'
	form_class = UpdateForm

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	template_name = 'blog/post_delete.html'
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		else:
			return False

def about(request):
	return render(request, 'blog/about.html')




