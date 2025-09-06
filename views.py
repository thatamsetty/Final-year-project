from django.shortcuts import render,redirect
from app.models import Department,Faculty,Subject,Timetable
from django.contrib import messages
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth import logout 
# Create your views here.
from datetime import datetime,timedelta





def index(request):
    return render(request, 'index.html')


def admin_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        if email=='admin@gmail.com' and password=='admin@123':
            request.session ['email']=email
            request.session['login']='admin'
            # messages.success(request,'Login Successfully')
            print('login')
            return redirect ('/dashboard')
        else:
            messages.error(request,'Invalid Credential')
            return redirect('/admin_login')


    return render(request,'adminlogin.html')

def dashboard(request):
    return render(request,'dashboard.html')


def add_department(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        Department.objects.create(department_name=name,email=email, password=password)
        return redirect('/dashboard')
    return render(request,'add_department.html')

def manage_department(request):
    departments=Department.objects.all()
    return render(request,'manage_department.html',{'departments':departments})





def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)

    if request.method == 'POST':
        department.department_name = request.POST['department_name']
        department.email = request.POST['email']
        department.password = request.POST['password']
        department.save()

        messages.success(request, 'Department updated successfully')
        return redirect('/manage_department')  

    return render(request, 'edit_department.html', {'department': department})




def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    department.delete()

    messages.success(request, 'Department deleted successfully')
    return redirect('/manage_department')  


def logout(request):
    del request.session['email']
    del request.session['login']
    return redirect('/')




def department_login(request):
    if request.method == 'POST':
        email=request.POST['email']
        password=request.POST['password']

        try:
            department = Department.objects.get(email=email,password=password)
            request.session['email']=email
            request.session['department_id'] = department.id  # Store the department ID, not the email
            request.session['login'] = 'department' 


            if email==email and password==password:
                request.session['email'] = email
                # request.session['department_name'] = department.department_name
                request.session['login'] = 'department'
                # messages.success(request, 'Login Successfully')
                print('department')
                return redirect('/department_dashboard')
            else:
                print('not found')
                messages.error(request, 'Invalid credentials')
        except Department.DoesNotExist:
            messages.error(request, 'Invalid credentials')

    return render(request,'department_login.html')


def department_logout(request):
    logout(request)
    return redirect('/')



def department_dashboard(request):
    if request.session.get('login') == 'department':
        department_name = request.session.get('department_name')
        return render(request, 'department_dashboard.html', {'department_name': department_name})
    else:
        messages.error(request, 'You are not logged in')
        return redirect('/department_login')


def add_faculty(request):
    if request.method == 'POST':
        name=request.POST['name']
        department_id=request.POST['department']
        department=Department.objects.get(id=department_id)
        email=request.POST['email']
        designation = request.POST['designation']
        faculty=Faculty.objects.create(name=name,department=department,email=email,designation=designation)
        return redirect('/department_dashboard')
    departments=Department.objects.all()

    return render(request,'add_faculty.html',{'departments':departments})


def add_subject(request):
    if request.method == 'POST':
        name=request.POST['name']
        department_id=request.POST['department']
        faculty_id=request.POST['faculty']
        department=Department.objects.get(id=department_id)
        faculty=Faculty.objects.get(id=faculty_id)
        subject=Subject.objects.create(name=name,department=department,faculty=faculty)
        return redirect('/department_dashboard')
    departments=Department.objects.all()
    faculties=Faculty.objects.all()
    return render(request,'add_subject.html',{'departments':departments,'faculties':faculties})



import random




import random

# def generate_timetable(request):
#     department_id = request.session.get('department_id')
#     if not department_id:
#         return redirect('/department_login')

#     try:
#         department = Department.objects.get(id=department_id)
#     except Department.DoesNotExist:
#         return redirect('/department_login')

#     subjects = list(Subject.objects.filter(department=department))
#     days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
#     lunch_period = 4
#     periods_per_day = 8

#     # Clear existing timetable
#     Timetable.objects.filter(department=department).delete()

#     lab_subjects = [s for s in subjects if getattr(s, 'is_lab', False)]
#     theory_subjects = [s for s in subjects if not getattr(s, 'is_lab', False)]

#     if not lab_subjects:
#         print("Warning: No lab subjects found for the department.")
#     if not theory_subjects:
#         print("Warning: No theory subjects found for the department.")

#     # Pick exactly 2 unique lab days
#     lab_days = random.sample(days_of_week, 2)
#     print("Selected lab days:", lab_days,'$$$$$$$$')

    

#     for day in days_of_week:
#         used_periods = set()

#         # Exclude lab from theory subjects on non-lab days
#         if day in lab_days:
#             # non_lab_theory_subjects = [s for s in theory_subjects if s.name.lower() not in 'lab']
#             scheduled_theories = random.sample(theory_subjects, len(theory_subjects)) if theory_subjects else []
#             print(scheduled_theories,'#############')
            
            
#         else:
            

