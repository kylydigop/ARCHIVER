from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone

from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings

from django.contrib import messages
import os

from django.core.paginator import Paginator
import mimetypes

from .form import searchForm, uploadThesisForm

from taggit.models import Tag

from .models import Thesis


# Create your views here.

@method_decorator(login_required, name='dispatch')
class homePage(ListView):
    model = Thesis
    paginate_by = 2
    queryset = Thesis.objects.all()
    
    form_class = searchForm

    def get(self, request, *args, **kwargs):

        thesis = Thesis.objects.all()
        tags = Tag.objects.all()

        context = {
            'form' : self.form_class,
            'thesis' : thesis,
            'tags' : tags,
        }

        return render(request, template_name='home.html', context=context)

    def post(self, request, *args, **kwargs):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            form_field = request.POST
            print(form_field)
            if 'tags' in form_field.keys():
                thesis_query = Thesis.objects.filter(title__icontains=form_field['thesis'], tags__name=form_field['tags']) 
            else:
                thesis_query = Thesis.objects.filter(title__icontains=form_field['thesis']) 
            

            if len(thesis_query) > 0 and len(form_field) > 0:
                data = []
                for pos in thesis_query:
                    item = {
                        'id' : pos.id,
                        'title' : pos.title,
                        'abstract' : pos.abstract,
                        'authors' : [res.as_dict() for res in pos.authors.all()],
                        'tags' : [str(res) for res in pos.tags.all()],
                        'slug' : pos.slug,
                        'whenpublished' : pos.whenpublished(),
                    }
                    data.append(item)
                res = data
            else:
                res = 'No result found.'
            return JsonResponse({'data' : res}, status=200)
        return JsonResponse({}, status=400)

@method_decorator(login_required, name='dispatch')
class searchContextPage(ListView):
    model = Thesis

    def get_queryset(self):
        return Thesis.objects.all()

    def get(self, request, *args, **kwargs):
        context={}
        return render(request, template_name='home.html', context=context)



@method_decorator(login_required, name='dispatch')
class uploadPage(DetailView):

    tag_list = []

    list_of_elements_in_tags = [
        'Artificial Intelligence',
        'Deep Learning',
        'Environment',
        'Education',
        'Machine Learning',
        'Medical Technology',
        'Agriculture'
    ]

    form = uploadThesisForm

    def get(self, request, *args, **kwargs):
        context={
            'form' : self.form,
        }
        return render(request, template_name='upload.html', context=context)

    def post(self,request,*args, **kwargs):
        form = uploadThesisForm(request.POST, request.FILES)
        
        if form.is_valid():            
            instance = form.save(commit=False)
            instance.uploader = request.user
            instance.save()
            authors = form.cleaned_data['authors']
            tags = form.cleaned_data['tags']          
            print(tags)
            for author in authors:
                instance.authors.add(author)            

            instance.tags.clear()

            chars_to_remove = [',',':','[','{',']','}','value']

            temp_tags = ' '.join(tags)
            print(temp_tags)

            for i in chars_to_remove:
                temp_tags = temp_tags.replace(i, '')
            
            tags = temp_tags.split()

            for value in tags:
                print(value)
                instance.tags.add(value)
                    
            
            try: 
                instance.save()
                messages.success(request, "Document has been uploaded")
                return redirect('/search/home')
            except:
                messages.error(request, "Failed to upload document. Please try again.")
                return redirect('/search/upload')
            
        else:
            form = uploadThesisForm()
            print('Failed')
 
        context = {
            'form' : self.form,
            'messages' : messages,
        }
        return render(request, template_name='upload.html', context=context)

@method_decorator(login_required, name='dispatch')
class abstractPage(DetailView):

    def get(self, request, slug, *args, **kwargs):

        obj = Thesis.objects.filter(slug=slug).first()

        context = {
            'thesis' : obj,
        }
        return render(request, template_name='abstract.html', context=context)
        

    def post(self, request, *args, **kwargs):
        context = {}
        return render(request, template_name='abstract.html', context=context)

@method_decorator(login_required, name='dispatch')
class DownloadFile(DetailView):
    def get(self,request,slug,*args,**kwargs):
        file = Thesis.objects.get(slug=slug)
        filename = file.document.name
        print(filename)
        file_dir = os.path.join(settings.MEDIA_ROOT, f'{filename}')
        print(file_dir)
        if os.path.exists(file_dir):
            print('File Exists')
            with open(file_dir, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_dir)
                return response
        else:
            return HttpResponseNotFound('Error')

class removeThesis(View):
    def get(self, request,id,*args,**kwargs):
        obj = Thesis.objects.get(id=id)
        obj.delete()
        return redirect('search')

@method_decorator(login_required, name='dispatch')
class aboutPage(View):
    def get(self, request, *args, **kwargs):

        context = {

        }
        return render(request, template_name='about.html', context=context)

        

        


        

