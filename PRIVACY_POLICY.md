# Privacy Policy - TalentScout Hiring Assistant

**Last Updated:** February 15, 2026

## Overview

TalentScout is committed to protecting your privacy and handling your personal information responsibly. This privacy policy explains how we collect, use, and protect your data during the recruitment process.

## Information We Collect

During your interaction with our hiring assistant chatbot, we collect the following information:

- **Personal Details:** Full name, email address, phone number
- **Professional Information:** Years of experience, desired position(s), current location
- **Technical Skills:** Your declared tech stack (programming languages, frameworks, tools)
- **Conversation Data:** Chat history and responses during the screening process

## How We Use Your Information

Your information is used exclusively for:

- **Recruitment Purposes:** Evaluating your candidacy for open positions
- **Technical Assessment:** Generating personalized interview questions based on your skills
- **Communication:** Contacting you about next steps in the hiring process
- **Record Keeping:** Maintaining candidate records for our recruitment pipeline

## Data Storage and Security

### Current Implementation (Demo/Assignment)
- **Storage Location:** Local JSON file on the application server
- **Access Control:** Limited to recruitment team members only
- **Retention:** Data is retained until the recruitment process concludes

### Production Recommendations
For a production environment, we recommend:
- **Encryption:** AES-256 encryption for data at rest
- **Database:** Secure database (PostgreSQL/MongoDB) instead of local files
- **Transmission:** HTTPS/TLS for all data in transit
- **Backups:** Regular encrypted backups with access controls

## Your Rights (GDPR Compliance)

Under GDPR and similar data protection regulations, you have the right to:

- **Access:** Request a copy of your personal data we hold
- **Rectification:** Request correction of inaccurate information
- **Erasure:** Request deletion of your data ("right to be forgotten")
- **Portability:** Request your data in a machine-readable format
- **Objection:** Object to processing of your personal data
- **Withdraw Consent:** Withdraw consent at any time

To exercise any of these rights, contact us at: [recruitment@talentscout.example.com]

## Data Sharing

We **DO NOT**:
- Sell your personal information to third parties
- Share your data with advertisers
- Use your information for purposes unrelated to recruitment

We **MAY** share your information with:
- Hiring managers and interview panels (internal only)
- Background verification services (with your explicit consent)
- Applicant Tracking Systems (if you progress to next stages)

## Third-Party Services

This application uses:

- **Groq API:** For AI-powered question generation
  - Only tech stack information is sent to Groq
  - No personal identifiable information (name, email, phone) is transmitted
  - Groq's privacy policy: https://groq.com/privacy

## Data Retention

- **Active Candidates:** Data retained during active recruitment (typically 3-6 months)
- **Unsuccessful Candidates:** Data deleted within 30 days of process completion (unless you opt-in for future opportunities)
- **Hired Candidates:** Data transferred to HR systems with separate privacy policies

## Cookies and Tracking

This chatbot does not use:
- Cookies for tracking
- Analytics services
- Advertising pixels

Session data is stored temporarily in browser memory and cleared when you close the tab.

## Children's Privacy

Our recruitment services are not directed to individuals under 18 years of age. We do not knowingly collect information from minors.

## Changes to This Policy

We may update this privacy policy periodically. The "Last Updated" date at the top indicates the most recent revision. Continued use of our services after changes constitutes acceptance of the updated policy.

## Contact Us

For questions or concerns about this privacy policy or our data practices:

- **Email:** privacy@talentscout.example.com
- **Address:** TalentScout Recruitment Agency, [Address]
- **Data Protection Officer:** [Name and Contact]

## Consent

By continuing to interact with this chatbot after reading this privacy notice, you consent to the collection and use of your information as described in this policy.

---

**Note:** This is a demonstration application created for educational/assignment purposes. For production use, consult with legal counsel to ensure full compliance with applicable data protection regulations in your jurisdiction.
