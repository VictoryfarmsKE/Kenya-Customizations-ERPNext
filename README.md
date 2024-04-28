### EXPNext Country Specific Functionality for Kenya

### Includes:

### Kenya Payroll Reports

• P9A Tax Deduction Card

• NSSF Report

• NHIF Report

• HELB Report

• Bank Payroll Advice Report

• Payroll Register Report

### Sales and Purchase Tax Reports

• Sales Tax Report

• Purchase Tax Report

### Installation

Using bench, [install ERPNext](https://github.com/frappe/bench#installation) as mentioned here.

Once ERPNext is installed, add CSF_KE app to your bench by running

```sh
$ bench get-app https://github.com/navariltd/CSF_KE.git
```

After that, you can install CSF_KE app on required site by running

```sh
$ bench --site [site.name] install-app csf_ke
```

##   
Casual Payroll System

### 1. Set-Up

**Doctypes:**

-   **Activity Type:**  
    Define primary tasks for casual workers, such as "Washing" or "Cleaning".
    -   Write activity type name and Save.
-   **Casual Activity Item:**  
    Link specific items/products to activity types. Set the cost per item manipulation (e.g., washing each item costs Ksh. 150).
    -   Choose the Activity Type
    -   Choose the Item
    -   Enter the cost
    -   Save

### 2. Daily Casual Payout

**Doctypes:**

-   **Attendance:**  
    Log daily attendance, including the type of shift worked.
    
-   **Casual Payroll Payout:**  
    Has two important tables.
    
    -   **Casual Payroll Payout Item:**
        -   Select the activity type
        -   Select Item worked on.
        -   The system will automatically fetch the rate set in the Casual Activity Item.
        -   Enter the quantity of items worked on that day.
        -   Total payout for all activities is calculated automatically.
    -   **Casual Payroll Payout Employee:**
        -   Choose the shift type and attendance date.
        -   Click on 'Get Employees' button.
        -   The system retrieves employees present during the specified shift and date.
        -   Click on 'Calculate Payout', the system then calculates the payout per employee. i.e Total Amount/Number of Employees fetched

### 3. Casual Salary Structure Assignment Tool

**Doctypes:**

-   **Casual Salary Structure Assignment Tool:**
    -   Specify the date range for attendance.
    -   Click "Calculate Payout" to sum the total amount earned by all casual workers during that period.
    -   Assign the appropriate salary structure for the specified timeframe.
    -   To ensure NSSF deductions, select the structure that includes NSSF contributions for the final week.
    -   Save and submit to automatically generate assignments for each employee, with the designated salary structure.

This system simplifies the process of calculating daily and weekly payouts for casual workers, ensuring accurate payroll processing and efficient management of salary structures.
### License

GNU General Public License (v3). See [license.txt](https://github.com/navariltd/CSF_KE/blob/master/license.txt) for more information.
