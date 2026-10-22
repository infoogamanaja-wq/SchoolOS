# Feature and integration map

## Teacher Portal — 17 areas

| Requested feature | Implemented workflow |
|---|---|
| Assigned classes | Current-session class/subject allocations and a scoped student roster; portal account IDs drive permissions. |
| Attendance | Save daily present/absent/late/excused records directly to the existing school register; unrelated classes rejected. |
| Timetable | Current timetable by allocated class/subject and teacher, with school session and local times. School admin manages schedules in Academics. |
| Lesson plans | Save draft/delivered plans against allocated curriculum topics; delivered homework reaches the existing family view. |
| Syllabus progress | Update allocated topics between planned, in progress and completed. |
| Assignments | Create/publish owned courses and activities, deadlines, resources; read submissions/attachments and record marks and feedback. |
| Question banks | Author MCQ, True/False, short-answer and essay items in owned draft banks; school administrators publish/mark CBT. |
| Score entry | Save draft marks against allocated existing assessments, then submit for school moderation. |
| Bulk uploads | Validate, preview and atomically confirm assessment-score CSV imports; no partial writes. |
| Corrections | Request a recorded score change; a different school administrator reviews unpublished corrections and sends them for fresh moderation. Published results stay locked. |
| Performance analytics | Recorded learner counts, mean raw marks and minimum/maximum for each allocated assessment. These are descriptive raw-score summaries, not predictive analytics or full-term weighted rankings. |
| Parent messaging | Message explicitly linked parents and reply to assigned parent messages through the existing Family Space message records. |
| Teaching resources | Share HTTPS learning links and notes with allocated classes/subjects. |
| Incidents | Report confidential factual incidents for allocated students to the existing Welfare case workflow; teachers see their own reports. |
| Leave | Request personal leave and view status; school admin reviews using existing Welfare leave records. |
| Professional development | Record training, provider, completion date, hours and optional HTTPS evidence; school review status is retained. |
| AI lesson assistance | Optional school-enabled provider integration for age-appropriate lesson drafts, with moderation, quotas and teacher review. Needs the school's key/network. |

## Student Portal — 14 areas

| Requested feature | Implemented workflow |
|---|---|
| Dashboard | Own identity/class, published-course count, recorded present days and planned study tasks. |
| Timetable | Current class schedule with subjects/rooms/local times. |
| Homework | Delivered academic homework plus available LMS assignments; text/validated attachment submission, deadlines and graded-work locks. |
| Learning resources | Published class courses, learning activities and shared HTTPS academic resources; completion tracking. |
| CBT | Published class exams, access codes/windows, explicit save/resume, immutable submission, timing/attempt locks, published results. |
| Grades | Own published legacy results and approved academic scores only after term publication. |
| Attendance | Own daily and period attendance. |
| Teacher feedback | Own graded assignment marks and teacher feedback. |
| Announcements | Audience-filtered Community Hub posts; school/class/student/person scopes are respected. |
| Clubs | Eligible club list and membership requests; school approval and capacity controls. |
| Library | Tenant catalogue, loan requests and own issue/due/return history; inventory controlled by school review. |
| Badges | Existing LMS badges awarded to this student's record by an authorised teacher. |
| Study planner | Private dated study tasks and completion, scoped to account and linked student. |
| Safeguarded AI study support | Optional moderated explanation/practice/hint assistance with school enablement, quotas, identifier filtering and active-exam blocks. No automatic grades or record access. |

## Preserved integrations and data

Finance, the working Parent & Guardian Portal, WhatsApp handoff, Community Hub, authentication and database credentials are not replaced. Teacher/student links use `ecosystem_links`; the older CBT/LMS lookup of `ecosystem_portal_links` is corrected. Existing Academics/LMS/CBT/Attendance/Welfare tables supply the workflows. Eight additive `lp_*` tables store corrections, development, clubs, membership, library loans, planning and AI controls/usage.

Student and teacher dashboard/menu links now open their functional portal instead of the old ecosystem summary. Old LMS submission forms pass through the new grade/deadline guards; teacher/student legacy welfare mutations are denied so they cannot bypass allocation checks. Legacy attachment access resolves current identity/allocation. Community Hub class audiences now follow current teacher allocations and explicit canonical student identity; existing parent audiences remain intact.

The release changes the index/router, adds learning_portal.php, expands the updater whitelist and records a new version. It does not ship config.php, database data/SQL dumps, uploads, .htaccess changes, installer changes, deletion rules or a replacement Finance/Parent module. Existing schema activation remains explicit rather than running during a ZIP upload.
