import io

from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from outwards.forms import NewCaseForm, UpdateForm
from outwards.models import Outward, Update, Case


def outwards(request):
    outwards = Outward.objects.all()
    return render(request, 'outwards.html', {'outwards': outwards})


def outward_cases(request, pk):
    outward = get_object_or_404(Outward, pk=pk)
    cases = outward.cases.order_by('-last_updated').annotate(replies=Count('updates') - 1)
    return render(request, 'cases.html', {'outward': outward, 'cases': cases})


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
    outwards = outward = get_object_or_404(Outward, pk=pk)
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