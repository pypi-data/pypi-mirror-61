mds-employee-timetracking
=========================
Working time recording for employees, with multiple time accounts, 
time account rules, automatic pause control and report.

Install
=======

pip install mds-employee-timetracking

Requires
========
- Tryton 5.0

HowTo
=====

For more information, read the files in the doc folder.

ToDo
====
- extend manual
- support for NFC door device

Changes
=======

*5.0.24 - 18.02.2020*

- fix: translations

*5.0.23 - 07.10.2019*

- fix: generate a valid calendar name in the Employees Wizard

*5.0.22 - 12.09.2019*

- upd: optimized selection of open presence-time by wizard
- upd: presence-times - workflow now allows: examine->editable
- fix: open presence-times appear in correct month
- fix: permissions for role working-time-admin

*5.0.21 - 06.09.2019*

- fix: permissions for employee to edit its sick days

*5.0.20 - 05.09.2019*

- add: employee can enter its sick days

*5.0.19 - 03.09.2019*

- add: new role 'Employee edit its start balance'

*5.0.18 - 02.09.2019*

- add: account rule extended - 
   applies on public holidays / not on public holidays / not set

*5.0.17 - 30.08.2019*

- fix: exception when deleting the start position of a period with 
   the existing end position

*5.0.16 - 14.08.2019*

- add: initial balance of a time account can be set manually

*5.0.15 - 19.07.2019*

- updt: field placement in employee wizard optimized
- fix: exception when accessing overlap calculation

*5.0.14 - 25.04.2019*

- new: config wizard

*5.0.13 - 18.04.2019*

- fix: calculation of remainig vacation days

*5.0.12 - 15.04.2019*

- new: holiday planning (new depency to mds-pim-calendar)

*5.0.11 - 14.02.2019*

- new: calendar view in evaluation + presence period + break time
- new: colors of background/text in calendar view selectable 
   for employee + type of presence, time account...
- info: GooCalendar on client side is neccasary

*5.0.10 - 11.02.2019*

- new: Attendance wizard extended, employee can enter his break times
- fix: report causes exception

*5.0.9 - 30.01.2019*

- fix: edit employee also corrects the associated company on the cronjob
- updt: optimized tests
- new: Time Entry Wizard accepts any number of Presence Types

*5.0.8 - 17.01.2019*

- checked compatibility to Tryton 5.0
