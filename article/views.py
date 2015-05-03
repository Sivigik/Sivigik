#This file is part of Sivigik.
#
#Foobar is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Foobar is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.gzip import gzip_page

from django.views import generic
from django.forms.formsets import formset_factory

from article.models import Article, Part
from home.models import Event

from article.forms import EditArticleForm, EditPartForm

from django.utils import timezone

#import markdown

@gzip_page
def view_article(request, pk):
    a = get_object_or_404(Article, pk=pk)
    d = {'article' : a,
         'current' : a.event.category.pk}
    return render(request, 'article/detail.html', d)
def view_comments(request, pk):
    a = get_object_or_404(Article, pk=pk)
    d = {'article' : a,
         'current' : a.event.category.pk}
    return render(request, 'article/comments.html', d)
@login_required(login_url='/member/login/')
def edit_article(request, article_id=0):
    if request.method == 'POST':
        form = EditArticleForm(request.POST, request.FILES)
        formset=formset_factory( EditPartForm )( request.POST )

        if form.is_valid():

            author = request.user.member
            date = timezone.now()
            title = form.cleaned_data['title']
            is_beta = form.cleaned_data['is_beta']
            category = form.cleaned_data['category']
            image = form.cleaned_data['image']
            is_pinned = form.cleaned_data['is_pinned']
            introduction = form.cleaned_data['introduction']

            if article_id == 0:
            	e = Event(name=title, pub_date=date, category=category, image=image, is_pinned=is_pinned)
                e.save()
            	a = Article(event=e, author=author, is_beta=is_beta, introduction=introduction)
                a.save()
                if formset.is_valid():
                    for p in formset:
                        text = p.cleaned_data['text']
                        title= p.cleaned_data['title']
                        part=Part(text=text, title=title, article=a)
                        part.save()
                idx = a.pk
            else:
            	a = get_object_or_404(Article, pk=article_id)
            	if image is None:
            		image = a.event.image
            	e = a.event
                a.introduction = introduction
            	a.is_beta = is_beta
                e.is_pinned =  is_pinned
            	e.name = title
            	e.pub_date = date
            	e.category = category
            	e.image = image
            	a.event = e

                if formset.is_valid():
                    for p in a.parts.all():
                        p.delete()
                    for p in formset:
                        a.parts.create(title=p.cleaned_data['title'], text=p.cleaned_data['text'])

                e.save()
                a.save()

            return HttpResponseRedirect(a.get_absolute_url())
    else:
    	if article_id == 0:
            form = EditArticleForm()
            parts = formset_factory(EditPartForm, extra=1)()
        else:
            a = get_object_or_404(Article, pk=article_id)
            p_list = []
            no_parts = True
            for i in a.parts.all():
                p_list.append({'title': i.title,'text':i.text})
                no_parts = False
            if no_parts:
                parts = formset_factory(EditPartForm, extra=0)(initial=p_list)
            else:
                parts = formset_factory(EditPartForm, extra=0)(initial=p_list)
            form = EditArticleForm(initial={'title':a.event.name,
    										'image':a.event.image,
    										'category':a.event.category,
    										'is_beta':a.is_beta,
                                            'introduction':a.introduction,})
    if article_id == 0:
    	send_to = '/article/new/'
    else :
    	send_to = '/article/' + article_id + '/edit/'
    
    return render(request, 'article/edit.html', locals())
