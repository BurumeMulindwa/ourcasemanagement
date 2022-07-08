import self
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Avg
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django_countries.fields import Country

from boards import models
from outwards.forms import NewCaseForm, UpdateForm
from outwards.models import Outward, Update, Case
from .forms import NewTopicForm, PostForm
from .models import Board, Post, Topic

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.mail import send_mail


def home(request):
    return render(request, 'home.html', {})


def landing(request):
    return render(request, 'landing.html', {})


def statistics(request):
    return render(request, 'statistics.html', {})


def boards_statistics(request):
    count = Board.objects.all().count()
    context = {'count': count}
    return render(request, 'boards_statistics.html', context)


def boards_statistics_countries(request):
    countries_cases = Board.objects.values('country').annotate(number=Count('pk')).order_by('country')
    countries_cases = {
        'countries_cases': ",".join(map(str, countries_cases))
    }
    context = {'countries_cases': countries_cases}
    return render(request, 'boards_statistics_countries.html', context)


def boards_statistics_instrument(request):
    instrument_cases = Board.objects.values('instrument').annotate(number=Count('pk')).order_by('instrument')
    instrument_cases = {
        'instrument_cases': ",".join(map(str, instrument_cases))
    }
    context = {'instrument_cases': instrument_cases}
    return render(request, 'boards_statistics_instrument.html', context)


def boards(request):
    # Set up Pagination
    p = Paginator(Board.objects.all().order_by('-id'), 10)
    page = request.GET.get('page')
    boards = p.get_page(page)
    nums = "a" * boards.paginator.num_pages

    context = {'boards': Board.objects.filter(employee=request.user), 'nums': nums}

    return render(request, 'boards.html', context)


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('last_updated')

    return render(request, 'topics.html', {'board': board, 'topics': topics})


def topic_history(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated')
    total = Topic.objects.all().aggregate(Sum('case_age'))
    return render(request, 'topic_history.html', {'board': board, 'topics': topics, 'total': total})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                notes=form.cleaned_data.get('notes'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


def topic_alerts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    topic.save()
    return render(request, 'topic_alerts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


def board_pdf(request, pk, topic_pk):
    # Create a ByteStream buffer:
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    # lines = [
    #    "This is line 1",
    #    "This is line 2",
    #    "This is line 3",
    # ]

    # Designate The Model
    board = get_object_or_404(Board, pk=pk)
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)

    # Create blank list:
    lines = [topic.board.reference, topic.progress, topic.requesting_party_reference_number,
             topic.point_of_contact_surname, " "]

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='board.pdf')


'''
def board_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    p.drawString(100, 100, "Hello Dear")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='board.pdf')
'''


def outwards(request):
    outwards = Outward.objects.all().order_by('-id')

    # Set up Pagination
    p = Paginator(Outward.objects.all().order_by('-id'), 10)
    page = request.GET.get('page')
    outwards = p.get_page(page)
    nums = "a" * outwards.paginator.num_pages

    context = {'outwards': Outward.objects.filter(employee=request.user), 'nums': nums}

    return render(request, 'outwards.html', context)


def outwards_statistics(request):
    count = Outward.objects.all().count()
    context = {'count': count}
    return render(request, 'outwards_statistics.html', context)


def outwards_statistics_countries(request):
    countries_cases = Outward.objects.values('country').annotate(number=Count('pk')).order_by('country')
    countries_cases = {
        'countries_cases': ",".join(map(str, countries_cases))
    }
    context = {'countries_cases': countries_cases}
    return render(request, 'outwards_statistics_countries.html', context)


def outwards_statistics_instrument(request):
    instrument_cases = Outward.objects.values('instrument').annotate(number=Count('pk')).order_by('instrument')
    instrument_cases = {
        'instrument_cases': ",".join(map(str, instrument_cases))
    }
    context = {'instrument_cases': instrument_cases}
    return render(request, 'outwards_statistics_instrument.html', context)


def outward_cases(request, pk):
    outward = get_object_or_404(Outward, pk=pk)
    cases = outward.topics.order_by('-last_updated')
    return render(request, 'cases.html', {'outward': outward, 'cases': cases})


def case_history(request, pk):
    outward = get_object_or_404(Outward, pk=pk)
    cases = outward.topics.order_by('-last_updated')
    return render(request, 'case_history.html', {'outward': outward, 'cases': cases})


@login_required
def new_case(request, pk):
    outward = get_object_or_404(Outward, pk=pk)
    if request.method == 'POST':
        form = NewCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            case.outward = outward
            case.initiator = request.user
            case.save()
            Update.objects.create(
                notes=form.cleaned_data.get('notes'),
                case=case,
                author=request.user
            )
            return redirect('case_updates', pk=pk, case_pk=case.pk)
    else:
        form = NewCaseForm()
    return render(request, 'new_case.html', {'outward': outward, 'form': form})


def case_updates(request, pk, case_pk):
    case = get_object_or_404(Case, outward__pk=pk, pk=case_pk)

    case.save()
    return render(request, 'case_updates.html', {'case': case})


def case_alerts(request, pk, case_pk):
    case = get_object_or_404(Case, outward__pk=pk, pk=case_pk)

    case.save()
    return render(request, 'case_alerts.html', {'case': case})


@login_required
def reply_case(request, pk, case_pk):
    case = get_object_or_404(Case, outward__pk=pk, pk=case_pk)
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            update = form.save(commit=False)
            update.case = case
            update.author = request.user
            update.save()
            return redirect('case_updates', pk=pk, case_pk=case_pk)
    else:
        form = UpdateForm()
    return render(request, 'reply_case.html', {'case': case, 'form': form})


def outward_pdf(request, pk, case_pk):
    # Create a ByteStream buffer:
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Add some lines of text
    # lines = [
    #    "This is line 1",
    #    "This is line 2",
    #    "This is line 3",
    # ]

    # Designate The Model
    outward = get_object_or_404(Outward, pk=pk)
    case = get_object_or_404(Case, outward__pk=pk, pk=case_pk)

    # Create blank list:
    lines = [case.outward.reference, case.progress, case.requesting_party_reference_number,
             case.point_of_contact_name, " "]

    # Loop
    for line in lines:
        textob.textLine(line)

    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='outward.pdf')


def inward_form_upload(request):
    if request.method == 'POST':
        form = InwardDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = InwardDocumentForm()
        context = {
            'form': form,
        }
    return render(request, 'inward_form_upload.html', {'form': form})


def outward_form_upload(request):
    if request.method == 'POST':
        form = OutwardDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('landing')
    else:
        form = OutwardDocumentForm()
        context = {
            'form': form,
        }
    return render(request, 'outward_form_upload.html', {'form': form})
