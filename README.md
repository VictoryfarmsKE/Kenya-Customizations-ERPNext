# EXPNext Country Specific Functionality for Kenya

## Includes:

## Kenya Payroll Reports
• P9A Tax Deduction Card, P10 Tax Report, NSSF Report, NHIF Report, HELB Report, Bank Payroll Advice Report, and Payroll Register Report

## Sales and Purchase Tax Reports
• Sales Tax Report and Purchase Tax Report

## Casual Payroll Customization
The Casual Payroll System streamlines the management of casual workers' payments by providing tools for setting up activity types and linking them to specific items/products. It includes functionalities for daily attendance logging, calculating daily payouts based on attended activities, and assigning salary structures for specified timeframes. With automated rate fetching and payout calculations, this system ensures accurate and efficient payroll processing for casual workers.
### 1. Set-Up

**Doctypes:**

-   **Activity Type:**
        ![Screenshot from 2024-04-28 07-40-42](https://github.com/navariltd/navari_csf_ke/assets/60258622/7e9a53c0-347c-452f-87bd-546934a455a1)

    Define primary tasks for casual workers, such as "Washing" or "Cleaning".
    -   Write activity type name and Save.
-   **Casual Activity Item:**
         ![Screenshot from 2024-04-28 08-58-46](https://github.com/navariltd/navari_csf_ke/assets/60258622/36ca612f-1e12-4f22-bd81-45a732d9665e)

      Link specific items/products to activity types. Set the cost per item manipulation (e.g., washing each NETM-001 costs Ksh. 150).<br/>


    - Choose the Activity Type
    -    Choose the Item
    -    Enter the cost
    -    Save
      
### 2. Daily Casual Payout

**Doctypes:**

-   **Attendance:**  
    Log daily attendance, including the type of shift worked.
    
-   **Casual Payroll Payout:**
![image (1)](https://github.com/navariltd/navari_csf_ke/assets/60258622/ed9bbeea-997e-41af-a462-48e3e2d87239)
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


![image (2)](https://github.com/navariltd/navari_csf_ke/assets/60258622/7fa5d17e-1ca2-475d-937c-c5580637c9cc)
**Doctypes:**

-   **Casual Salary Structure Assignment Tool:**
    -   Specify the date range for attendance.
    -   Click "Calculate Payout" to sum the total amount earned by all casual workers during that period.
    -   Assign the appropriate salary structure for the specified timeframe.
    -   To ensure NSSF deductions, select the structure that includes NSSF contributions for the final week.
    -   Save and submit to automatically generate salary structure assignments for each employee, with the designated salary structure.

This system simplifies the process of calculating daily and weekly payouts for casual workers, ensuring accurate payroll processing and efficient management of salary structures.

##### Timesheet Center
---
<a id="Timesheet_Center"></a>
There is usually an attempt (every hour) to create overtime timesheets, from an employee's attendance records.<br>

Overtime is marked in two scenarios:
1. Additional time (more than 30 minutes) past an employee's shift end time. (Overtime 1.5)
2. An attendance record appearing on a day that is also on an employee's holiday list. (overtime 2.0)

Even though the overtime timesheets are created automatically, there may be scenarios where we would want to do this manually. Hence the ***Timesheet Center*** doctype.<br> 
![Screenshot from 2024-05-17 14-56-26](https://github.com/navariltd/navari_csf_ke/assets/60260520/9f41ec51-06ba-4f5f-a800-93bec9961f9a)
Select the *Start Date* and *End Date* for which you want to generate the overtime timesheets.<br>
Save the document.<br>
Click on the *Generate Timesheets* button.<br>
**NB:** Timesheet Center is a [Single Doctype](https://frappeframework.com/docs/user/en/basics/doctypes/single-doctype)

### 4. Payroll
<a id="Payroll"></a>
The doctype below, *Navari Custom Payroll Settings* is important while linking attendance data to payroll. <br>

##### Navari Custom Payroll Settings
---
<a id="Navari_Custom_Payroll_Settings"></a>
As the name suggests, settings related to payroll are stored here.


![Screenshot from 2024-05-17 15-12-44](https://github.com/navariltd/navari_csf_ke/assets/60260520/4e473d4f-c225-429e-bc14-fa36dbc75ed5)

1. *Maximum monthly hours:* The maximum number of hours beyond which, the rest is carried over to overtime while creating employee salary slips.
2. *Overtime 1.5 Activity:* Overtime 1.5 is what the employee gets for working past their shift time, on a regular day. We tag the activity set here while creating timesheets for overtime 1.5
3. *Overtime 2.0 Activity:* Overtime 2.0 is what the employeee gets for working on a day that appears on their holiday list. We tag the activity set here while creating timesheets for overtime 2.0
4. *Include early entry:* When checked, hours before shift start time will be considered while making employee salary slips. When uncheked, working hours will be calculated from the shift start time while making salary slips, doesn't matter if an employee checked in earlier for their shift.

**NB:** *Overtime 1.5 Activity* and *Overtime 2.0 Activity* should be different so as to differentiate between the two types of overtime.

## How attendance is matched to payroll
<a id="how_attendance_is_matched_to_payroll"></a>
This is how payroll works on ERPNext:
1. Create an [employee.](https://frappehr.com/docs/v14/en/employee)
2. Create [salary components.](https://frappehr.com/docs/v14/en/salary-component)
3. Create a [salary structure.](https://frappehr.com/docs/v14/en/salary-structure)
4. Create a [salary structure assignment](https://frappehr.com/docs/v14/en/salary-structure-assignment) for each employee.
5. Create a [payroll entry](https://frappehr.com/docs/v14/en/payroll-entry) and generate [salary slips](https://frappehr.com/docs/v14/en/salary-slip) for each employee.

### Steps for Payroll Generation
With the biostar TA API integration, there are a few other things that happen, adding a few more steps while generating salary slips for employees who are paid per hour.
1. Checkin/Checkout logs are fetched from the biostar server and created under [employee checkin](https://frappehr.com/docs/v14/en/employee_checkin), after every hour. Please note that [biostar settings](#Biostar_Settings) need to be configured correctly for this to happen. Also, the *Attendance Device ID (Biometric/RF tag ID)* needs to be set for employees whose checkin/checkout data needs to be fetched from biostar server.
![Screenshot from 2024-05-17 15-18-07](https://github.com/navariltd/navari_csf_ke/assets/60260520/4322df73-e3f2-469c-b016-d83533539a6d)
2. Attendance is marked as per the shifts assigned to each employee. This happens automatically for every shift type with *Enable Auto Attendance* checked.
![Screenshot from 2024-05-17 15-18-48](https://github.com/navariltd/navari_csf_ke/assets/60260520/87badc65-79f3-4f12-9810-5991858f7d01)
3. Overtime timesheets are generated, from the attendance data. Happens automatically, one can also choose to generate these manually from the [timesheet center.](#Timesheet_Center)
![Screenshot from 2024-05-17 15-19-19](https://github.com/navariltd/navari_csf_ke/assets/60260520/8bf63740-7111-4d69-a9ba-031806dd3f5b)
4. Timesheets need to be submitted for them to be considered when running payroll.

***On the few changes to the payroll process:***
1. Make sure to assign an *Attendance Device ID (Biometric/RF tag ID)* to every employee whose checkin/checkout data we need to fetch from biostar server.
2. When creating a salary structure for employees who are based per hour, make sure to check the *Wage based salary (hours)* field, and fill the *Hour Rate* and *Salary Component* fields.
![Screenshot from 2024-05-17 22-27-21](https://github.com/navariltd/navari_csf_ke/assets/60260520/b09aeeae-ecf9-4542-a2f5-e8c99cd2cbff)
3. When running payroll on payroll entry, after generating salary slips, attendance data is fetched and added to employees attendance in the salary slips. Attendance data will be picked from [attendance](https://frappehr.com/docs/v14/en/attendance) and timesheet records generated over that payroll period.
4. Attendance data will be added to the *Attendance Details* tab on a salary slip.
![Screenshot from 2024-05-17 22-31-11](https://github.com/navariltd/navari_csf_ke/assets/60260520/44c3fd26-c789-4aac-871b-376db5051f16)

<br>
*1. Attendance:* Picked from an employee's attendance records over that payroll period<br>
> *Payment Hours* - this is a custom field in attendance doctype which accurately captures total shift hours, excluding unpaid breaks if any and overtime. It is captured as billable hours in Attendance Details in Salary Slip.<br>

*2. Overtime 1.5:* Picked from timesheet records, timesheets with the activity type set as *Overtime 1.5 Activity* on *VF Payroll Settings*<br>
*3. Overtime 2.0:* Picked from timesheet records, timesheets with the activity type set as *Overtime 2.0 Activity* on *VF Payroll Settings*<br>
*4. Regular Working Hours:* Sum of *Billiable Hours* from the *Attendance* table. Hours beyond what is set as *Maximum monthly hours* on *VF Payroll Settings* are carried over to the *Overtime Hours* field.<br>
*5. Overtime Hours:* Sum of hours from *Overtime 1.5* table plus what has been carried over from *Regular Working Hours*, incase there is anything to carry over.<br>
*6. Holiday hours:* Sum of hours from *Overtime 2.0* table.<br>
*7. Hourly Rate:* Fetched from the salary structure assigned to an employee. Used to calculate basic and overtime pay (Both regular and holiday overtime)<br>
See salary structure below:
![Screenshot from 2024-05-17 22-34-31](https://github.com/navariltd/navari_csf_ke/assets/60260520/fcc6c265-efb6-425e-9c26-ddb0a348c55b)

```Basic salary = (hourly_rate * regular_working_hours)``` <br>
```OT hours = hourly_rate * 1.5 * overtime_hours``` <br>
```Holiday Hours = hourly_rate * 2 * holiday_hours```<br>
*NB: OT here refers to regular overtime*<br>
See how the hours from the above screenshots reflect on earnings and deductions:
![Screenshot from 2024-05-17 22-49-36](https://github.com/navariltd/navari_csf_ke/assets/60260520/1d0c770f-de32-451c-b1e8-704330bfe398)



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

