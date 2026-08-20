import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas for adding page numbers 'Page X of Y' and professional headers/footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        if self._pageNumber > 1:
            # Header
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#0284C7")) # Blue
            self.drawString(54, letter[1] - 36, "FINTRACK PRO")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B")) # Slate
            self.drawString(125, letter[1] - 36, "|   System Architecture, Engineering Blueprint & Interview Mastery Guide")
            
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 45, letter[0] - 54, 45)

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(54, 32, "Confidential — Engineering Preparation & Project Architecture Document")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.restoreState()


def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0F172A") # Deep Slate Navy
    accent_blue = colors.HexColor("#0284C7")   # Sky Blue / Cyan
    accent_green = colors.HexColor("#059669")  # Emerald
    accent_amber = colors.HexColor("#D97706")  # Amber
    accent_red = colors.HexColor("#DC2626")    # Red
    dark_text = colors.HexColor("#1E293B")
    muted_text = colors.HexColor("#475569")
    card_bg = colors.HexColor("#F8FAFC")
    border_color = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=14
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=muted_text
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=dark_text,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1E293B")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=dark_text
    )

    story = []

    # ==================== COVER / HEADER BLOCK ====================
    story.append(Paragraph("FINTRACK PRO", title_style))
    story.append(Paragraph("Full Architecture Blueprint, Engineering Workflows & Interview Mastery Guide", subtitle_style))
    
    meta_text = """
    <b>Stack:</b> MongoDB &bull; Express.js &bull; React 18 &bull; Node.js (MERN) &bull; Tailwind CSS &bull; Chart.js &bull; Docker<br/>
    <b>Domain:</b> Automated Personal Finance Management, Real-Time Budgeting & Scheduled Analytics<br/>
    <b>Document Scope:</b> Architectural Breakdown, Directory Map, End-to-End Workflows, Tech Selection Rationale, and Interview Strategy.
    """
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=4, spaceAfter=14))

    # ==================== SECTION 1 ====================
    story.append(Paragraph("1. Executive Summary & Core Motivation (\"Why I Made It\")", h1_style))
    
    p1 = """
    <b>The Real-World Problem:</b> Personal financial tracking suffers from severe user drop-off. Traditional budgeting apps and spreadsheets are <i>passive</i>—they require tedious manual data entry and offer zero proactive intervention. Users often realize they overspent only at the end of the month when it is too late to adjust habits.
    """
    story.append(Paragraph(p1, body_style))

    p2 = """
    <b>The FinTrack Pro Solution:</b> FinTrack Pro was engineered as an <i>active financial co-pilot</i>. Beyond standard transaction logging, it provides:
    """
    story.append(Paragraph(p2, body_style))

    story.append(Paragraph("&bull; <b>Real-Time Threshold Alerts:</b> Automatically evaluates period expenditures after every logged expense and triggers instant email alerts at <b>80% (Warning)</b> and <b>100% (Breach)</b> thresholds.", bullet_style))
    story.append(Paragraph("&bull; <b>Decoupled Background Automation:</b> A localized cron scheduler (<code>node-cron</code> + <code>moment-timezone</code>) generates and sends structured daily expense digests and monthly reviews.", bullet_style))
    story.append(Paragraph("&bull; <b>High-Performance Native Analytics:</b> MongoDB aggregation pipelines process category distributions and daily trends directly in the database engine.", bullet_style))
    story.append(Paragraph("&bull; <b>Modern, Responsive UX:</b> Built with React 18, Tailwind CSS, Chart.js, and Framer Motion with full light/dark theme adaptation.", bullet_style))
    
    story.append(Spacer(1, 8))

    # Pitch Box Table
    pitch_data = [
        [
            Paragraph("<b>🎙️ 30-Second Elevator Pitch (Ready-to-Use in Interviews):</b><br/>"
                      "<i>\"FinTrack Pro is a full-stack personal finance tracker built on the MERN stack with automated background intelligence. Unlike passive spreadsheets, it actively protects user budgets by executing real-time threshold evaluations on every expense—triggering instant email alerts at 80% and 100% caps—while running timezone-aware midnight cron jobs to deliver daily spending digests and monthly reviews directly to user inboxes.\"</i>", callout_style)
        ]
    ]
    pitch_table = Table(pitch_data, colWidths=[letter[0]-108])
    pitch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(pitch_table)

    story.append(Spacer(1, 14))

    # ==================== SECTION 2 ====================
    story.append(Paragraph("2. System Architecture & Component Interaction", h1_style))
    
    arch_desc = """
    The application follows a decoupled 3-Tier Architecture designed for scalability, data isolation, and low-latency client rendering.
    """
    story.append(Paragraph(arch_desc, body_style))

    # Architecture Diagram Table
    arch_flow = [
        [Paragraph("<b>TIER</b>", table_header_style), Paragraph("<b>COMPONENTS & RESPONSIBILITIES</b>", table_header_style), Paragraph("<b>KEY TECHNOLOGIES</b>", table_header_style)],
        [
            Paragraph("<b>Client Tier<br/>(Frontend SPA)</b>", table_cell_bold),
            Paragraph("&bull; <b>Views:</b> Dashboard, Ledger, Budgets, Goals, Profile, Auth<br/>"
                      "&bull; <b>State:</b> AuthContext (JWT/user), ThemeContext (light/dark)<br/>"
                      "&bull; <b>Network:</b> Axios Client with Request (Bearer Token) & Response (401 catch) Interceptors<br/>"
                      "&bull; <b>Visuals:</b> Chart.js canvas rendering & Framer Motion transitions", table_cell_style),
            Paragraph("React 18<br/>Tailwind CSS<br/>Axios<br/>Chart.js<br/>Formik + Yup", table_cell_style)
        ],
        [
            Paragraph("<b>API Tier<br/>(Express Backend)</b>", table_cell_bold),
            Paragraph("&bull; <b>Routing & Auth:</b> Passport-JWT Strategy & Middleware<br/>"
                      "&bull; <b>Controllers:</b> Analytics, Auth, Budget, Goal, Transaction, User<br/>"
                      "&bull; <b>Error Interceptor:</b> Centralized Mongoose error handler<br/>"
                      "&bull; <b>Services:</b> Nodemailer email dispatcher & node-cron background task scheduler", table_cell_style),
            Paragraph("Node.js (ESM)<br/>Express.js<br/>Passport.js<br/>Nodemailer<br/>Node-Cron", table_cell_style)
        ],
        [
            Paragraph("<b>Data Tier<br/>(MongoDB)</b>", table_cell_bold),
            Paragraph("&bull; <b>Collections:</b> Users, Transactions, Budgets, Goals, Categories<br/>"
                      "&bull; <b>Indexes:</b> Compound indexes on <code>(user, date)</code> and <code>(user, type)</code><br/>"
                      "&bull; <b>Pipelines:</b> Aggregation engine for sums, groups, and lookups", table_cell_style),
            Paragraph("MongoDB Atlas / Local<br/>Mongoose ODM", table_cell_style)
        ]
    ]

    t_arch = Table(arch_flow, colWidths=[100, 270, 134])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # ==================== SECTION 3 ====================
    story.append(Paragraph("3. Detailed Project Structure & File Directory Map", h1_style))
    story.append(Paragraph("FinTrack Pro is organized under a clean, modular repository layout separating client and server concerns:", body_style))

    file_data = [
        [Paragraph("<b>DIRECTORY / FILE</b>", table_header_style), Paragraph("<b>PRIMARY RESPONSIBILITY & INTERNAL IMPLEMENTATION</b>", table_header_style)],
        [
            Paragraph("<code>server/server.js</code>", table_cell_bold),
            Paragraph("Entry point: Mounts CORS, body-parser, Passport, DB connection, API routes, error handlers, and kicks off the cron scheduler.", table_cell_style)
        ],
        [
            Paragraph("<code>server/controllers/</code>", table_cell_bold),
            Paragraph("<b>analytics.controller.js:</b> MongoDB aggregation pipelines for charts & dashboard stats.<br/>"
                      "<b>transaction.controller.js:</b> Transaction CRUD, filters, and budget breach hook.<br/>"
                      "<b>budget.controller.js:</b> Budget management and live spent calculation.<br/>"
                      "<b>goal.controller.js:</b> Goal milestones and contribution updates.<br/>"
                      "<b>auth.controller.js:</b> User registration, login, and password resets.", table_cell_style)
        ],
        [
            Paragraph("<code>server/models/</code>", table_cell_bold),
            Paragraph("<b>User.model.js:</b> User schema, bcrypt hash hook, email preferences.<br/>"
                      "<b>Transaction.model.js:</b> Type (income/expense), amount, category, date (indexed).<br/>"
                      "<b>Budget.model.js:</b> Category-specific/global limits, periods, notification toggles.<br/>"
                      "<b>Goal.model.js:</b> Target amounts, current amount, virtual progress getter.<br/>"
                      "<b>Category.model.js:</b> Predefined vs custom categories, icons, colors.", table_cell_style)
        ],
        [
            Paragraph("<code>server/services/</code>", table_cell_bold),
            Paragraph("<b>scheduler.service.js:</b> node-cron background job running at midnight in Asia/Kolkata timezone.<br/>"
                      "<b>email.service.js:</b> Nodemailer integration with responsive HTML templates for digests and alerts.", table_cell_style)
        ],
        [
            Paragraph("<code>client/src/contexts/</code>", table_cell_bold),
            Paragraph("<b>AuthContext.js:</b> Global auth state, token decoding, automatic expiration checks.<br/>"
                      "<b>ThemeContext.js:</b> Light/Dark/System theme toggling setting <code>.dark</code> class on root.", table_cell_style)
        ],
        [
            Paragraph("<code>client/src/services/</code>", table_cell_bold),
            Paragraph("<b>apiClient.js:</b> Axios instance configured with request JWT injection and 401 response handling.<br/>"
                      "<b>*service.js:</b> Granular API wrappers for analytics, budgets, transactions, and auth.", table_cell_style)
        ],
        [
            Paragraph("<code>client/src/pages/</code>", table_cell_bold),
            Paragraph("<b>DashboardPage.jsx:</b> Summary metric cards, pie/line charts, quick add modal.<br/>"
                      "<b>TransactionsPage.jsx:</b> Full ledger with multi-criteria filters & pagination.<br/>"
                      "<b>BudgetPage.jsx:</b> Budget cards with live animated progress bars.<br/>"
                      "<b>GoalsPage.jsx:</b> Circular progress trackers and milestone contribution forms.", table_cell_style)
        ],
        [
            Paragraph("<code>docker-compose.yml</code>", table_cell_bold),
            Paragraph("Multi-container configuration orchestrating Server (Node 18), Client (Nginx), and MongoDB with isolated network bridging.", table_cell_style)
        ]
    ]

    t_file = Table(file_data, colWidths=[150, 354])
    t_file.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_file)

    story.append(Spacer(1, 14))

    # ==================== SECTION 4 ====================
    story.append(Paragraph("4. End-to-End Engineering Workflows & Flowcharts", h1_style))

    # Flowchart A: Budget Alert
    story.append(Paragraph("A. Real-Time 80% & 100% Budget Alert Workflow", h2_style))
    
    flow_a_box = [
        [
            Paragraph("<b>[User Submits Expense]</b> &rarr; <code>POST /api/transactions</code><br/>"
                      "&darr;<br/>"
                      "<b>[DB Save & Trigger]</b> &rarr; Saves Transaction document & invokes <code>checkAndNotifyBudgetBreach()</code><br/>"
                      "&darr;<br/>"
                      "<b>[Aggregation Engine]</b> &rarr; Queries active budgets for category/global & aggregates total spent in date window<br/>"
                      "&darr;<br/>"
                      "<b>[Threshold Evaluation]</b> &rarr; <code>usagePercentage = (totalSpent / budget.amount) * 100</code><br/>"
                      "&bull; <b>80% &le; Usage &lt; 100%:</b> Triggers <code>sendBudgetBreachAlert(..., 80)</code> &rarr; Dispatches ⚠️ <b>Orange Warning Email</b><br/>"
                      "&bull; <b>Usage &ge; 100%:</b> Triggers <code>sendBudgetBreachAlert(..., 100)</code> &rarr; Dispatches 🛑 <b>Red Critical Breach Email</b><br/>"
                      "&bull; <b>Client Progress Bar:</b> Dynamic CSS switches: <b>Green (&lt;80%)</b> &rarr; <b>Yellow (&ge;80%)</b> &rarr; <b>Red (&ge;100%)</b>", callout_style)
        ]
    ]
    t_flow_a = Table(flow_a_box, colWidths=[letter[0]-108])
    t_flow_a.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FEF3C7")), # Amber tint
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#D97706")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_flow_a)

    story.append(Spacer(1, 10))

    # Flowchart B: Scheduled Cron
    story.append(Paragraph("B. Timezone-Aware Automated Email Digest Workflow", h2_style))
    flow_b_box = [
        [
            Paragraph("<b>[Cron Trigger]</b> &rarr; <code>node-cron</code> triggers at <code>00:05 AM</code> in <code>Asia/Kolkata</code><br/>"
                      "&darr;<br/>"
                      "<b>[Timezone Partitioning]</b> &rarr; <code>moment-timezone</code> resolves exact UTC boundary of yesterday (00:00:00 &rarr; 23:59:59)<br/>"
                      "&darr;<br/>"
                      "<b>[User Query & Filter]</b> &rarr; Selects users where <code>emailPreferences.dailyReport === true</code><br/>"
                      "&darr;<br/>"
                      "<b>[MongoDB Aggregation]</b> &rarr; Groups yesterday's expenses by category + calculates total expenditure<br/>"
                      "&darr;<br/>"
                      "<b>[Nodemailer Dispatch]</b> &rarr; Populates responsive HTML template & delivers personalized digest to inbox", callout_style)
        ]
    ]
    t_flow_b = Table(flow_b_box, colWidths=[letter[0]-108])
    t_flow_b.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F0FDF4")), # Green tint
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#059669")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_flow_b)

    story.append(PageBreak())

    # ==================== SECTION 5 ====================
    story.append(Paragraph("5. Architectural Decision Matrix (\"Why I Chose Each Technology\")", h1_style))
    story.append(Paragraph("In technical interviews, justify your technology choices through trade-offs and engineering requirements:", body_style))

    tech_matrix = [
        [Paragraph("<b>TECHNOLOGY</b>", table_header_style), Paragraph("<b>WHY IT WAS CHOSEN</b>", table_header_style), Paragraph("<b>ALTERNATIVE CONSIDERED & TRADE-OFF</b>", table_header_style)],
        [
            Paragraph("<b>MongoDB & Mongoose</b>", table_cell_bold),
            Paragraph("&bull; Flexible schema for dynamic custom categories and variable metadata.<br/>"
                      "&bull; High-performance Aggregation Pipeline for computing real-time chart analytics and budget totals directly in DB.", table_cell_style),
            Paragraph("<b>PostgreSQL:</b> Would require complex multi-table joins and rigid migrations for custom user tags and category colors.", table_cell_style)
        ],
        [
            Paragraph("<b>React 18 + Context API</b>", table_cell_bold),
            Paragraph("&bull; SPA architecture with fast client-side routing.<br/>"
                      "&bull; Context API handles Auth & Theme cleanly without third-party boilerplate.", table_cell_style),
            Paragraph("<b>Redux Toolkit:</b> Overkill for this application scale; Context API + custom hooks provided superior maintainability.", table_cell_style)
        ],
        [
            Paragraph("<b>Passport.js + JWT</b>", table_cell_bold),
            Paragraph("&bull; Stateless, token-based authentication scalable across multi-container instances without shared session stores.<br/>"
                      "&bull; Bcrypt salted hashing prevents rainbow table exploits.", table_cell_style),
            Paragraph("<b>Session Cookies:</b> Requires Redis session store in clustered container environments, adding deployment complexity.", table_cell_style)
        ],
        [
            Paragraph("<b>Tailwind CSS</b>", table_cell_bold),
            Paragraph("&bull; Utility-first design system with rapid prototyping.<br/>"
                      "&bull; Native class-based Dark Mode support for seamless day/night toggles with zero CSS bloat.", table_cell_style),
            Paragraph("<b>Bootstrap / MUI:</b> Heavy bundle sizes, hard-to-customize styling, and difficult dark mode theming.", table_cell_style)
        ],
        [
            Paragraph("<b>Node-Cron + Moment-TZ</b>", table_cell_bold),
            Paragraph("&bull; Built-in lightweight task scheduling within the Node runtime.<br/>"
                      "&bull; Moment-timezone eliminates server UTC offset bugs during midnight report generation.", table_cell_style),
            Paragraph("<b>External Cron Service (AWS EventBridge):</b> Unnecessary cloud vendor lock-in for a standalone monolithic service.", table_cell_style)
        ],
        [
            Paragraph("<b>Chart.js + Framer Motion</b>", table_cell_bold),
            Paragraph("&bull; Canvas-based GPU-accelerated chart rendering.<br/>"
                      "&bull; Framer Motion provides fluid page transitions and staggered entry animations for high-polish UX.", table_cell_style),
            Paragraph("<b>D3.js:</b> Unnecessarily high development complexity for standard financial bar/line/pie charts.", table_cell_style)
        ]
    ]

    t_tech = Table(tech_matrix, colWidths=[110, 210, 184])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_tech)

    story.append(Spacer(1, 14))

    # ==================== SECTION 6 ====================
    story.append(Paragraph("6. Interview Vocabulary Guide: Keywords to USE vs AVOID", h1_style))
    story.append(Paragraph("How you articulate your project determines whether interviewers view you as a junior coder or a production-ready software engineer. Use this vocabulary matrix:", body_style))

    vocab_matrix = [
        [Paragraph("<b>❌ KEYWORDS TO AVOID (Sounds Junior)</b>", table_header_style), Paragraph("<b>✅ KEYWORDS TO USE (Sounds Senior & Professional)</b>", table_header_style)],
        [
            Paragraph("\"I made a basic CRUD app to store expenses.\"", table_cell_style),
            Paragraph("<b>\"I engineered a full-stack personal finance system with real-time proactive notification hooks and background analytics.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I used MongoDB because it's easy and NoSQL.\"", table_cell_style),
            Paragraph("<b>\"I leveraged MongoDB's Aggregation Framework (<code>$match</code>, <code>$group</code>, <code>$lookup</code>) to offload heavy analytical calculations directly to the database engine.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I wrote a script to send emails.\"", table_cell_style),
            Paragraph("<b>\"I implemented a decoupled background task scheduler using <code>node-cron</code> with timezone-aware calendar partitioning (<code>moment-timezone</code>) and responsive HTML templates.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I used JWT to check users.\"", table_cell_style),
            Paragraph("<b>\"I designed stateless JWT authentication integrated with Passport.js, secured with bcrypt password hashing and Axios request/response interceptors for 401 handling.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I just added dark mode with CSS.\"", table_cell_style),
            Paragraph("<b>\"I architected a token-based design system using Tailwind CSS supporting dynamic system-synced light/dark mode and fluid Framer Motion animations.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I checked budgets on the front-end.\"", table_cell_style),
            Paragraph("<b>\"I built a server-side threshold evaluation pipeline that dynamically checks spending limits post-transaction and dispatches tiered warnings at 80% and 100% utilization.\"</b>", table_cell_bold)
        ],
        [
            Paragraph("\"I put everything in one server.\"", table_cell_style),
            Paragraph("<b>\"I structured the codebase following MVC separation of concerns and containerized the entire stack with Docker & Docker Compose for deterministic deployments.\"</b>", table_cell_bold)
        ]
    ]

    t_vocab = Table(vocab_matrix, colWidths=[240, 264])
    t_vocab.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor("#991B1B")), # Dark Red
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#065F46")), # Dark Green
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_vocab)

    story.append(PageBreak())

    # ==================== SECTION 7 ====================
    story.append(Paragraph("7. Master Technical Interview Questions & Battle-Tested Answers", h1_style))

    # Q1
    story.append(Paragraph("Q1: How do you ensure high performance and low latency when querying millions of transactions?", h2_style))
    ans1 = """
    <b>Answer:</b> <i>\"We optimized database performance on three levels:</i><br/>
    <b>1. Compound Indexing:</b> In <code>Transaction.model.js</code>, we established compound indexes on <code>{ user: 1, date: -1 }</code> and <code>{ user: 1, type: 1 }</code>. Because all queries and aggregations are scoped to the authenticated user and sorted/filtered by date, MongoDB executes fast Index Scans (IXSCAN) rather than expensive Collection Scans (COLLSCAN).<br/>
    <b>2. In-Database Aggregations:</b> Instead of pulling thousands of raw transaction objects into Node.js memory to compute totals with JavaScript loops, we push computation to MongoDB using <code>$match</code> &rarr; <code>$group</code> &rarr; <code>$project</code> pipelines, drastically reducing memory footprint and network payload.<br/>
    <b>3. Projection & Pagination:</b> List views enforce query limits, pagination skips, and selective field projections.\"
    """
    story.append(Paragraph(ans1, body_style))
    story.append(Spacer(1, 4))

    # Q2
    story.append(Paragraph("Q2: How does the cron scheduler handle timezone discrepancies when generating daily reports?", h2_style))
    ans2 = """
    <b>Answer:</b> <i>\"Cloud servers (e.g. AWS, Render) default to UTC. If a cron runs at 00:05 UTC, it would be 05:35 AM IST, which would disrupt user reporting. To solve this, we used <code>moment-timezone</code> configured explicitly to <code>Asia/Kolkata</code>. The scheduler converts the user's localized 'yesterday' into absolute UTC ISO boundaries (<code>2026-08-17T18:30:00.000Z</code> to <code>2026-08-18T18:29:59.999Z</code>) before querying MongoDB, guaranteeing that users receive reports reflecting their true calendar day regardless of where the server is hosted.\"</i>
    """
    story.append(Paragraph(ans2, body_style))
    story.append(Spacer(1, 4))

    # Q3
    story.append(Paragraph("Q3: How do you prevent email spam when a user repeatedly logs transactions above the 80% or 100% threshold?", h2_style))
    ans3 = """
    <b>Answer:</b> <i>\"In <code>checkAndNotifyBudgetBreach()</code>, alert notifications are state-gated using notification flags (such as <code>notifiedAt80</code> and <code>notifiedAt100</code> on the Budget document) and verified against the user's <code>emailPreferences.budgetAlerts</code> setting. Once an 80% warning has been dispatched for an active monthly cycle, subsequent transactions between 80% and 99% will not re-trigger emails. The system triggers the next alert only when the threshold transitions into the 100% breach category.\"</i>
    """
    story.append(Paragraph(ans3, body_style))
    story.append(Spacer(1, 4))

    # Q4
    story.append(Paragraph("Q4: How is data isolation and security maintained in a multi-tenant environment?", h2_style))
    ans4 = """
    <b>Answer:</b> <i>\"Security is enforced defensively at multiple layers:</i><br/>
    &bull; <b>Stateless JWT Verification:</b> All protected endpoints pass through Passport-JWT middleware which extracts and verifies the bearer token from the header.<br/>
    &bull; <b>Strict Tenant Scoping:</b> All database queries in controllers strictly inject <code>{ user: req.user._id }</code> into the query filter, ensuring users can never read, modify, or delete another user's records.<br/>
    &bull; <b>Password Defense:</b> Passwords are salted and hashed via bcrypt in Mongoose <code>pre('save')</code> hooks, and marked with <code>select: false</code> to prevent accidental exposure in API responses.<br/>
    &bull; <b>CORS & Input Validation:</b> Strict CORS configurations and Formik/Yup schema validations prevent malicious payloads and injection vulnerabilities.\"
    """
    story.append(Paragraph(ans4, body_style))

    story.append(Spacer(1, 14))

    # Final Summary Signoff Box
    signoff_data = [
        [
            Paragraph("<b>🎯 Summary Checklist for Interview Day:</b><br/>"
                      "&check; Emphasize <b>proactive alerts</b> and <b>background automation</b> as the core differentiator.<br/>"
                      "&check; Highlight <b>MongoDB Aggregation Pipelines</b> when discussing data queries.<br/>"
                      "&check; Mention <b>Timezone-aware Cron scheduling</b> and <b>Compound Indexing</b> for scalability.<br/>"
                      "&check; Walk through the <b>Axios Interceptor</b> and <b>Passport-JWT</b> flow for full-stack authentication.<br/>"
                      "&check; Showcase <b>Docker Compose</b> containerization for production deployment readiness.", callout_style)
        ]
    ]
    t_signoff = Table(signoff_data, colWidths=[letter[0]-108])
    t_signoff.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1.5, primary_color),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_signoff)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at: {filename}")

if __name__ == "__main__":
    output_path = "/Users/aditi/Desktop/FinTrack_Pro_Architecture_and_Interview_Mastery_Guide.pdf"
    build_pdf(output_path)
