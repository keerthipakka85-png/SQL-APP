# InsightSQL - AI Powered Workforce Analytics Assistant

## 1. Executive Summary

InsightSQL is an AI-powered workforce analytics assistant that enables business stakeholders to ask questions about organizational data in plain English instead of writing SQL. The product translates natural-language questions into safe, read-only database queries, executes them against approved data sources, and presents understandable answers with supporting visualizations and query transparency.

The primary problem is an access gap: business stakeholders need timely answers from databases, but many do not have SQL expertise. This dependency on analysts and engineers creates delays, repeated requests, inconsistent definitions, and limited self-service decision-making.

The initial product will focus on trusted workforce analytics, including headcount, hiring, attrition, staffing trends, workforce composition, and related operational metrics. InsightSQL will prioritize correctness, data security, clear business definitions, and an auditable user experience over unrestricted query flexibility.

### Product Vision

Make trusted workforce insights available to every authorized stakeholder through a simple conversation with company data.

### MVP Scope

- Secure connection to approved relational data sources.
- Natural-language questions from authenticated users.
- AI-generated, read-only SQL.
- Query validation and permission enforcement before execution.
- Results displayed as summaries, tables, and suitable charts.
- Follow-up questions that preserve conversation context.
- Citations to source tables, fields, filters, and metric definitions.
- Feedback and audit logging for continuous improvement.

### Out of Scope for MVP

- Write, update, or delete operations.
- Autonomous changes to databases or HR systems.
- Unapproved data-source connections.
- Automated employment decisions or recommendations about individual employees.
- Replacing governed reporting for financial, legal, payroll, or regulatory filings.

## 2. Business Objectives

1. **Increase self-service access to data** by enabling non-technical stakeholders to answer common workforce questions without SQL support.
2. **Reduce time to insight** by shortening the path from a business question to a trusted answer.
3. **Reduce repetitive analytics requests** handled manually by data, HR, and engineering teams.
4. **Improve consistency of workforce metrics** through governed definitions, semantic metadata, and visible data provenance.
5. **Protect sensitive workforce information** through role-based access, row-level security, privacy controls, and read-only execution.
6. **Increase adoption of data-informed decisions** across HR, finance, operations, and executive teams.
7. **Create a measurable learning loop** through user feedback, failed-query analysis, and usage analytics.

### Suggested Success Metrics

- At least 70% of pilot users successfully answer a supported question without analyst assistance.
- Median time from question submission to answer is under 10 seconds for standard queries.
- At least 60% of common workforce analytics requests are resolved through self-service during the pilot.
- At least 90% of executed MVP queries pass automated safety and permission checks.
- At least 85% positive rating for answer usefulness among pilot users.
- Zero unauthorized access incidents involving workforce data.

## 3. Stakeholders

| Stakeholder | Role and Needs |
|---|---|
| Business stakeholders | Ask questions in English and receive fast, understandable answers without SQL knowledge. |
| HR and People Analytics | Analyze workforce trends using trusted definitions and reduce repetitive reporting work. |
| Executives and leaders | Monitor workforce health through concise summaries, trends, and drill-downs. |
| Finance and workforce planning | Compare headcount, hiring, attrition, and workforce costs where authorized. |
| Data analysts | Govern metrics, validate generated queries, investigate feedback, and support complex analysis. |
| Data engineering | Maintain connectors, schemas, performance, reliability, and query controls. |
| Security and privacy | Ensure least-privilege access, sensitive-data protection, monitoring, and compliance. |
| Legal and compliance | Review handling of employee data, retention, auditability, and regulated use cases. |
| IT and platform administrators | Configure identity, environments, data sources, roles, and operational policies. |
| Product and support teams | Define priorities, measure outcomes, and help users resolve issues. |

## 4. Functional Requirements

### 4.1 Identity and Access

- The system shall require authentication through the organization's approved identity provider.
- The system shall support role-based access control for administrators, analysts, and business users.
- The system shall enforce the user's existing database permissions and applicable row-level or column-level policies.
- The system shall prevent users from discovering or querying data sources, fields, or records they are not authorized to access.
- Administrators shall be able to deactivate access without deleting audit history.

### 4.2 Data Source and Metadata Management

