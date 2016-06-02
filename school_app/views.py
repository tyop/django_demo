from django.shortcuts import render
from school_app.models import School, Classroom, Student, SchoolSelect
from django.http import JsonResponse
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
import json

def traverse(root_node, level=0, nodes=[], edges=[]):
    if isinstance(root_node, QuerySet):
        for node in root_node:
             traverse(node, level, nodes, edges)
    else:
        next_id = len(nodes)
        node_dict = {"id":next_id, "label":root_node.name, "group":level, "value":0}
        nodes.append(node_dict)
        level += 1
        if hasattr(root_node, "children"):
            parent = next_id
            for node in root_node.children.all():
                edges.append({"to":parent, "from":len(nodes)})
                traverse(node, level, nodes, edges)
    return {"nodes":nodes, "edges":edges}

def make_tree(school_id=None):
    data = {"nodes":[], "edges":[]}
    school_objects = School.objects
    if school_id is None:
        school_objects = school_objects.all()
    else:
        school_objects = school_objects.filter(pk=school_id)
    data = traverse(school_objects, level=0, nodes=[], edges=[])
    return data

def network(request):
    school_select = SchoolSelect(data=request.POST)

    context_dict = {
    "forms":{
        "school":school_select,
        }
    }
    resp = None
    if request.method == "POST":
        school_id = None
        if school_select.is_valid():
            school_id = school_select.data["schools"]
        resp = JsonResponse(make_tree(school_id))
    else:
        context_dict["vis_data"] = mark_safe(json.dumps(make_tree()))
        resp = render(request,'network.html',context=context_dict)

    return resp
