from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Sum

from .forms import RegisterForm, SemesterForm, GRADE_POINTS
from .models import CGPARecord, SemesterCourse


# ─────────────────────────────
# AUTH
# ─────────────────────────────

def homepage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'cgpaapp/home.html')


def register_view(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'cgpaapp/register.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')

    return render(request, 'cgpaapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')


# ─────────────────────────────
# DASHBOARD
# ─────────────────────────────

@login_required
def dashboard(request):
    records = CGPARecord.objects.filter(user=request.user)
    cgpa = compute_cgpa(records)

    return render(request, 'cgpaapp/dashboard.html', {
        'records': records,
        'cgpa': cgpa,
        'total_semesters': records.count(),
    })


# ─────────────────────────────
# GRADE
# ─────────────────────────────

def get_grade(score):
    if score >= 70: return "A"
    if score >= 60: return "B"
    if score >= 50: return "C"
    if score >= 45: return "D"
    if score >= 40: return "E"
    return "F"


# ─────────────────────────────
# GPA CALCULATOR (FINAL FIX)
# ─────────────────────────────

@login_required
def calculate(request):
    form = SemesterForm(request.POST or None)
    result = None
    error = None

    if request.method == 'POST' and form.is_valid():

        semester = form.cleaned_data['semester']

        names = request.POST.getlist('course_name[]')
        units = request.POST.getlist('unit[]')
        scores = request.POST.getlist('score[]')

        # remove empty rows safely
        valid_rows = [
            (n.strip(), u, s)
            for n, u, s in zip(names, units, scores)
            if n.strip() and u and s
        ]

        if not valid_rows:
            error = "No valid courses entered"
            return render(request, 'cgpaapp/calculate.html', {
                'semester_form': form,
                'error': error,
            })

        # create semester record
        record = CGPARecord.objects.create(
            user=request.user,
            semester=semester,
            gpa=0,
            total_units=0,
            total_credit_point=0,
        )

        total_units = 0
        total_points = 0
        courses = []

        for name, u, s in valid_rows:
            unit = float(u)
            score = float(s)

            grade = get_grade(score)
            point = GRADE_POINTS[grade]
            credit_point = unit * point

            SemesterCourse.objects.create(
                record=record,
                name=name,
                unit=unit,
                score=score,
                grade=grade,
                credit_point=credit_point,
            )

            courses.append({
                'name': name,
                'unit': unit,
                'score': score,
                'grade': grade,
                'credit_point': credit_point,
            })

            total_units += unit
            total_points += credit_point

        gpa = round(total_points / total_units, 2)

        record.gpa = gpa
        record.total_units = total_units
        record.total_credit_point = total_points
        record.save()

        cgpa = compute_cgpa(CGPARecord.objects.filter(user=request.user))

        result = {
            'semester': semester,
            'courses': courses,
            'gpa': gpa,
            'cgpa': cgpa
        }

    return render(request, 'cgpaapp/calculate.html', {
        'semester_form': form,
        'result': result,
        'error': error,
    })


# ─────────────────────────────
# DELETE
# ─────────────────────────────

@login_required
def delete_record(request, pk):
    record = get_object_or_404(CGPARecord, pk=pk, user=request.user)

    if request.method == 'POST':
        record.delete()

    return redirect('dashboard')


# ─────────────────────────────
# CGPA
# ─────────────────────────────

def compute_cgpa(records):
    agg = records.aggregate(
        sum_cp=Sum('total_credit_point'),
        sum_units=Sum('total_units'),
    )

    if agg['sum_units']:
        return round(agg['sum_cp'] / agg['sum_units'], 2)

    return 0.0


# ─────────────────────────────
# SEMESTER DETAIL (NOW WORKS)
# ─────────────────────────────

@login_required
def semester_detail(request, pk):
    record = get_object_or_404(CGPARecord, pk=pk, user=request.user)
    courses = record.courses.all()

    return render(request, 'cgpaapp/semester_detail.html', {
        'record': record,
        'courses': courses
    })