from msilib.schema import ListView
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
# Create your views here.


class OrderListView(ListView):
    pass


class OerderCreateView(CreateView):
    pass


class OrderUpdateView(UpdateView):
    pass


class OrderReadView(DetailView):
    pass


class OrderDeleteView(DeleteView):
    pass


def forming_complete(request, pk):
    pass
