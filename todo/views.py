# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from todo.models import List, Item
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms
import datetime

PRIORITY_CHOICES = (
	(1, 'Low'),
	(2, 'Normal'),
	(3, 'High'),
)

class completeForm(forms.Form):
	item_complete = forms.BooleanField(required=False)

class newListForm(forms.Form):
	todo_name = forms.CharField(max_length=250, label='Create a new list', required=True, widget=forms.TextInput(attrs={'placeholder': 'New list name'}))

class newItemForm(forms.Form):
	todo_name = forms.CharField(max_length=250, label='Create a new item', required=True, widget=forms.TextInput(attrs={'placeholder': 'New item name'}))
	priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=True)

def status_report(request):

	if request.method == 'POST':
		form = newListForm(request.POST)
		if form.is_valid():
			l = List(title=form.cleaned_data['todo_name'])
			l.save()
			return HttpResponseRedirect('/')		# Redirect after POST

	# Below code is executed if form was not submitted OR if the form was invalid
	form = newListForm()
	todo_listing = []
	for todo_list in List.objects.all():
		todo_dict = {}
		todo_dict['list_object'] = todo_list
		todo_dict['item_count'] = todo_list.item_set.count()
		todo_dict['items_complete'] = todo_list.item_set.filter(completed=True).count()
		if todo_dict['item_count'] != 0:
			todo_dict['percent_complete'] = int(float(todo_dict['items_complete']) / todo_dict['item_count'] * 100)
		else:
			todo_dict['percent_complete'] = 0
		todo_listing.append(todo_dict)

	return render(request, 'status_report.html', {'todo_listing': todo_listing, 'newList_form': form})

def list_detail(request, list_id):
	
	if request.method == 'POST':
		form = newItemForm(request.POST)
		if form.is_valid():
			i = Item(
				title = form.cleaned_data['todo_name'],
				created_date = datetime.datetime.now(),
				priority = form.cleaned_data['priority'],
				completed = False,
				todo_list = List.objects.get(pk=list_id)
			)
			i.save()
			return HttpResponseRedirect('/list/%s' % list_id)		# Redirect after POST

	# Below code is executed if form was not submitted OR if the form was invalid
	return render(request, 'list_detail.html', {'todo_list': List.objects.get(pk=list_id), 'newItem_form': newItemForm()})


def item_detail(request, item_id):
	i = get_object_or_404(Item, pk=item_id)

	if request.method == 'POST':
		form = completeForm(request.POST)
		if form.is_valid():
			i.completed = form.cleaned_data['item_complete']
			i.save()
			return HttpResponseRedirect('/list/%d' % i.todo_list.id )

	# Below code is executed if form was not submitted OR if the submitted form was invalid
	form = completeForm(initial={'item_complete': i.completed})
	return render(request, 'item_detail.html', {'todo_item': i, 'complete_form': form })

	#	return HttpResponse('You are looking at to-do item %s' % item_id)

def list_delete(request, list_id):
	if request.method == 'POST':
		l = List.objects.get(pk=list_id)
		for item in l.item_set.all():
			item.delete()	

		l.delete()
		return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/list/%s' % list_id)

def item_delete(request, item_id):
	if request.method == 'POST':
		i = Item.objects.get(pk=item_id)
		i.delete()

	return HttpResponseRedirect('/list/%s' % i.todo_list.id )
