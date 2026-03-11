from .models import Lead, Employee

def get_next_employee_for_lead():
    """
    Get the next employee in round-robin order for lead assignment.
    Returns the employee who should be assigned the next lead.
    """
    active_employees = Employee.objects.filter(status='Active').order_by('id')
    if not active_employees.exists():
        return None
    
    last_lead = Lead.objects.filter(employee__isnull=False).order_by('-created_at').first()
    if not last_lead or not last_lead.employee:
        return active_employees.first()
    
    employees_list = list(active_employees)
    try:
        last_index = next(i for i, emp in enumerate(employees_list) if emp.id == last_lead.employee_id)
        next_index = (last_index + 1) % len(employees_list)
        return employees_list[next_index]
    except (StopIteration, IndexError):
        return employees_list[0]


def get_employees_ordered_for_display(exclude_lead_id=None):
    """
    Get all active employees ordered with the next assignee first.
    Useful for displaying employee lists in forms.
    """
    all_employees = Employee.objects.filter(status='Active').order_by('name')
    next_emp = get_next_employee_for_lead()
    
    employees_list = list(all_employees)
    if next_emp and next_emp in employees_list:
        employees_list.remove(next_emp)
        employees_list.insert(0, next_emp)
    
    return employees_list