#             non_lab_theory_subjects = [s for s in theory_subjects if s.name.lower() != 'lab']
#             scheduled_theories = random.sample(non_lab_theory_subjects, len(non_lab_theory_subjects)) if non_lab_theory_subjects else []
#             print(scheduled_theories,'!!!!!!!!!!!!!!!')
            

#         subject_index = 0
#         target_name = 'lab'

#         # Find index of 'lab' in scheduled_theories safely (only on lab days)
#         if day in lab_days:
#             index = next((i for i, subj in enumerate(scheduled_theories) if target_name.lower() in subj.name.lower()), -1)
#             print(f"Index of lab in scheduled_theories on {day}:", index)

#             if index != -1:
#                 # Safely replace neighbors for 3 consecutive lab periods
#                 length = len(scheduled_theories)

#                 # The replacements depend on position to avoid index errors
#                 if index >= 2:
#                     # Replace previous two
#                     scheduled_theories[index-1] = scheduled_theories[index]
#                     scheduled_theories[index-2] = scheduled_theories[index]
#                 elif index == 1:
#                     scheduled_theories[index-1] = scheduled_theories[index]
#                     if index + 1 < length:
#                         scheduled_theories[index+1] = scheduled_theories[index]
#                 elif index == 0:
#                     if index + 1 < length:
#                         scheduled_theories[index+1] = scheduled_theories[index]
#                     if index + 2 < length:
#                         scheduled_theories[index+2] = scheduled_theories[index]

#             print("Scheduled theories after lab adjustment:", [s.name for s in scheduled_theories])

#         # Assign lab subject on lab days first
#         if day in lab_days and lab_subjects:
#             lab_subject = lab_subjects[0]
#             print(f"Assigning lab subject {lab_subject.name} on {day}")

#             possible_starts = [p for p in range(1, periods_per_day - 2) if lunch_period not in [p, p+1, p+2]]
#             random.shuffle(possible_starts)

#             for start_period in possible_starts:
#                 if all(p not in used_periods for p in [start_period, start_period+1, start_period+2]):
#                     for offset in range(3):
#                         period = start_period + offset
#                         start_time = calculate_start_time(period)
#                         end_time = calculate_end_time(start_time)

#                         Timetable.objects.create(
#                             department=department,
#                             subject=lab_subject,
#                             faculty=lab_subject.faculty,
#                             day_of_week=day,
#                             period=period,
#                             start_time=start_time,
#                             end_time=end_time
#                         )
#                         used_periods.add(period)
#                     break  # Lab assigned, stop searching start period

#         # Fill remaining periods with theory subjects (lab excluded on non-lab days)
#         for period in range(1, periods_per_day + 1):
#             if period == lunch_period or period in used_periods:
#                 continue
#             if not scheduled_theories:
#                 continue

#             subject = scheduled_theories[subject_index % len(scheduled_theories)]
#             subject_index += 1

#             if subject.faculty:
#                 start_time = calculate_start_time(period)
#                 end_time = calculate_end_time(start_time)

#                 Timetable.objects.create(
#                     department=department,
#                     subject=subject,
#                     faculty=subject.faculty,
#                     day_of_week=day,
#                     period=period,
#                     start_time=start_time,
#                     end_time=end_time
#                 )
#                 used_periods.add(period)

#     return redirect('view_table')

