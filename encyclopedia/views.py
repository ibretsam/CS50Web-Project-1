from curses.ascii import HT
from random import random
from tkinter import W
from turtle import title
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import markdown
from django import forms
from django.forms import MultiWidget, TextInput, Textarea
from . import util
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': "form-control", 'style': "width: 90%;"}))
    content = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={'class': "form-control", 'style': "width: 90%;"}))

class EditEntryForm(forms.Form):
    content = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={'class': "form-control", 'style': "width: 90%;"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content == None:
        entry_content = ("##404 Error <br> Page was not found")
    entry_content = markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {'content': entry_content, 'title': title})

def search(request):
    searched_query = request.GET['searched']
    if searched_query in util.list_entries():
        return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': searched_query}))
    else:
        substring_entries = []
        for entry in util.list_entries():
            if searched_query.lower() in entry.lower():
                substring_entries.append(entry)
    return render(request, "encyclopedia/search.html", {'entries': substring_entries, 'searched_query': searched_query, 'title': "Search"})
    
def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': title}))
            else:
                return render(request, "encyclopedia/error.html", {
                    "error_message": "Error: Entry title duplicated"
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm(),
        "title": "Create a new page"
    })

def edit(request, title):
    if request.method == "GET":
        page_content = util.get_entry(title)
        if page_content == None:
            title == ("Page was not found")
        return render(request, "encyclopedia/edit.html", {
            'title': title,
            'edit_form': EditEntryForm(initial={'content': page_content})
        })
    elif request.method == "POST":
        edit_form = EditEntryForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data["content"]
            util.save_entry(title, content)
        else:
            return(request, "encyclopedia/edit.html", {
                "edit_form": forms
            })
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': title}))


def random_page(request):
    title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("wiki:entry", kwargs={'title': title}))