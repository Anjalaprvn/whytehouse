# Quick Reference - Sample Data

## Database Summary

| Item | Count | Details |
|------|-------|---------|
| **Accounts** | 3 | SBI, HDFC, ICICI |
| **Resorts** | 5 | Goa (2), Jaipur, Munnar, Manali |
| **Meal Plans** | 4 | EP, CP, MAP, AP |
| **Invoices** | 15 | Last 3 months |
| **Vouchers** | 10 | Last 2 months |
| **Customers** | 3 | Existing |
| **Employees** | 3 | Existing |

## Quick Commands

### Populate Data
```bash
python manage.py populate_data
```

### Check Counts
```bash
python manage.py shell -c "from admin_panel.models import *; print('Invoices:', Invoice.objects.count(), '| Resorts:', Resort.objects.count(), '| Accounts:', Account.objects.count())"
```

### Delete All Sample Data
```python
python manage.py shell
from admin_panel.models import Invoice, Voucher, Resort, Account, Meal
Invoice.objects.all().delete()
Voucher.objects.all().delete()
Resort.objects.all().delete()
Account.objects.all().delete()
Meal.objects.all().delete()
```

## Quick Links

| Feature | URL |
|---------|-----|
| **Invoice Report** | http://127.0.0.1:8000/sales/reports/invoice/ |
| **Invoice List** | http://127.0.0.1:8000/sales/invoices/ |
| **Add Invoice** | http://127.0.0.1:8000/sales/invoices/add/ |
| **Voucher List** | http://127.0.0.1:8000/sales/vouchers/ |
| **Resort List** | http://127.0.0.1:8000/sales/resorts/ |
| **Account List** | http://127.0.0.1:8000/sales/accounts/ |
| **Meal List** | http://127.0.0.1:8000/sales/meals/ |
| **Employee List** | http://127.0.0.1:8000/employee/ |

## Sample Resorts

1. **Nilaya Resort & Spa** - Goa
2. **Amber Palace Resort** - Jaipur
3. **Jungle Retreat** - Munnar
4. **Beach Paradise Resort** - Goa
5. **Mountain View Lodge** - Manali

## Sample Accounts

1. **Whyte House Primary** - SBI (Current)
2. **Whyte House Savings** - HDFC (Savings)
3. **Business Operations** - ICICI (Current)

## Testing Invoice Report

### Test 1: All Invoices for a Resort
```
From Date: 2024-12-01
To Date: 2026-02-28
Resort: Nilaya Resort & Spa
Employee View: OFF
```

### Test 2: Employee Performance
```
From Date: 2024-12-01
To Date: 2026-02-28
Resort: Any
Employee View: ON
Employee: Select any employee
```

### Test 3: Monthly Report
```
From Date: 2026-01-01
To Date: 2026-01-31
Resort: Any
Employee View: OFF
```

## Invoice Date Distribution

- **Dec 2024**: 6 invoices
- **Jan 2026**: 6 invoices
- **Feb 2026**: 3 invoices

## Price Ranges

- **Invoices**: ₹5,000 - ₹20,000
- **Vouchers**: ₹8,000 - ₹25,000
- **Tax**: 18% GST included

## Payment Status

- **Fully Paid**: ~33% of invoices
- **75% Paid**: ~33% of invoices
- **50% Paid**: ~33% of invoices

## Quick Verification

```bash
# Check if data exists
python manage.py shell -c "from admin_panel.models import Invoice; print('Total Invoices:', Invoice.objects.count()); print('Date Range:', Invoice.objects.first().invoice_date if Invoice.objects.exists() else 'No data', 'to', Invoice.objects.last().invoice_date if Invoice.objects.exists() else 'No data')"
```

## Troubleshooting

### No employees in dropdown?
- Employees must have invoices assigned
- Check: `Invoice.objects.filter(sales_person__isnull=False).count()`

### No data in report?
- Check date range matches invoice dates
- Verify resort has invoices
- Check if employee has invoices (if employee view enabled)

### Want more data?
- Run `python manage.py populate_data` again
- Or manually create invoices at `/sales/invoices/add/`

## Summary

✅ 15 invoices created across 5 resorts
✅ 10 vouchers created
✅ 3 bank accounts ready
✅ 4 meal plans available
✅ All employees have invoices assigned
✅ Ready to test invoice report!

**Start Testing**: http://127.0.0.1:8000/sales/reports/invoice/