def generate_timetable(request):
    department_id = request.session.get('department_id')
    if not department_id:
        return redirect('/department_login')

    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return redirect('/department_login')

    subjects = list(Subject.objects.filter(department=department))
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    lunch_period = 4
    periods_per_day = 8

    # Clear existing timetable
    Timetable.objects.filter(department=department).delete()

    # lab_subjects = [s for s in subjects if getattr(s, 'is_lab', False)]
    # theory_subjects = [s for s in subjects if not getattr(s, 'is_lab', False)]
    lab_subjects = [s for s in subjects if 'lab' in s.name.lower()]
    theory_subjects = [s for s in subjects if 'lab' not in s.name.lower()]

    if not lab_subjects:
        print("Warning: No lab subjects found for the department.")
    if not theory_subjects:
        print("Warning: No theory subjects found for the department.")

    # Pick 2 lab days and assign different lab subjects
    lab_days = random.sample(days_of_week, 2)
    lab_day_subject_map = dict(zip(lab_days, lab_subjects[:2]))  # One lab subject per lab day

    print("Selected lab days and their subjects:", {day: subj.name for day, subj in lab_day_subject_map.items()})

    for day in days_of_week:
        used_periods = set()
        scheduled_theories = []

        is_lab_day = day in lab_days
        lab_subject = lab_day_subject_map.get(day)

        if is_lab_day and lab_subject:
            # Assign 3 consecutive periods for lab (excluding lunch)
            print(f"Assigning lab: {lab_subject.name} on {day}")
            possible_starts = [
                p for p in range(1, periods_per_day - 2)
                if lunch_period not in [p, p + 1, p + 2]
            ]
            random.shuffle(possible_starts)

            for start_period in possible_starts:
                if all(p not in used_periods for p in [start_period, start_period + 1, start_period + 2]):
                    for offset in range(3):
                        period = start_period + offset
                        start_time = calculate_start_time(period)
                        end_time = calculate_end_time(start_time)

                        Timetable.objects.create(
                            department=department,
                            subject=lab_subject,
                            faculty=lab_subject.faculty,
                            day_of_week=day,
                            period=period,
                            start_time=start_time,
                            end_time=end_time
                        )
                        used_periods.add(period)
                    break

            # For the rest of the day: schedule only theory subjects
            available_theories = [s for s in theory_subjects if s != lab_subject]
            scheduled_theories = random.sample(available_theories, len(available_theories)) if available_theories else []

        else:
            # Non-lab day: only theory subjects
            scheduled_theories = random.sample(theory_subjects, len(theory_subjects)) if theory_subjects else []

        # Fill the rest of the periods
        subject_index = 0
        for period in range(1, periods_per_day + 1):
            if period == lunch_period or period in used_periods:
                continue

            if not scheduled_theories:
                continue

            subject = scheduled_theories[subject_index % len(scheduled_theories)]
            subject_index += 1

            if subject.faculty:
                start_time = calculate_start_time(period)
                end_time = calculate_end_time(start_time)

                Timetable.objects.create(
                    department=department,
                    subject=subject,
                    faculty=subject.faculty,
                    day_of_week=day,
                    period=period,
                    start_time=start_time,
                    end_time=end_time
                )
                used_periods.add(period)

    return redirect('view_table')


def calculate_start_time(period):
    base_time = datetime.strptime('09:00', '%H:%M')
    return (base_time + timedelta(hours=(period - 1))).time()

def calculate_end_time(start_time):
    return (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()



# def calculate_start_time(period):
#     """Calculate the start time based on the period number."""
#     start_hour = 9 + (period - 1)  # Starts at 9:00 AM and increments by 1 hour for each period
#     return datetime.strptime(f"{start_hour}:00", "%H:%M").time()

# def calculate_end_time(start_time):
#     """Calculate the end time by adding 1 hour (60 minutes) to the start time."""
#     start_datetime = datetime.combine(datetime.today(), start_time)
#     end_datetime = start_datetime + timedelta(minutes=60)  # Each period lasts 60 minutes (1 hour)
#     return end_datetime.time()

def calculate_start_time(period):
    base_time = datetime.strptime('09:00', '%H:%M')
    return (base_time + timedelta(hours=(period - 1))).time()

def calculate_end_time(start_time):
    return (datetime.combine(datetime.today(), start_time) + timedelta(hours=1)).time()


from django.shortcuts import render, redirect
from .models import Department, Timetable

def view_table(request):
    # Get department ID from session
    department_id = request.session.get('department_id')
    if not department_id:
        return redirect('/department_login')

    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return redirect('/department_login')

    # Get all timetable entries for the department
    timetable_entries = Timetable.objects.filter(department=department)

    # Prepare dictionary for each weekday
    timetable_data = {
        'Monday': [],
        'Tuesday': [],
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
    }

    # Store lab subjects' period indices
    lab_periods = set()

    for entry in timetable_entries:
        # Format time for comparison in template
        entry.start_time_formatted = entry.start_time.strftime('%H:%M:%S')
        entry.end_time_formatted = entry.end_time.strftime('%H:%M:%S')

        # Collect the lab periods (for display later)
        if entry.subject.is_lab:  # Assuming 'is_lab' is an attribute
            for i in range(entry.period, entry.period + 3):  # Lab spans 3 periods
                lab_periods.add((entry.day_of_week, i))

        if entry.day_of_week in timetable_data:
            timetable_data[entry.day_of_week].append(entry)

    # Sort entries by period to keep correct order in each row
    for day in timetable_data:
        timetable_data[day].sort(key=lambda x: x.period)

    # Define standard time slots (must match generate_timetable logic)
    time_slots = [
        '09:00:00', '10:00:00', '11:00:00', '12:00:00',
        '13:00:00', '14:00:00', '15:00:00', '16:00:00'
    ]

    # Mark lab periods with a special tag in the timetable
    for day in timetable_data:
        for entry in timetable_data[day]:
            if (day, entry.period) in lab_periods:
                entry.is_lab = True  # Mark as lab for display

    return render(request, 'view_table.html', {
        'timetable_data': timetable_data,
        'department': department,
        'time_slots': time_slots
    })