- Administrators shall be able to configure approved read-only database connections.
- The system shall support the selected MVP relational database type through a secure connector.
- The system shall ingest or reference schema metadata, including tables, columns, relationships, data types, and descriptions.
- Authorized data stewards shall be able to define business metrics such as headcount, attrition rate, and active employee.
- Metric definitions shall include calculation logic, applicable filters, ownership, and last-reviewed date.
- The system shall identify sensitive fields and prevent their use unless explicitly approved.
- The system shall indicate metadata freshness and connector health.

### 4.3 Natural-Language Questioning

- Users shall be able to submit workforce questions in plain English.
- The system shall support common question patterns, including filtering, grouping, aggregation, comparison, ranking, time series, and trend analysis.
- The system shall interpret common date ranges such as last month, current quarter, year to date, and previous year.
- The system shall ask a clarifying question when the request is ambiguous, incomplete, or uses an undefined business term.
- Users shall be able to refine a question through follow-up prompts while retaining relevant conversation context.
- The system shall provide example questions based on the user's authorized data and role.
- The system shall clearly state when a question is unsupported or cannot be answered with available data.

### 4.4 Query Generation and Safety

- The system shall translate supported natural-language requests into SQL using approved schema and metric metadata.
- Generated SQL shall be read-only and shall not contain insert, update, delete, merge, drop, alter, truncate, grant, or equivalent mutation operations.
- The system shall validate generated SQL before execution for syntax, permissions, data access policy, excessive resource use, and injection risks.
- The system shall apply query timeouts, row limits, and resource limits appropriate to the environment.
- The system shall show the generated SQL to users with permission to view it; other users shall receive an appropriate transparency summary.
- The system shall not execute a query when validation fails.
- The system shall provide a useful, non-sensitive error message when generation or execution fails.
- The system shall support query cancellation for long-running requests.

### 4.5 Answer Presentation

- The system shall return a concise natural-language answer supported by the query result.
- The system shall display the underlying result set in a table when appropriate.
- The system shall select a suitable chart type for trends, comparisons, distributions, and rankings.
- Users shall be able to switch between summary, table, and chart views when the data supports those views.
- The answer shall show the time period, filters, aggregation, and relevant assumptions.
- The answer shall identify source tables, metric definitions, and data freshness where available.
- The system shall distinguish between zero, null, unavailable, and suppressed values.
- The system shall avoid presenting estimates as exact results.
- Users shall be able to export authorized results to a supported format such as CSV.

### 4.6 Conversation and Collaboration

- Users shall be able to view recent conversations and reopen them.
- Users shall be able to rename, archive, and delete their own conversations subject to retention policy.
- Users shall be able to share an answer only with users who are authorized to access the underlying data.
- Shared answers shall either re-run under the recipient's permissions or clearly indicate that access is unavailable.
- Users shall be able to provide positive, negative, and written feedback on an answer.
- Users shall be able to report incorrect data, incorrect interpretation, privacy concerns, or technical failures.

### 4.7 Administration and Governance

- Administrators shall be able to manage users, roles, data sources, sensitive fields, query limits, and retention settings.
- Data stewards shall be able to review and publish metric definitions.
- Administrators shall be able to inspect query, access, error, and feedback logs.
- The system shall support disabling individual prompts, metrics, tables, or data sources without taking down the entire product.
- The system shall provide usage reporting, including active users, question volume, success rate, latency, and feedback trends.

## 5. Non Functional Requirements

### Security and Privacy

- All data shall be encrypted in transit and at rest using organization-approved standards.
- Database credentials and API keys shall be stored in an approved secrets manager and shall never be exposed to end users or application logs.
- The application shall use least-privilege service accounts and read-only database access for MVP.
- Prompt, query, result, and audit logs shall be classified and retained according to organizational privacy policy.
- Sensitive employee data shall be masked, minimized, aggregated, or suppressed where required.
- The product shall provide controls to reduce the risk of prompt injection, SQL injection, data exfiltration, and unauthorized inference.
- Security events and access violations shall be logged and alertable.

### Accuracy and Trust

- The product shall use governed metadata and metric definitions as the preferred source for business terminology.
- Every answer shall be traceable to the executed query and its source data when permissions allow.
- The product shall communicate uncertainty, ambiguity, missing data, and stale data explicitly.
- Quality evaluation shall include a maintained test set of representative workforce questions.
- Human review shall be required before publishing new governed metrics or enabling high-risk data domains.

### Performance and Scalability

