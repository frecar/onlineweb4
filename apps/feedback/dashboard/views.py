# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from guardian.decorators import permission_required

from apps.dashboard.tools import has_access, get_base_context
from apps.feedback.models import Feedback, TextQuestion, RatingQuestion, Choice
from apps.feedback.models import MultipleChoiceRelation, MultipleChoiceQuestion
from apps.feedback.dashboard.forms import FeedbackForm, TextQuestionForm, MultipleChoiceQuestionForm
from apps.feedback.dashboard.forms import RatingQuestionForm, MultipleChoiceRelationForm, ChoiceForm


@login_required
@permission_required('feedback.view_item', return_403=True)
def index(request):

    # Generic check to see if user has access to dashboard. (In Komiteer or superuser)
    if not has_access(request):
        raise PermissionDenied

    # Create the base context needed for the sidebar
    context = get_base_context(request)

    context['feedbacks'] = Feedback.objects.all()

    return render(request, 'feedback/dashboard/feedbackschemas.html', context)

@login_required
@permission_required('feedback.add', return_403=True)
def new(request):

    if not has_access(request):
        raise PermissionDenied

    feedback = Feedback.objects.create(author=request.user)

    return redirect(details, feedback_pk=feedback.feedback_id)

@login_required
@permission_required('feedback.delete', return_403=True)
def delete(request, feedback_pk):

    if not has_access(request):
        raise PermissionDenied

    feedback = get_object_or_404(Feedback, pk=feedback_pk)

    if feedback.feedbackrelation_set.all():
        messages.error(request, "Dette skjemaet har vært i bruk og kan ikke slettes.")
        return redirect(details, feedback_pk=feedback_pk)
    else:
        feedback.delete()
        messages.success(request, "Skjemaet har blitt slettet.")
        return redirect(index)


@login_required
@permission_required('feedback.view', return_403=True)
def details(request, feedback_pk):
    # Generic check to see if user has access to dashboard. (In Komiteer or superuser)
    if not has_access(request):
        raise PermissionDenied

    # Create the base context needed for the sidebar
    context = get_base_context(request)

    context['feedback'] = get_object_or_404(Feedback, pk=feedback_pk)

    textquestions =  TextQuestion.objects.filter(feedback=context['feedback'])
    context['textquestions'] = [(textquestion.id, TextQuestionForm(instance=textquestion)) for textquestion in textquestions]

    ratingquestions =  RatingQuestion.objects.filter(feedback=context['feedback'])
    context['ratingquestions'] = [(ratingquestion.id, RatingQuestionForm(instance=ratingquestion)) for ratingquestion in ratingquestions]

    mcquestions =  MultipleChoiceRelation.objects.filter(feedback=context['feedback'])
    context['mcquestions'] = [(mcquestion.id, MultipleChoiceRelationForm(instance=mcquestion)) for mcquestion in mcquestions]

    if request.method == 'POST':
        # if 'feedback.change_item' not in context['user_permissions']:
        #     raise PermissionDenied

        feedback_form = FeedbackForm(request.POST, instance=context['feedback'])
        print request.POST
        if not feedback_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            feedback_form.save()
            messages.success(request, u'Tilbakemeldingsskjemaet ble oppdatert')
        context['feedback_form'] = feedback_form
    else:
        context['feedback_form'] = FeedbackForm(instance=context['feedback'])

    context['textquestion_form'] = TextQuestionForm()
    context['ratingquestion_form'] = RatingQuestionForm()
    context['mcquestion_form'] = MultipleChoiceRelationForm()

    return render(request, 'feedback/dashboard/details.html', context)



@login_required
@permission_required('feedback.add_question', return_403=True)
def new_textquestion(request, feedback_pk):
    if not has_access(request):
        raise PermissionDenied

    # Get base context

    feedback = get_object_or_404(Feedback, pk=feedback_pk)

    if request.method == 'POST':
        textquestion_form = TextQuestionForm(request.POST)

        if not textquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            textquestion = textquestion_form.save(commit=False)
            textquestion.feedback = feedback
            textquestion.save()
            messages.success(request, u'Spørsmålet ble lagt til.')

        return redirect(details, feedback_pk=feedback_pk)

    raise PermissionDenied

@login_required
@permission_required('feedback.edit_question', return_403=True)
def edit_textquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    textquestion = get_object_or_404(TextQuestion, pk=question_pk)

    if request.method == 'POST':
        textquestion_form = TextQuestionForm(request.POST, instance=textquestion)

        if not textquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            textquestion.save()
            messages.success(request, u'Spørsmålet ble endret.')

        return redirect(details, feedback_pk=feedback_pk)

    raise PermissionDenied


@login_required
@permission_required('feedback.delete_question', return_403=True)
def delete_textquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    textquestion = get_object_or_404(TextQuestion, pk=question_pk)

    if textquestion.answer.all():
        messages.error(request, u'Spørsmålet har svar og kan ikke slettes.')
    else:
        textquestion.delete()
        messages.success(request, u'Spørsmålet har blitt slettet.')
    return redirect(details, feedback_pk=feedback_pk)        


