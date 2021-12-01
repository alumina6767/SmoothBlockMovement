from django.shortcuts import render
#from django.http import HttpResponse
#from .forms import UploadFileForm

# Imaginary function to handle an uploaded file
#from somewhere import handle_uploaded_file

#def handle_uploaded_file(f):
#    with open('tmp/file/test.txt', 'wb+') as destination:
#        for chunk in f.chunks():
#            destination.write(chunk)
from .convert import convert

def index(request):
    context = ""
    if request.method == 'POST' and request.FILES and ".schem" in request.FILES['txt'].name:
        context = request.FILES['txt']
        add_tag = request.POST['add_tag']
        mode = request.POST['mode']
        # context = context.read()
        context = convert(context, add_tag, mode)
        # form = UaploadFileForm(request.POST, request.FILES)
        # if form.is_valid():
            #handle_uploaded_file(request.FILES['file'])
            #form = request.FILES['file'].read()
            # form = "aaa"
   # else:
        # form = UploadFileForm()
    return render(request, 'sbm/index.html', {'form': context})
# Create your views here.
#def index(request):
#    return render(request, 'five/index.html', {})
    #return HttpResponse('<h1>Hello, myapp!</h1>')
