from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Note
from .forms import NoteForm

@login_required
def home(request):
  notes = Note.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'notes/home.html', {'notes': notes})

@login_required
def add_note(request):
  if request.method == 'POST':
   form = NoteForm(request.POST)
   if form.is_valid():
    note = form.save(commit=False)
    note.user = request.user
    note.save()
    return redirect('home')
  else:
      form = NoteForm()
  return render(request, 'notes/add_note.html', {'form': form})

@login_required
def edit_note(request, pk):
  note = get_object_or_404(Note, pk=pk, user=request.user)
  if request.method == 'POST':
   form = NoteForm(request.POST, instance=note)
   if form.is_valid():
    form.save()
    return redirect('home')
  else:
      form = NoteForm(instance=note)
  return render(request, 'notes/edit_note.html', {'form': form})
  
@login_required
def delete_note(request, pk):
  note = get_object_or_404(Note, pk=pk, user=request.user)
  if request.method == 'POST':
    note.delete()
    return redirect('home')
  return render(request, 'notes/delete_note.html', {'note': note})

def register(request):
  if request.method == 'POST':
   form = UserCreationForm(request.POST)
   if form.is_valid():
    user = form.save()
    login(request, user)
   return redirect('home')
  else:
      form = UserCreationForm()
  return render(request, 'notes/register.html', {'form': form})

