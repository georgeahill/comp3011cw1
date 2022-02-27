from itertools import chain
import json

from django.contrib import auth
from django.contrib.auth.models import User, Permission
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Professor, Module, Teaching, Rating


@csrf_exempt
def HandleRegisterRequest(request):
    # limit user permissions
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    email = request.POST.get("email", None)

    # print(list(p.codename for p in Permission.objects.all()))
    if username and password and email:
        try:
            user = User.objects.create_user(
                username=username, password=password, email=email
            )
        except IntegrityError:
            return HttpResponse("User exists", status=400)

        user.user_permissions.set(
            [
                Permission.objects.get(codename="add_rating"),
                Permission.objects.get(codename="view_teaching"),
                Permission.objects.get(codename="view_module"),
                Permission.objects.get(codename="view_professor"),
            ]
        )

        return HttpResponse()
    else:
        return HttpResponse(status=400)

    return HttpResponse("Not Implemented")


@csrf_exempt
def HandleLoginRequest(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


def HandleLogoutRequest(request):
    auth.logout(request)
    return HttpResponse(status=200)


def Handle500(request, *args, **kwargs):
    return HttpResponse(status=400)


def HandleTeachingListRequest(request):
    teachings = Teaching.objects.all()

    retObj = {}

    for teaching in teachings:
        hashTuple = (
            teaching.module.code,
            teaching.module.name,
            teaching.year,
            teaching.semester,
        )

        if hashTuple not in retObj:
            retObj[hashTuple] = [teaching.professor.__str__()]
        else:
            retObj[hashTuple].append(teaching.professor.__str__())

    outvals = []

    for values in retObj.items():
        outvals.append(list(values[0]) + [values[1]])

    return HttpResponse(json.dumps(outvals))


def GetProfessorRating(professor_id, module_id=None):
    if module_id:
        teachings = Teaching.objects.filter(
            professor__code=professor_id, module__code=module_id
        )
    else:
        teachings = Teaching.objects.filter(professor__code=professor_id)

    ratings = list(chain(*chain(teaching.rating_set.all() for teaching in teachings)))

    if len(ratings) == 0:
        return "'No ratings yet'"

    avg = 0
    for rating in ratings:
        avg += rating.rating

    avg /= len(ratings)

    # to avoid banker's rounding we add 0.5 and floor
    avg = int(avg + 0.5)

    return "*" * avg


def HandleProfessorRatingRequest(request, professor_id):
    ratings = GetProfessorRating(professor_id)
    return HttpResponse(json.dumps(ratings))


@csrf_exempt
def HandleProfessorModuleRatingRequest(request, professor_id, module_id):
    if request.method == "POST" and request.user.is_authenticated:
        # TODO: verification of input
        year = request.POST.get("year")
        semester = request.POST.get("semester")
        rating = request.POST.get("rating")

        if rating not in ("1", "2", "3", "4", "5"):
            return HttpResponse("Invalid rating", status=400)

        teaching = Teaching.objects.filter(
            professor__code=professor_id,
            module__code=module_id,
            year=year,
            semester=semester,
        )[0]

        if not teaching:
            return HttpResponse("Module instance not found", status=400)

        new_rating, created = Rating.objects.update_or_create(
            rated_id=teaching.id, user_id=request.user.id, defaults={"rating": rating}
        )

        new_rating.save()

        return HttpResponse(new_rating)
    elif request.method == "POST" and not request.user.is_authenticated:
        return HttpResponse(status=401)
    else:
        professor = Professor.objects.get(code=professor_id)
        module = Module.objects.get(code=module_id)
        avg = f"The rating for {professor} in module {module} is {GetProfessorRating(professor_id, module_id)}"

        return HttpResponse(json.dumps(avg))
