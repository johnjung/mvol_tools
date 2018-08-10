from django.shortcuts import render
from django.http import HttpResponse
from listpage.multilist import *
from listpage.multilistxtract import *
from listpage.models import mvolFolder
import html
import json
import datetime
import time
import pytz

# Create your views here.

def main(request):
	context = {'allists' : exmultilist.lists}
	return render(request, 'listpage/main.html', context)

def hierarch(request, mvolfolder_name):

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
			return None

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
	with open('listpage/holdname.json', "r") as jsonfile:
		fjson = json.load(jsonfile)

	currdir = fjson

	for subsect in namesections:
				if first:
					namehold = subsect
					first = False
				else:
					namehold = namehold + "-" + subsect
				parentlist.append((namehold, subsect))
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
		prosync = ex
		devsync = ex
		localize(child)		
		currtime = child[1]['owncloud'][1]
		devsync = chxistnrecent(currtime, child[1]['development'][1])
		prosync = chxistnrecent(currtime, child[1]['production'][1])
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
	}
	
	return render(request, 'listpage/mvolpagejson.html', context)
'''
	def hierarch(request, mvolfolder_name):
		#this one works on with a database


	target = mvolFolder.objects.get(name = mvolfolder_name)

	parentlist = []
	curr = target
	namesections = mvolfolder_name.split("-")
	finalchunk = namesections.pop()
	#finalchunk taken seperately as it's only section in breadcrumb
	# trail that does not have a link
	i = len(namesections) - 1
	while(curr.parent):
		parentlist = [(curr.parent, namesections[i] + '-')] + parentlist
		curr = curr.parent
		i -= 1
	
	prelist = target.children.all()
	prelist = prelist.extra(order_by = ['name'])
	childlist = []
	check = html.unescape("&#10004;")
	ex = html.unescape("&#10006;")
	
	def chxistnrecent(lasttime, comparetime):
		# checks if two times exist and compares them
		if lasttime and comparetime:
			if comparetime > lasttime:
					lasttime = comparetime
		else:
			if comparetime:
						lasttime = comparetime
		return lasttime

	def retrievevalsyn(child):
		#recursively tells if upper levels in hierarchy are completely
		# valid and synced based on lower levels
		potentialchildren = child.children.all()
		link = False
		if potentialchildren:
			link = True
			valid = check
			devsync = check
			prosync = check
			lastdev = None
			lastpro = None
			#lastdev and prodev give a folder's most recent upload time
			# to both servers so that upper levels can update their own times
			child.valid = True
			for grandchild in potentialchildren:
				info = retrievevalsyn(grandchild)
				if grandchild.date > child.date:
					child.date = grandchild.date
				if info[1] == ex:
					valid = ex
					child.valid = False
				if info[2] == ex:
					devsync = ex
				if info[3] == ex:
					prosync = ex
				lastdev = chxistnrecent(lastdev, grandchild.dev)
				lastpro = chxistnrecent(lastpro, grandchild.pro)
			if devsync == check:
				child.dev = lastdev
			if prosync == check:
				child.pro = lastpro
			child.save()
		else:
			valid = ex
			devsync = ex
			prosync = ex
			if child.valid:
				valid = check
				if child.dev:
					if child.date < child.dev:
						devsync = check
				if child.pro:
					if child.date < child.pro:
						prosync = check
		return(child, valid, devsync, prosync, link)

	for child in prelist:
		childlist.append(retrievevalsyn(child))
	context = {'name' : (mvolfolder_name, finalchunk),
						'parents' : parentlist,
						'children' : childlist,
	}
	
	return render(request, 'listpage/mvolpage.html', context)
	'''