- Standard questions shall return an answer within 10 seconds at the 95th percentile under expected pilot load.
- The system shall provide progress or status feedback for requests that exceed the standard response time.
- The architecture shall support independent scaling of the user interface, orchestration layer, model calls, and query execution.
- Caching shall not bypass authorization and shall be invalidated according to data freshness requirements.

### Availability and Reliability

- The service shall target 99.5% monthly availability during the pilot, excluding approved maintenance.
- Failed model calls, connector failures, and database timeouts shall have controlled retries and graceful error handling.
- The system shall avoid duplicate query execution when a request is retried.
- Audit records shall be durable and protected from unauthorized modification.

### Usability and Accessibility

- A first-time user shall be able to submit a supported question without training or documentation.
- Answers shall use plain language and define technical terms when needed.
- The interface shall meet the organization's accessibility standard, targeting WCAG 2.1 AA.
- The experience shall support keyboard navigation, readable contrast, responsive layouts, and screen readers.
- The product shall make destructive or high-impact actions unavailable in the MVP rather than relying only on warnings.

### Maintainability and Observability

- Components shall have documented interfaces, configuration, deployment steps, and ownership.
- The system shall expose metrics for latency, failures, token or model usage, query performance, and authorization denials.
- Application logs shall be structured, correlated by request ID, and scrubbed of secrets and unnecessary personal data.
- Model prompts, model versions, schema versions, and generated SQL shall be versioned or identifiable for audit and debugging.

## 6. User Stories

1. As a business leader, I want to ask "How many active employees do we have by department?" so that I can understand current workforce distribution without writing SQL.
2. As an HR partner, I want to compare voluntary attrition this quarter with the same quarter last year so that I can identify meaningful changes.
3. As a workforce planner, I want to filter headcount by location, department, and employment type so that I can prepare planning scenarios.
4. As a non-technical user, I want the assistant to ask clarifying questions when my request is ambiguous so that I do not receive a misleading answer.
5. As a data analyst, I want to see the generated SQL, data sources, and metric definitions so that I can validate how an answer was produced.
6. As a data steward, I want to publish governed definitions for metrics so that users receive consistent answers to common questions.
7. As a security administrator, I want database permissions to apply to every generated query so that users cannot access unauthorized workforce data.
8. As a user, I want to ask a follow-up question such as "What about just Engineering?" so that I can explore results conversationally.
9. As an executive, I want concise summaries and charts so that I can understand a trend quickly.
10. As an analyst, I want to review failed or negatively rated questions so that I can improve metadata and supported use cases.
11. As a platform administrator, I want to configure read-only data sources and query limits so that the service is safe to operate.
12. As a privacy officer, I want audit logs and retention controls so that use of employee data can be reviewed and governed.

## 7. Acceptance Criteria

### Epic: Ask a Question

- Given an authenticated user with access to workforce data, when they submit a supported English question, then the system generates a read-only query and returns an answer, result table, or chart.
- Given a question that contains an ambiguous term or missing time period, when the system cannot determine a single valid interpretation, then it asks a clarifying question before execution.
- Given a question that cannot be answered from available data, when the user submits it, then the system explains the limitation and does not fabricate a result.

### Epic: Secure Query Execution

- Given a generated query, when validation detects a mutation statement, unauthorized field, unsafe operation, or resource violation, then the query is blocked and no database result is returned.
- Given two users with different permissions, when they submit the same question, then each receives only data authorized for their identity.
- Given a long-running query, when it exceeds the configured timeout, then execution stops and the user receives a recoverable error message.

### Epic: Trusted Answers

- Given a successful answer, when the result is displayed, then the response includes the period, filters, relevant metric definition, and data freshness when available.
- Given a null, zero, unavailable, or suppressed value, when the result is displayed, then the UI distinguishes the value state accurately.
- Given a user with SQL-view permission, when an answer is displayed, then the user can inspect the generated SQL and source metadata.

### Epic: Follow-Up Analysis

- Given a completed question, when the user asks a relevant follow-up, then the system retains the prior context and applies the new filter or comparison correctly.
- Given a follow-up that changes the subject or cannot be safely resolved from context, when it is submitted, then the system asks for clarification rather than assuming intent.

### Epic: Feedback and Governance

- Given an answer, when the user submits feedback, then the feedback is stored with the request ID, question, result status, and model or metadata version.
- Given an administrator, when they disable a data source or metric, then new requests cannot use it while existing audit history remains available.
- Given an authorized administrator, when they review audit logs, then they can identify the user, timestamp, data source, generated query, execution status, and access decision without exposing secrets.

