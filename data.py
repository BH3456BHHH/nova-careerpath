CAREER_PATHS = {
    "consulting": {
        "name": "Management Consulting",
        "description": "Strategy and operations advisory at top-tier firms",
        "required_skills": {
            "analytical": 9, "communication": 8, "leadership": 7,
            "business_strategy": 8, "technical": 5, "networking": 6,
        },
        "preferred_gpa": 16.0,
    },
    "investment_banking": {
        "name": "Investment Banking",
        "description": "M&A, capital markets and financial advisory",
        "required_skills": {
            "analytical": 9, "technical": 8, "communication": 7,
            "business_strategy": 7, "leadership": 6, "networking": 7,
        },
        "preferred_gpa": 17.0,
    },
    "tech": {
        "name": "Tech & Product",
        "description": "Product management, data and software roles at tech companies",
        "required_skills": {
            "technical": 9, "analytical": 8, "communication": 7,
            "business_strategy": 6, "leadership": 6, "networking": 5,
        },
        "preferred_gpa": 14.0,
    },
    "entrepreneurship": {
        "name": "Entrepreneurship & Startups",
        "description": "Founding or joining early-stage startups",
        "required_skills": {
            "business_strategy": 8, "leadership": 8, "communication": 8,
            "analytical": 7, "technical": 6, "networking": 8,
        },
        "preferred_gpa": 13.0,
    },
    "marketing": {
        "name": "Marketing & Brand",
        "description": "Brand management, digital marketing and consumer insights",
        "required_skills": {
            "communication": 9, "analytical": 7, "business_strategy": 7,
            "technical": 6, "leadership": 6, "networking": 6,
        },
        "preferred_gpa": 14.0,
    },
    "sustainability": {
        "name": "Sustainability & Impact",
        "description": "ESG, policy and impact-driven organisations",
        "required_skills": {
            "communication": 8, "analytical": 7, "business_strategy": 7,
            "leadership": 7, "networking": 7, "technical": 5,
        },
        "preferred_gpa": 14.0,
    },
}

COURSES = [
    {
        "name": "Strategy Consulting Fundamentals",
        "description": "Case structuring, hypothesis-driven thinking and client communication.",
        "career_relevance": ["consulting"],
    },
    {
        "name": "Financial Modelling & Valuation",
        "description": "DCF, LBO and comparable company analysis in Excel.",
        "career_relevance": ["investment_banking", "consulting"],
    },
    {
        "name": "Corporate Finance",
        "description": "Capital structure, M&A fundamentals and financial decision-making.",
        "career_relevance": ["investment_banking", "consulting"],
    },
    {
        "name": "Data Analysis & Python",
        "description": "Pandas, visualisation and statistical analysis for business problems.",
        "career_relevance": ["tech", "consulting", "investment_banking"],
    },
    {
        "name": "Product Management",
        "description": "Roadmaps, user research, sprint planning and go-to-market strategy.",
        "career_relevance": ["tech"],
    },
    {
        "name": "Digital Marketing",
        "description": "SEO, SEM, content strategy and performance analytics.",
        "career_relevance": ["marketing", "entrepreneurship"],
    },
    {
        "name": "Brand Management",
        "description": "Brand equity, consumer insights and campaign planning.",
        "career_relevance": ["marketing"],
    },
    {
        "name": "Entrepreneurship & Venture Creation",
        "description": "Business model design, lean startup and fundraising basics.",
        "career_relevance": ["entrepreneurship"],
    },
    {
        "name": "ESG & Sustainable Finance",
        "description": "ESG frameworks, impact measurement and green finance instruments.",
        "career_relevance": ["sustainability"],
    },
    {
        "name": "Negotiation & Influence",
        "description": "Structured negotiation techniques for business and client settings.",
        "career_relevance": ["consulting", "investment_banking", "entrepreneurship"],
    },
]

ACTIVITIES = [
    {
        "name": "Consulting Club",
        "description": "Case prep, mock interviews and real client projects with alumni mentors.",
        "career_relevance": ["consulting"],
    },
    {
        "name": "Finance & Investment Society",
        "description": "Stock pitches, investment fund management and financial modelling workshops.",
        "career_relevance": ["investment_banking", "consulting"],
    },
    {
        "name": "Entrepreneurship Society",
        "description": "Hackathons, pitch competitions and startup mentorship from founders.",
        "career_relevance": ["entrepreneurship", "tech"],
    },
    {
        "name": "Marketing Society",
        "description": "Live brand projects, case competitions and industry speaker events.",
        "career_relevance": ["marketing"],
    },
    {
        "name": "Sustainability & Impact Club",
        "description": "ESG research, NGO partnerships and sustainability consulting projects.",
        "career_relevance": ["sustainability"],
    },
    {
        "name": "Tech & Data Society",
        "description": "Python workshops, data competitions and product management sprints.",
        "career_relevance": ["tech"],
    },
    {
        "name": "Debate Society",
        "description": "Structured argumentation and public speaking for client-facing roles.",
        "career_relevance": ["consulting", "investment_banking", "marketing"],
    },
    {
        "name": "Model United Nations",
        "description": "Negotiation, policy analysis and international stakeholder management.",
        "career_relevance": ["sustainability", "consulting"],
    },
]

ALUMNI_TRAJECTORIES = [
    {
        "career": "consulting",
        "label": "McKinsey — via Consulting Club + 2 internships",
        "path": [
            {"role": "Consulting Club President", "org": "Nova SBE", "duration": "1 year"},
            {"role": "Summer Analyst", "org": "Roland Berger", "duration": "3 months"},
            {"role": "Business Analyst", "org": "McKinsey & Company", "duration": "Full-time"},
        ],
        "key_activities": ["Consulting Club", "Case competitions", "Finance Society"],
    },
    {
        "career": "investment_banking",
        "label": "Goldman Sachs — via Finance Society + IBD internship",
        "path": [
            {"role": "Finance Society VP", "org": "Nova SBE", "duration": "1 year"},
            {"role": "Summer Analyst", "org": "BNP Paribas", "duration": "3 months"},
            {"role": "Analyst, IBD", "org": "Goldman Sachs", "duration": "Full-time"},
        ],
        "key_activities": ["Finance Society", "CFA Level 1", "Bloomberg certification"],
    },
    {
        "career": "tech",
        "label": "Google — via data projects + product internship",
        "path": [
            {"role": "Tech Society Lead", "org": "Nova SBE", "duration": "1 year"},
            {"role": "Product Intern", "org": "Farfetch", "duration": "6 months"},
            {"role": "Associate PM", "org": "Google", "duration": "Full-time"},
        ],
        "key_activities": ["Tech Society", "Python projects", "Hackathons"],
    },
    {
        "career": "entrepreneurship",
        "label": "Founded B2B SaaS — via Nova incubator",
        "path": [
            {"role": "Entrepreneurship Society President", "org": "Nova SBE", "duration": "1 year"},
            {"role": "Founder", "org": "Own startup", "duration": "Ongoing"},
        ],
        "key_activities": ["Entrepreneurship Society", "Beta-i accelerator", "Pitch competitions"],
    },
]
