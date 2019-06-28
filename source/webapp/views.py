from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from webapp.forms import ArticleForm, CommentForm, UserForm
from webapp.models import Article, Comment, Rate
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Sum
import json

class ArticleListView(ListView):
    template_name = 'article_list.html'
    model = Article


class ArticleDetailView(DetailView):
    template_name = 'article_detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['total_rate'] = self.object.rates.aggregate(Sum("rate"))['rate__sum']
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article_create.html'
    form_class = ArticleForm
    model = Article

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'article_update.html'
    form_class = ArticleForm
    model = Article

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:article_list')

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class CommentCreateView(LoginRequiredMixin, CreateView):
    template_name = 'partial/comment_form.html'
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        form.instance.article = article
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'comment_update.html'
    form_class = CommentForm
    model = Comment

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class CommentListView(ListView):
    template_name = 'comment_list.html'
    model = Comment


class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'comment_delete.html'
    model = Comment
    success_url = reverse_lazy('webapp:article_list')

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class UserDetailView(DetailView):
    template_name = 'user_details.html'
    model = User


class UserUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    model = User
    template_name = 'user_update.html'
    form_class = UserForm

    def get_success_url(self):
        return reverse('webapp:user_details', kwargs={'pk': self.object.pk})

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if user != self.request.user:
            return HttpResponseRedirect(reverse('webapp:user_details', kwargs={'pk': pk}))
        return super().get(request, pk=pk)

    def get_permission_required(self):
        return None

    def has_permission(self):
        return self.request.user == self.get_object().author


class ArticleRateView(UpdateView, LoginRequiredMixin):

    def get(self, request, pk):
        return HttpResponseRedirect(reverse('webapp:article_detail', kwargs={'pk': pk}))

    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        rate, _ = Rate.objects.update_or_create(article=article, user=self.request.user)
        if request.POST.get('value') == "+1":
            rate.rate = 1
        else:
            rate.rate = -1

        rate.save()
        data = {'total': article.rates.aggregate(Sum("rate"))['rate__sum']}
        return HttpResponse(content=json.dumps(data), content_type="application/json", status=201)