### Epic: Usability and Accessibility

- Given a first-time user, when they open the product, then they can identify where to ask a question and submit one using keyboard navigation.
- Given a supported result, when it is displayed on desktop or mobile, then text, controls, tables, and charts remain readable without overlapping or losing essential information.
- Given a screen-reader user, when they navigate the question flow and answer, then controls and result states have meaningful accessible names and relationships.

## 8. Project Risks

| Risk | Impact | Likelihood | Mitigation |
|---|---|---:|---|
| Incorrect SQL or interpretation produces misleading answers | High | Medium | Governed metadata, validation, benchmark questions, citations, confidence and ambiguity handling, human review for high-risk metrics. |
| Unauthorized access to employee data | Very high | Low to medium | Identity-aware authorization, least privilege, row and column controls, read-only access, security testing, audit logs, privacy review. |
| Sensitive information is inferred from aggregate results | High | Medium | Minimum group-size thresholds, suppression, masking, restricted dimensions, privacy review, monitoring for repeated probing. |
| Inconsistent or unclear business definitions | High | High | Metric catalog, named owners, versioned definitions, freshness indicators, data steward approval. |
| Poor source data quality reduces trust | High | Medium | Data quality checks, visible freshness and limitations, source ownership, issue reporting, quality dashboards. |
| Query latency or database load affects production systems | Medium to high | Medium | Timeouts, row limits, query cost controls, replicas or governed warehouse, workload monitoring, caching with authorization checks. |
| Model or provider outage blocks the assistant | Medium | Medium | Provider abstraction, retries, fallback messaging, health monitoring, optional secondary model for approved workloads. |
| Users over-rely on AI answers for high-impact decisions | High | Medium | Clear usage policy, disclaimers for unsupported decisions, approval workflows for sensitive domains, human review requirements. |
| Low adoption because answers are not understandable | Medium | Medium | Usability testing, plain-language response design, examples, feedback loop, iterative prompt and metadata improvement. |
| Cost grows faster than usage value | Medium | Medium | Usage quotas, model routing, query/result caching, token monitoring, budget alerts, success metrics tied to business value. |
| Regulatory or contractual requirements change | High | Low to medium | Legal and compliance review, configurable retention and access controls, documented data-processing practices. |

## 9. Future Enhancements

### Near Term

- Support additional data warehouses and business applications.
- Add scheduled reports, subscriptions, and alerts for metric changes.
- Add saved questions, reusable dashboards, and team workspaces.
- Improve semantic search across data catalogs and documentation.
- Add multilingual question and answer support.
- Add richer exports and approved integrations with collaboration tools.

### Medium Term

- Enable controlled natural-language exploration across finance, sales, operations, and customer data.
- Add anomaly detection and explainable trend summaries.
- Support organization-specific synonyms, abbreviations, and terminology learning.
- Add data quality explanations and recommended remediation links.
- Add analyst review workflows for correcting generated SQL and promoting successful patterns.
- Add governed scenario analysis using approved snapshots or planning datasets.

### Long Term

- Provide proactive workforce insights based on user-configured objectives and thresholds.
- Support multimodal analysis of approved structured and unstructured sources.
- Offer a semantic metrics layer shared by InsightSQL and other reporting tools.
- Enable natural-language dashboard authoring with version control and approval workflows.
- Add fine-grained privacy-preserving analytics for small groups and sensitive workforce domains.
- Support secure, human-approved actions in connected systems only after governance, audit, and risk controls are established.

## Product Decisions and Open Questions

- Which relational database or warehouse is the first supported source?
- Which workforce metrics and data domains are approved for the pilot?
- What minimum group size is required before an aggregate result can be shown?
- Which roles may inspect generated SQL and detailed source metadata?
- Which identity provider, secrets manager, model provider, and deployment environment are required?
- What retention period applies to prompts, generated SQL, results, and audit logs?
- Which questions are explicitly prohibited because they could influence employment decisions or expose sensitive personal information?
- Who owns approval and ongoing maintenance of each governed metric?

## MVP Definition of Done

The MVP is ready for pilot when authenticated users can ask approved workforce questions in English, receive accurate and understandable answers, inspect supporting provenance where authorized, and receive only data permitted by their role. All executed queries are read-only, validated, bounded, observable, and auditable; pilot success metrics are measurable; and security, privacy, and data-governance stakeholders have approved the enabled data domains.