@login_required
@permission_required('feedback.add_question', return_403=True)
def new_ratingquestion(request, feedback_pk):
    if not has_access(request):
        raise PermissionDenied

    feedback = get_object_or_404(Feedback, pk=feedback_pk)

    if request.method == 'POST':
        ratingquestion_form = RatingQuestionForm(request.POST)

        if not ratingquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            ratingquestion = ratingquestion_form.save(commit=False)
            ratingquestion.feedback = feedback
            ratingquestion.save()
            messages.success(request, u'Spørsmålet ble lagt til.')

        return redirect(details, feedback_pk=feedback_pk)

    raise PermissionDenied

@login_required
@permission_required('feedback.edit_question', return_403=True)
def edit_ratingquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    ratingquestion = get_object_or_404(RatingQuestion, pk=question_pk)

    if request.method == 'POST':
        ratingquestion_form = RatingQuestionForm(request.POST, instance=ratingquestion)

        if not ratingquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            ratingquestion.save()
            messages.success(request, u'Spørsmålet ble endret.')

        return redirect(details, feedback_pk=feedback_pk)

    raise PermissionDenied


@login_required
@permission_required('feedback.delete_question', return_403=True)
def delete_ratingquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    ratingquestion = get_object_or_404(RatingQuestion, pk=question_pk)

    if ratingquestion.answer.all():
        messages.error(request, u'Spørsmålet har svar og kan ikke slettes.')
    else:
        ratingquestion.delete()
        messages.success(request, u'Spørsmålet har blitt slettet.')
    return redirect(details, feedback_pk=feedback_pk)      


@login_required
@permission_required('feedback.add_question', return_403=True)
def new_mcquestion(request, feedback_pk):
    if not has_access(request):
        raise PermissionDenied

    feedback = get_object_or_404(Feedback, pk=feedback_pk)

    if request.method == 'POST':
        mcquestion_form = MultipleChoiceRelationForm(request.POST)

        if not mcquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            mcquestion = mcquestion_form.save(commit=False)
            mcquestion.feedback = feedback           
            mcquestion.save()
            messages.success(request, u'Spørsmålet ble lagt til.')

        return redirect(details, feedback_pk=feedback.feedback_id)

    raise PermissionDenied

@login_required
@permission_required('feedback.edit_question', return_403=True)
def edit_mcquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    mcquestion = get_object_or_404(MultipleChoiceRelation, pk=question_pk)

    if mcquestion.answer.all():
        messages.error(request, u'Dette spørsmålet har svar og kan ikke redigeres.')
        return redirect(details, feedback_pk=feedback_pk)

    if request.method == 'POST':
        mcquestion_form = MultipleChoiceRelationForm(request.POST, instance=mcquestion)

        if not mcquestion_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            mcquestion.save()
            messages.success(request, u'Spørsmålet ble endret.')

        return redirect(details, feedback_pk=feedback_pk)

    raise PermissionDenied

@login_required
@permission_required('feedback.delete_question', return_403=True)
def delete_mcquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    mcquestion = get_object_or_404(MultipleChoiceRelation, pk=question_pk)     

    if mcquestion.answer.all():
        messages.error(request, u'Spørsmålet har svar og kan ikke slettes.')
    else:
        mcquestion.delete()
        messages.success(request, u'Spørsmålet har blitt slettet.')

    return redirect(details, feedback_pk=feedback_pk)   



# Multiple MultipleChoice

@login_required
@permission_required('feedback.multiplechoice', return_403=True)
def multiplechoice_index(request):
    if not has_access(request):
        raise PermissionDenied

    # Create the base context needed for the sidebar
    context = get_base_context(request)

    context['multiple_choices'] = MultipleChoiceQuestion.objects.all()

    if request.method == 'POST':
        multiple_choices_form = MultipleChoiceQuestionForm(request.POST)

        if not multiple_choices_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            multiple_choices_form.save()
            messages.success(request, u'Spørsmålet ble opprettet')
            return redirect(multiplechoice_index)

        context['form'] = multiple_choices_form

    else:
        context['form'] = MultipleChoiceQuestionForm()

    return render(request, 'feedback/dashboard/multiplechoice_index.html', context)


@login_required
@permission_required('feedback.multiplechoice', return_403=True)
def multiplechoice_details(request, multiple_choice_pk):

    if not has_access(request):
        raise PermissionDenied

    # Get base context
    context = get_base_context(request)

    context['multiple_choice'] = MultipleChoiceQuestion.objects.get(pk=multiple_choice_pk)

    choices =  Choice.objects.filter(question=context['multiple_choice'])
    context['choice_forms'] = [(choice.id, ChoiceForm(instance=choice)) for choice in choices]

    if request.method == 'POST':
        inventory_form = ItemForm(request.POST)

        if not inventory_form.is_valid():
            messages.error(request, u'Noen av de påkrevde feltene inneholder feil.')
        else:
            inventory_form.save()
            messages.success(request, u'Varen ble opprettet')
            return redirect(index)

        context['form'] = inventory_form

    else:
        context['form'] = ItemForm()

    return render(request, 'inventory/dashboard/new.html', context)