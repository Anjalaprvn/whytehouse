# Sample Data Population Guide

## Overview
The database has been populated with sample data for testing the invoice report and other features.

## What Was Created

### 1. Bank Accounts (3)
- **Whyte House Primary Account** - State Bank of India (Current)
- **Whyte House Savings** - HDFC Bank (Savings)
- **Business Operations Account** - ICICI Bank (Current)

### 2. Resorts (5)
- **Nilaya Resort & Spa** - Goa
- **Amber Palace Resort** - Jaipur
- **Jungle Retreat** - Munnar
- **Beach Paradise Resort** - Goa
- **Mountain View Lodge** - Manali

### 3. Meal Plans (4)
- **European Plan (EP)** - Room only
- **Continental Plan (CP)** - Room with breakfast
- **Modified American Plan (MAP)** - Room with breakfast and dinner
- **American Plan (AP)** - Room with all meals

### 4. Invoices (15)
- Spread across last 3 months
- Random assignments to employees and resorts
- Various package prices (₹5,000 - ₹20,000)
- Different payment statuses (partial/full)
- Includes GST calculations

### 5. Vouchers (10)
- Spread across last 2 months
- Random assignments to employees and resorts
- Various package prices (₹8,000 - ₹25,000)
- Different payment statuses

## How to Use

### Test Invoice Report
1. Go to: `http://127.0.0.1:8000/sales/reports/invoice/`
2. Select date range: Last 3 months
3. Select any resort from the dropdown
4. Click "Fetch Details" to see invoices

### Test Employee Filter
1. Go to: `http://127.0.0.1:8000/sales/reports/invoice/`
2. Enable "Employee View Report" toggle
3. Select an employee from dropdown
4. Only shows employees who have invoices assigned

### View Invoices
- List: `http://127.0.0.1:8000/sales/invoices/`
- Add: `http://127.0.0.1:8000/sales/invoices/add/`

### View Vouchers
- List: `http://127.0.0.1:8000/sales/vouchers/`
- Add: `http://127.0.0.1:8000/sales/vouchers/add/`

### View Resorts
- List: `http://127.0.0.1:8000/sales/resorts/`
- Add: `http://127.0.0.1:8000/sales/resorts/add/`

### View Accounts
- List: `http://127.0.0.1:8000/sales/accounts/`
- Add: `http://127.0.0.1:8000/sales/accounts/add/`

### View Meals
- List: `http://127.0.0.1:8000/sales/meals/`
- Add: `http://127.0.0.1:8000/sales/meals/add/`

## Sample Data Details

### Invoice Distribution
```
December 2024: 6 invoices
January 2026: 6 invoices
February 2026: 3 invoices
```

### Resort Distribution
Each resort has 2-4 invoices assigned randomly

### Employee Distribution
Each employee (3 total) has 4-6 invoices assigned

### Payment Status
- Fully Paid: ~33%
- 75% Paid: ~33%
- 50% Paid: ~33%

## Re-running the Command

If you want to add more data, simply run:
```bash
python manage.py populate_data
```

**Note**: The command uses `get_or_create()`, so it won't create duplicates. It will skip existing records and only create new ones.

## Clearing Data

If you want to start fresh:

### Option 1: Delete Specific Data
```python
python manage.py shell

from admin_panel.models import Invoice, Voucher, Resort, Account, Meal

# Delete all invoices
Invoice.objects.all().delete()

# Delete all vouchers
Voucher.objects.all().delete()

# Delete all resorts
Resort.objects.all().delete()

# Delete all accounts
Account.objects.all().delete()

# Delete all meals
Meal.objects.all().delete()
```

### Option 2: Reset Database (Nuclear Option)
```bash
# Delete database
rm db.sqlite3

# Recreate database
python manage.py migrate

# Recreate superuser
python manage.py createsuperuser

# Repopulate data
python manage.py populate_data
```

## Customizing Sample Data

To modify the sample data, edit:
`admin_panel/management/commands/populate_data.py`

You can change:
- Number of invoices/vouchers
- Date ranges
- Price ranges
- Resort names and locations
- Account details
- Meal plan options

## Verification Commands

### Check Data Counts
```bash
python manage.py shell -c "from admin_panel.models import *; print('Accounts:', Account.objects.count()); print('Resorts:', Resort.objects.count()); print('Meals:', Meal.objects.count()); print('Invoices:', Invoice.objects.count()); print('Vouchers:', Voucher.objects.count())"
```

### Check Invoice Distribution by Resort
```python
python manage.py shell

from admin_panel.models import Invoice

for resort in Resort.objects.all():
    count = Invoice.objects.filter(resort=resort).count()
    print(f"{resort.resort_name}: {count} invoices")
```

### Check Invoice Distribution by Employee
```python
python manage.py shell

from admin_panel.models import Invoice, Employee

for emp in Employee.objects.all():
    count = Invoice.objects.filter(sales_person=emp).count()
    print(f"{emp.name}: {count} invoices")
```

### Check Date Range
```python
python manage.py shell

from admin_panel.models import Invoice

invoices = Invoice.objects.all().order_by('invoice_date')
if invoices:
    print(f"Earliest: {invoices.first().invoice_date}")
    print(f"Latest: {invoices.last().invoice_date}")
```

## Testing Scenarios

### Scenario 1: Resort Performance Report
1. Go to invoice report
2. Select "Nilaya Resort & Spa"
3. Select last 3 months
4. View all invoices for that resort

### Scenario 2: Employee Performance Report
1. Go to invoice report
2. Enable employee view
3. Select an employee
4. View their sales performance

### Scenario 3: Monthly Revenue Report
1. Go to invoice report
2. Select date range: January 1-31, 2026
3. Select any resort
4. Export to Excel for analysis

### Scenario 4: Payment Status Check
1. Go to invoice list
2. Check "Pending" amounts
3. Identify customers with outstanding payments

## Sample Invoice Details

### Example Invoice: INV-202601-0001
- Customer: Random from existing customers
- Date: January 2026
- Resort: Random from 5 resorts
- Package: ₹5,000 - ₹20,000
- Tax: 18% GST
- Status: Partial/Full payment

## Benefits of Sample Data

✅ **Immediate Testing** - No need to manually create data
✅ **Realistic Scenarios** - Data mimics real-world usage
✅ **Report Testing** - Can test all report features
✅ **Performance Testing** - See how system handles multiple records
✅ **Demo Ready** - Perfect for demonstrations

## Next Steps

1. ✅ Data populated successfully
2. Test invoice report with different filters
3. Test employee performance tracking
4. Test Excel export functionality
5. Create more invoices as needed
6. Customize data for your specific needs

## Summary

Your database now contains:
- 3 Bank Accounts
- 5 Resorts (across India)
- 4 Meal Plans
- 15 Invoices (last 3 months)
- 10 Vouchers (last 2 months)

All data is interconnected and ready for testing the invoice report and other features!
