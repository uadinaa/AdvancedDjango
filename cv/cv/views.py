from .models import Profile, CV
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
from .forms import ProfileForm
from .forms import ContactForm
from django.shortcuts import render, redirect
from .forms import CVForm


def accept(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ProfileForm()
    return render(request, 'pdf/accept.html', {'form': form})


def accept(request):
    if request.method == "POST":
        name = request.POST.get("name", "")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        summary = request.POST.get("summary", "")
        degree = request.POST.get("degree", "")
        school = request.POST.get("school", "")
        university = request.POST.get("university", "")
        previous_work = request.POST.get("previous_work", "")
        skills = request.POST.get("skills", "")


        employed = request.POST.get("employed", "")
        if employed == 'on':
            employed = True
        else:
            employed = False

        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            degree=degree,
            school=school,
            university=university,
            previous_work=previous_work,
            skills=skills,
            employed=employed
        )
        profile.save()

    return render(request, 'pdf/accept.html')


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return render(request, 'success.html', {'name': name})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})



def resume(request,id):
    user_profile = Profile.objects.get(pk=id)
    return render(request, 'pdf/resume.html', {'user_profile': user_profile})


def resume(request,id):
        user_profile = Profile.objects.get(pk=id)
        template = loader.get_template('pdf/resume.html')
        html = template.render({'user_profile':user_profile})
        options ={
                'page-size':'Letter',
                'encoding':"UTF-8",
        }
        pdf = pdfkit.from_string(html,False,options)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] ='attachment'
        filename = "resume.pdf"
        return response


def list(request):
        profiles = Profile.objects.all()
        return render(request,'pdf/list.html',{'profiles':profiles})


def create_cv(request):
    if request.method == "POST":
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cv_list')
    else:
        form = CVForm()
    return render(request, 'cv_form.html', {'form': form})


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect


def share_cv_email(request, cv_id):
    cv = get_object_or_404(CV, id=cv_id)
    recipient_email = request.POST.get('email')

    if recipient_email:
        send_mail(f"{cv.name}'s CV",
                  f"Check out {cv.name}'s CV at {request.build_absolute_uri(cv.profile_picture.url)}",
                  settings.EMAIL_HOST_USER, [recipient_email])
    return redirect('cv_list')

