# -*- encoding: utf-8 -*-

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect

from guardian.decorators import permission_required

from apps.dashboard.tools import has_access, get_base_context
from apps.feedback.models import Feedback, TextQuestion, RatingQuestion, MultipleChoiceRelation
from apps.feedback.dashboard.forms import FeedbackForm, TextQuestionForm
from apps.feedback.dashboard.forms import RatingQuestionForm, MultipleChoiceQuestionForm


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
@permission_required('feedback.add_feedback', return_403=True)
def new(request):

    if not has_access(request):
        raise PermissionDenied

    # Get base context
    context = get_base_context(request)

    feedback = Feedback.objects.create(author=request.user)

    return redirect(details, feedback_pk=feedback.feedback_id)


@login_required
@permission_required('feedback.view_item', return_403=True)
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
    context['mcquestions'] = [(mcquestion.id, MultipleChoiceQuestionForm(instance=mcquestion)) for mcquestion in mcquestions]

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
    context['mcquestion_form'] = MultipleChoiceQuestionForm()

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

        return redirect(details, feedback_pk=feedback.feedback_id)

    raise PermissionDenied

@login_required
@permission_required('feedback.edit_question', return_403=True)
def edit_textquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    # Get base context

    feedback = get_object_or_404(Feedback, pk=feedback_pk)
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

    # Get base context

    if request.method == 'POST':
        textquestion = get_object_or_404(TextQuestion, pk=question_pk)
        #TODO check for dependencies
        textquestion.delete()
        return redirect(details, feedback_pk=feedback_pk)        

    raise PermissionDenied


@login_required
@permission_required('feedback.add_question', return_403=True)
def new_ratingquestion(request, feedback_pk):
    if not has_access(request):
        raise PermissionDenied

    # Get base context

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

        return redirect(details, feedback_pk=feedback.feedback_id)

    raise PermissionDenied

@login_required
@permission_required('feedback.edit_question', return_403=True)
def edit_ratingquestion(request, feedback_pk, question_pk):
    if not has_access(request):
        raise PermissionDenied

    # Get base context

    feedback = get_object_or_404(Feedback, pk=feedback_pk)
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

    # Get base context

    if request.method == 'POST':
        ratingquestion = get_object_or_404(RatingQuestion, pk=question_pk)
        #TODO check for dependencies
        ratingquestion.delete()
        return redirect(details, feedback_pk=feedback_pk)        

    raise PermissionDenied


@login_required
@permission_required('feedback.add_question', return_403=True)
def new_mcquestion(request, feedback_pk):
    if not has_access(request):
        raise PermissionDenied

    # Get base context

    feedback = get_object_or_404(Feedback, pk=feedback_pk)

    if request.method == 'POST':
        mcquestion_form = MultipleChoiceQuestionForm(request.POST)

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

    # Get base context

    feedback = get_object_or_404(Feedback, pk=feedback_pk)
    mcquestion = get_object_or_404(MultipleChoiceRelation, pk=question_pk)

    if request.method == 'POST':
        mcquestion_form = MultipleChoiceQuestionForm(request.POST, instance=mcquestion)

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

    # Get base context

    if request.method == 'POST':
        mcquestion = get_object_or_404(MultipleChoiceRelation, pk=question_pk)
        #TODO check for dependencies
        mcquestion.delete()
        return redirect(details, feedback_pk=feedback_pk)        

    raise PermissionDenied