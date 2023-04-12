from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from assessments.models import *
from django.contrib import messages
from assessments.models import *
from administration.models import *
from django.urls import reverse
from django.db.models import Q
from sophia import settings
from .result import *
from thefuzz import fuzz, process
from langdetect import detect


@staff_member_required
@login_required(login_url='login')
def dashboard(request):
	assessment = allAssessment.objects
	video = videoAns.objects.all()[:5]
	return render(request, 'dashboard.html', {'assessment': assessment, 'video': video})


@staff_member_required
@login_required(login_url='login')
def allAnswer(request):
	url = settings. MEDIA_URL
	video = videoAns.objects.all()
	return render(request, 'all_submmision.html', {'video': video, 'url': url})


@staff_member_required
@login_required(login_url='login')
def searchbar(request):
	query = request.GET.get('q')
	url = settings. MEDIA_URL
	if query:
		results = videoAns.objects.filter(
		    Q(user_name__icontains=query) | Q(assessment_name__icontains=query))
	else:
		results = videoAns.objects.all()
	return render(request, 'all_submmision.html', {'results': results, 'query': query, 'url': url})


@staff_member_required
@login_required(login_url='login')
def Add_assessment(request):
	if request.method == 'GET':
		ass_name = request.GET.get('ass_name')
		ass_dec = request.GET.get('ass_dec')
		new_ass = allAssessment()
		new_ass.assessmentName = ass_name
		new_ass.assessmentDes = ass_dec
		new_ass.save()
		return redirect('addassessment')
	return redirect('addassessment')


@staff_member_required
@login_required(login_url='login')
def add_assessment(request):
	return render(request, 'add_assessments.html')


@staff_member_required
@login_required(login_url='login')
def view_assessments(request, ass_id):

	ass_id = ass_id
	assessment = allAssessment.objects.filter(assId=ass_id)
	allque = allAssessment.objects.get(assId=ass_id).question_set.all()[:5]
	return render(request, 'assview.html', {'ques': allque, 'ass': assessment})


@staff_member_required
@login_required(login_url='login')
def Add_question(request):
		if request.method == 'GET':
			que = request.GET.get('que')
			ops1 = request.GET.get('ops1')
			ops2 = request.GET.get('ops2')
			ops3 = request.GET.get('ops3')
			ops4 = request.GET.get('ops4')
			ass_name = request.GET.get('ass')
			ass = allAssessment.objects.get(assessmentName=ass_name)
			ass_id = ass.assId
			new_que = Question()
			new_que.quostion = que
			new_que.ops1 = ops1
			new_que.ops2 = ops2
			new_que.ops3 = ops3
			new_que.ops4 = ops4
			new_que.assessment = ass
			new_que.save()
			return HttpResponseRedirect(reverse("view", args=(ass_id,)))
		return HttpResponseRedirect(reverse("view", args=(ass_id,)))
# ebb5f4cc42d841d0aa7369f975d9af42

@staff_member_required
@login_required(login_url='login')
def view_analysis(request, ansId):
	url = settings. MEDIA_URL
	result = videoAns.objects.filter(ansId=ansId)
	for ass in result:
			aname = ass.assessment_name


	return render(request, "analysis.html", {"result": result, 'url': url})


@staff_member_required
@login_required(login_url='login')
def generate_tras(request, ansId):
	ref_url = request.META.get('HTTP_REFERER')
	result = videoAns.objects.get(ansId=ansId)
	vf = result.videoAns.path
	import requests
	API_KEY = "623cfea0aba24d8f981195bbc20d48e0"
	filename = vf

# Upload Module Begins
	def read_file(filename, chunk_size=5242880):
		with open(filename, 'rb') as _file:
			while True:
				data = _file.read(chunk_size)
				if not data:
					break
				yield data

	headers = {'authorization': API_KEY}
	response = requests.post('https://api.assemblyai.com/v2/upload',
                        headers=headers,
                        data=read_file(filename))

	json_str1 = response.json()
# Upload Module Ends

# Submit Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript"
	json = {
    	"audio_url": json_str1["upload_url"]
	}

	response = requests.post(endpoint, json=json, headers=headers)

	json_str2 = response.json()
# Submit Module Ends

# CheckStatus Module Begins
	endpoint = "https://api.assemblyai.com/v2/transcript/" + json_str2["id"]

	response = requests.get(endpoint, headers=headers)

	json_str3 = response.json()

	while json_str3["status"] != "completed":
		response = requests.get(endpoint, headers=headers)
		json_str3 = response.json()
# CheckStatus Module Ends
	result.trasnscript = json_str3["text"]
	result.save()
	messages.success(request, 'Transcript is generated Successfully.')
	return HttpResponseRedirect(ref_url)

@staff_member_required
@login_required(login_url='login')
def generate_result(request):
	if request.method == 'GET':
		ansId = request.GET.get('ansId')
		expected_answer = request.GET.get('exampleRadios')
		s1 = expected_answer
		ref_url = request.META.get('HTTP_REFERER')
		answer = videoAns.objects.filter(ansId=ansId)
		for trans in answer:
			s2 = trans.trasnscript
		Percent = Cal_Accu(s1, s2)
		answer=videoAns.objects.get(ansId=ansId)
		answer.answer_accurecy=Percent
		answer.save()
		print(s1)
		print(s2)
	return HttpResponseRedirect(ref_url)







    


	