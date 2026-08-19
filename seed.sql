PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

INSERT OR IGNORE INTO departments (department_id, department_name, location) VALUES
    (1, 'Engineering', 'Seattle'),
    (2, 'Human Resources', 'New York'),
    (3, 'Finance', 'Chicago'),
    (4, 'Sales', 'Austin'),
    (5, 'Operations', 'Denver');

INSERT OR IGNORE INTO employees
    (employee_id, department_id, manager_id, first_name, last_name, email, job_title, hire_date, salary, employment_status)
VALUES
    (1, 1, NULL, 'Ava', 'Thompson', 'ava.thompson@example.com', 'VP of Engineering', '2018-03-12', 185000, 'Active'),
    (2, 1, 1, 'Liam', 'Carter', 'liam.carter@example.com', 'Engineering Manager', '2019-07-08', 145000, 'Active'),
    (3, 1, 2, 'Mia', 'Rodriguez', 'mia.rodriguez@example.com', 'Senior Software Engineer', '2020-01-20', 132000, 'Active'),
    (4, 1, 2, 'Noah', 'Patel', 'noah.patel@example.com', 'Software Engineer', '2021-05-17', 112000, 'Active'),
    (5, 1, 2, 'Emma', 'Wilson', 'emma.wilson@example.com', 'QA Engineer', '2022-09-01', 98000, 'On Leave'),
    (6, 2, NULL, 'Olivia', 'Bennett', 'olivia.bennett@example.com', 'Chief People Officer', '2017-11-06', 178000, 'Active'),
    (7, 2, 6, 'Ethan', 'Nguyen', 'ethan.nguyen@example.com', 'HR Business Partner', '2020-06-15', 108000, 'Active'),
    (8, 2, 6, 'Sophia', 'Kim', 'sophia.kim@example.com', 'Recruiting Manager', '2019-02-25', 118000, 'Active'),
    (9, 2, 8, 'Lucas', 'Martin', 'lucas.martin@example.com', 'Technical Recruiter', '2023-01-09', 82000, 'Active'),
    (10, 3, NULL, 'Isabella', 'Moore', 'isabella.moore@example.com', 'Chief Financial Officer', '2016-08-22', 195000, 'Active'),
    (11, 3, 10, 'James', 'Lee', 'james.lee@example.com', 'Finance Manager', '2018-10-01', 128000, 'Active'),
    (12, 3, 11, 'Amelia', 'Davis', 'amelia.davis@example.com', 'Financial Analyst', '2021-03-29', 92000, 'Active'),
    (13, 3, 11, 'Benjamin', 'Clark', 'benjamin.clark@example.com', 'Senior Accountant', '2019-12-02', 101000, 'Inactive'),
    (14, 4, NULL, 'Charlotte', 'Lewis', 'charlotte.lewis@example.com', 'Chief Revenue Officer', '2017-04-10', 180000, 'Active'),
    (15, 4, 14, 'Henry', 'Walker', 'henry.walker@example.com', 'Sales Director', '2018-06-18', 135000, 'Active'),
    (16, 4, 15, 'Evelyn', 'Hall', 'evelyn.hall@example.com', 'Account Executive', '2022-02-14', 87000, 'Active'),
    (17, 4, 15, 'Alexander', 'Young', 'alexander.young@example.com', 'Sales Operations Analyst', '2021-08-30', 90000, 'Active'),
    (18, 5, NULL, 'Harper', 'Allen', 'harper.allen@example.com', 'Chief Operating Officer', '2016-01-11', 190000, 'Active'),
    (19, 5, 18, 'Daniel', 'King', 'daniel.king@example.com', 'Operations Manager', '2019-09-23', 122000, 'Active'),
    (20, 5, 19, 'Ella', 'Wright', 'ella.wright@example.com', 'Workforce Analyst', '2023-04-03', 79000, 'Active');

INSERT OR IGNORE INTO projects
    (project_id, department_id, project_name, description, start_date, end_date, budget, project_status)
VALUES
    (1, 1, 'Analytics Platform Modernization', 'Modernize the internal analytics platform.', '2024-01-15', NULL, 450000, 'Active'),
    (2, 1, 'Identity Access Upgrade', 'Improve authentication and access controls.', '2024-04-01', '2024-12-20', 180000, 'Completed'),
    (3, 2, 'Employee Experience Survey', 'Launch and analyze the annual engagement survey.', '2025-01-06', NULL, 75000, 'Active'),
    (4, 2, 'Leadership Development Program', 'Create a leadership development curriculum.', '2025-03-10', NULL, 120000, 'Planned'),
    (5, 3, 'Annual Planning Automation', 'Automate the annual budgeting workflow.', '2024-07-08', NULL, 210000, 'Active'),
    (6, 3, 'Expense Policy Refresh', 'Review and implement updated expense controls.', '2024-02-12', '2024-08-30', 60000, 'Completed'),
    (7, 4, 'Customer Growth Initiative', 'Improve pipeline generation and conversion.', '2025-02-03', NULL, 300000, 'Active'),
    (8, 4, 'Sales Enablement Portal', 'Centralize sales training and collateral.', '2025-05-19', NULL, 145000, 'On Hold'),
    (9, 5, 'Workforce Planning Program', 'Create a repeatable workforce planning process.', '2024-09-16', NULL, 250000, 'Active'),
    (10, 5, 'Operations Efficiency Review', 'Identify and implement process improvements.', '2024-03-04', '2025-01-31', 160000, 'Completed');

INSERT OR IGNORE INTO employee_projects
    (employee_id, project_id, project_role, assigned_date, allocation_pct)
VALUES
    (1, 1, 'Executive Sponsor', '2024-01-15', 10),
    (2, 1, 'Engineering Lead', '2024-01-15', 35),
    (3, 1, 'Senior Developer', '2024-01-22', 60),
    (4, 1, 'Developer', '2024-02-05', 50),
    (5, 1, 'QA Lead', '2024-02-05', 40),
    (3, 2, 'Technical Lead', '2024-04-01', 25),
    (4, 2, 'Developer', '2024-04-01', 30),
    (6, 3, 'Executive Sponsor', '2025-01-06', 15),
    (7, 3, 'Program Partner', '2025-01-06', 45),
    (8, 3, 'Recruiting Contributor', '2025-01-13', 20),
    (8, 4, 'Program Lead', '2025-03-10', 40),
    (9, 4, 'Program Coordinator', '2025-03-10', 35),
    (10, 5, 'Executive Sponsor', '2024-07-08', 10),
    (11, 5, 'Finance Lead', '2024-07-08', 45),
    (12, 5, 'Analyst', '2024-07-15', 60),
    (13, 6, 'Accounting Lead', '2024-02-12', 40),
    (14, 7, 'Executive Sponsor', '2025-02-03', 10),
    (15, 7, 'Sales Lead', '2025-02-03', 45),
    (16, 7, 'Account Executive', '2025-02-10', 50),
    (17, 7, 'Operations Analyst', '2025-02-10', 30),
    (18, 9, 'Executive Sponsor', '2024-09-16', 10),
    (19, 9, 'Program Lead', '2024-09-16', 50),
    (20, 9, 'Workforce Analyst', '2024-09-23', 70),
    (19, 10, 'Operations Lead', '2024-03-04', 40),
    (20, 10, 'Process Analyst', '2024-03-11', 50);

COMMIT;
