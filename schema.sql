PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    location TEXT
);

CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    manager_id INTEGER,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    job_title TEXT NOT NULL,
    hire_date TEXT NOT NULL CHECK (date(hire_date) IS NOT NULL),
    salary REAL NOT NULL CHECK (salary >= 0),
    employment_status TEXT NOT NULL DEFAULT 'Active'
        CHECK (employment_status IN ('Active', 'On Leave', 'Inactive')),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id)
        ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    department_id INTEGER NOT NULL,
    project_name TEXT NOT NULL UNIQUE,
    description TEXT,
    start_date TEXT NOT NULL CHECK (date(start_date) IS NOT NULL),
    end_date TEXT,
    budget REAL NOT NULL CHECK (budget >= 0),
    project_status TEXT NOT NULL DEFAULT 'Planned'
        CHECK (project_status IN ('Planned', 'Active', 'Completed', 'On Hold')),
    CHECK (end_date IS NULL OR date(end_date) IS NOT NULL),
    CHECK (end_date IS NULL OR date(end_date) >= date(start_date)),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS employee_projects (
    employee_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    project_role TEXT NOT NULL,
    assigned_date TEXT NOT NULL CHECK (date(assigned_date) IS NOT NULL),
    allocation_pct REAL NOT NULL CHECK (allocation_pct > 0 AND allocation_pct <= 100),
    PRIMARY KEY (employee_id, project_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_employees_department_id
    ON employees(department_id);

CREATE INDEX IF NOT EXISTS idx_employees_manager_id
    ON employees(manager_id);

CREATE INDEX IF NOT EXISTS idx_projects_department_id
    ON projects(department_id);

CREATE INDEX IF NOT EXISTS idx_employee_projects_project_id
    ON employee_projects(project_id);
