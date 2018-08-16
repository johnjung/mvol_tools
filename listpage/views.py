from django.shortcuts import render
from django.http import HttpResponse
import html
import json
import datetime
import time
import pytz
from itertools import islice
from base.views import breadcrumbs


# Create your views here.

def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

def homepage(request):
	breadcrumbs = [{
        "href": "/",
        "text": "Home"
    }]
	context = {"breadcrumbs" : breadcrumbs}
	return render(request, 'listpage/homepage.html', context)

def errpage(request):
	breadcrumbs = [{
	"href": "/",
	"text": "Home"},
	{"href": "/emilproject", "text": "Emil Project Homepage"}]
	errors = ["This thing was bad.",
	"This other thing was even worse.",
	"Whoa, slow down now, what is this."]
	context = {'errarray' : errors, "breadcrumbs" : breadcrumbs}
	return render(request, 'listpage/errpage.html', context)

def prelistpage(request):
	breadcrumbs = [{
      "href": "/",
      "text": "Home"},
      {"href": "/emilproject", "text": "Emil Project Homepage"}]
	with open('listpage/listsnar.json', "r") as jsonfile:
		fjson = json.load(jsonfile)
	n = 5
	fjson = {"none" : (take(n, fjson["none"]), len(fjson["none"]) > n),
		"ready" : (take(n, fjson["ready"]), len(fjson["ready"]) > n),
		"queue" : (take(n, fjson["queue"]), len(fjson["queue"]) > n),
		"valid" : (take(n, fjson["valid"]), len(fjson["valid"]) > n),
		"invalid" : (take(n, fjson["invalid"]), len(fjson["invalid"]) > n)}

	def localized(start):
		timezone = pytz.timezone("America/Chicago")	
		for child in start.items():
			for grandchild in child[1][0]:
				grandchild[1] = timezone.localize(datetime.datetime.fromtimestamp(grandchild[1]))

	localized(fjson)
	context = {"allists" : fjson, "breadcrumbs": breadcrumbs}
	return render(request, 'listpage/prelistpage.html', context)

def listpage(request, status):
	breadcrumbs = [{
      "href": "/",
      "text": "Home"},
      {"href": "/emilproject", "text": "Emil Project Homepage"},
      {"href": "/emilproject/mvolreport", "text": "Mvol Report"} ]
	with open('listpage/listsnar.json', "r") as jsonfile:
		fjson = json.load(jsonfile)
	def localizer(start):
		timezone = pytz.timezone("America/Chicago")	
		for child in start:
			child[1] = timezone.localize(datetime.datetime.fromtimestamp(child[1]))
	localizer(fjson[status])
	context = {"allists" : fjson[status],
							"name": status, "breadcrumbs": breadcrumbs}
	return render(request, 'listpage/listpage.html', context)

def hierarch(request, mvolfolder_name):
	breadcrumbs = [{
      "href": "/",
      "text": "Home"},
      {"href": "/emilproject", "text": "Emil Project Homepage"}]

	def chxistnrecent(currtime, comparetime):
		# checks if two times exist and compares them
		checkd = html.unescape("&#10004;")
		exd = html.unescape("&#10006;")
		if comparetime:
			if comparetime < currtime:
				return exd
			else:
				return checkd
		else:
			return "none"

	def chxistnrecentx(status):
		# checks if two times exist and compares them
		checkd = html.unescape("&#10004;")
		exd = html.unescape("&#10006;")
		if status == "in-sync":
			return checkd
		elif status == "out-of-sync":
			return exd
		else:
			return "none"

	def localize(child):
		timezone = pytz.timezone("America/Chicago")	
		try:
			child[1]['owncloud'][1] = timezone.localize(datetime.datetime.fromtimestamp(child[1]['owncloud'][1]))
		except Exception:
			pass
		try:
			child[1]['development'][1] = timezone.localize(datetime.datetime.fromtimestamp(child[1]['development'][1]))
		except Exception:
			pass
		try:
			child[1]['production'][1] = timezone.localize(datetime.datetime.fromtimestamp(child[1]['production'][1]))
		except Exception:
			pass


	currname = mvolfolder_name
	namesections = mvolfolder_name.split("-")
	finalchunk = namesections.pop()

	parentlist = []
	namehold = ""
	first = True
	with open('listpage/snar.json', "r") as jsonfile:
		fjson = json.load(jsonfile)

	currdir = fjson

	for subsect in namesections:
				if first:
					namehold = subsect
					first = False
				else:
					namehold = namehold + "-" + subsect
				parentlist.append((namehold, subsect))
				breadcrumbs.append({"href" : "/emilproject/" + namehold, "text" : subsect})
				try:
					currdir = currdir[namehold]['children']
				except Exception as e:
					break
	if mvolfolder_name == "mvol":
			prechildlist = currdir['mvol']['children']
	else:
		namehold = namehold + "-" + finalchunk
		try:
			prechildlist = currdir[namehold]['children']
		except Exception as e:
			prechildlist = {}
	childlist = []
	i = 0
	childnames = prechildlist.keys()
	check = html.unescape("&#10004;")
	ex = html.unescape("&#10006;")
	for child in prechildlist.items():
		valid = ex
		prosync = "none"
		devsync = "none"
		localize(child)		
		currtime = child[1]['owncloud'][1]
		if child[1]['development'][0] == "in-sync":
			devsync = check
		elif child[1]['development'][0] == "out-of-sync":
			devsync = ex
		if child[1]['production'][0] == "in-sync":
			prosync = check
		elif child[1]['production'][0] == "out-of-sync":
			prosync = ex
		if child[1]['owncloud'][0] == "valid":
			valid = check
		childlist.append((list(childnames)[i], child, valid, devsync, prosync))
		i += 1

	oneupfrombottom = False
	if childlist:
		if not 'children' in childlist[0][1][1]:
			oneupfrombottom = True

	context = {'name' : (currname, finalchunk),
						'parents' : parentlist,
						'children' : childlist,
						'oneupfrombottom' : oneupfrombottom,
						'breadcrumbs': breadcrumbs
	}
	
	return render(request, 'listpage/mvolpagejson.html', context)