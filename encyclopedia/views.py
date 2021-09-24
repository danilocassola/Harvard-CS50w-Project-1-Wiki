from django.shortcuts import render
from . import util
from markdown2 import Markdown
from django.urls import reverse
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from random import choice
import string

class NewTitleForm(forms.Form):
    title = forms.CharField(label="New Title", max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="Content", widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def title(request, name):
    file = util.get_entry(name)
    markdowner = Markdown()

    if file is None:
        return render(request, "encyclopedia/error.html")

    else:
        return render(request, "encyclopedia/title.html", {
            "title": name,
            "file": markdowner.convert(file)
        })


def newpage(request):

    if request.method == "POST":
        form = NewTitleForm(request.POST)
        file = util.get_entry(request.POST["title"])
        if file is None:
            util.save_entry(request.POST["title"], request.POST["content"])
            return HttpResponseRedirect(reverse("title", args=(request.POST["title"],)))

        else:
            messages.add_message(request, messages.ERROR, 'ERROR: Encyclopedia entry already exists with the provided title.')
            return render(request, "encyclopedia/new.html", {
                #"form": NewTitleForm()
                #"title": title,
                "form": NewTitleForm(initial={'content': request.POST["content"], 'title': request.POST["title"]})
            })
    else:
        form = NewTitleForm(request.POST)
        return render(request, "encyclopedia/new.html", {
            "form": NewTitleForm()
        })


def edit(request):
        title = request.POST["name"]
        file = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": NewTitleForm(initial={'content': file})
        })


def update(request):
        util.save_entry(request.POST["name"], request.POST["content"])
        return HttpResponseRedirect(reverse("title", args=(request.POST["name"],)))


def randompage(request):
    page = choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=(page,)))


def search(request):
    file = request.GET.get("q","")
    if util.get_entry(file) is not None:
        return HttpResponseRedirect(reverse("title", args=(file,)))
    else:
        search_string = []
        for entry in util.list_entries():
            if file.upper() in entry.upper():
                search_string.append(entry)

        return render(request, "encyclopedia/index.html", {
            "entries": search_string,
            "search": True
        })