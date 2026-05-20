import markdown2

from django.shortcuts import render, redirect

from . import util

import random

from django import forms

entries = util.list_entries()

class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title of Entry'}))
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Markdown content',
            'rows': 5,
            'cols': 40
            })
    )

def convert(title):
    entry = util.get_entry(title)
    if entry == None:
        return None
    else:
        markdowner = markdown2.Markdown()
        return markdowner.convert(entry)
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def file(request, title):
    html = convert(title)
    if html == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/pages.html", {
            "entry": html,
            "title": title
        })
    
def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()
    for entry in entries:
        if entry.lower() == query.lower():
            return redirect("file", title=entry)
        
    results = [entry for entry in entries if query.lower() in entry.lower()]
        
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].strip()
            content = form.cleaned_data["content"].strip()
            entries = util.list_entries()
            if title.lower() in [entry.lower() for entry in entries]:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "error": f"An entry with the title '{title}' already exists."
                })
            util.save_entry(title, content)
            return redirect("file", title=title)
        return render(request, "encyclopedia/create.html", {
            "form": form
        })
    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

def edit(request, title):
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return redirect("file", title=title)
    
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html")
    

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": content
    })

def random_page(request):
    files = util.list_entries()

    if files:
        random_file = random.choice(files)
        return redirect("file", title=random_file)
    
    