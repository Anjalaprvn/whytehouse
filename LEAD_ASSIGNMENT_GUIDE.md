# Round-Robin Lead Assignment System

## Overview
This system automatically distributes leads among employees in a rotating manner. When a new lead is added or edited, it's assigned to the next employee in the sequence.

## How It Works

### Example with 3 Employees
- Employee 1, Employee 2, Employee 3

**Sequence:**
1. Lead 1 → Employee 1
2. Lead 2 → Employee 2
3. Lead 3 → Employee 3
4. Lead 4 → Employee 1 (cycles back)
5. Lead 5 → Employee 2
6. And so on...

## Implementation Details

### Helper Functions
Located in: `admin_panel/lead_assignment.py`

#### `get_next_employee_for_lead()`
- Returns the next employee who should be assigned a lead
- Finds the last assigned lead and gets the next employee in rotation
- If no leads exist, returns the first active employee
- Handles edge cases when employees are deleted

#### `get_employees_ordered_for_display()`
- Returns all active employees with the next assignee first
- Used in forms to show the recommended employee at the top

### Views Using This System

#### `add_lead(request)`
- When no employee is selected, auto-assigns using `get_next_employee_for_lead()`
- Displays employees with next assignee first in the form

#### `edit_lead(request, id)`
- Shows employees ordered with next assignee first
- Allows manual override of assignment

#### `view_lead(request, lead_id)`
- Shows employees ordered with next assignee first
- Allows reassignment if needed

## Key Features

✅ **Automatic Distribution** - Leads are evenly distributed among active employees
✅ **Scalable** - Works with any number of employees (3, 5, 10, etc.)
✅ **Manual Override** - Users can still manually assign leads if needed
✅ **Active Employees Only** - Only employees with "Active" status are included
✅ **Handles Deletions** - If an employee is deleted, the system adapts automatically

## Adding New Employees

When you add a new employee:
1. Set their status to "Active"
2. They'll automatically be included in the rotation
3. The next lead will be assigned to them when their turn comes

## Removing Employees

When you deactivate an employee:
1. Change their status to "Inactive" or "On Leave"
2. They'll be excluded from future assignments
3. Existing leads assigned to them remain unchanged

## Database Queries

The system uses these queries:
- `Employee.objects.filter(status='Active').order_by('id')` - Get active employees
- `Lead.objects.filter(employee__isnull=False).order_by('-created_at').first()` - Get last assigned lead

## Testing the System

To verify the round-robin assignment:
1. Create 3 active employees
2. Add leads one by one
3. Check that each lead is assigned to the next employee in sequence
4. Verify the cycle repeats after the last employee

## Future Enhancements

Possible improvements:
- Load balancing (assign to employee with fewer leads)
- Time-based rotation (assign based on time of day)
- Skill-based assignment (assign based on employee expertise)
- Geographic assignment (assign based on customer location)
