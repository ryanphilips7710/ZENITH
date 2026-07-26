"""
Structured knowledge base for the IBM Z Summit 2026 AI Assistant.

This is the "context" the assistant is grounded in — instead of a full
RAG/vector-store pipeline (overkill for ~500 participants and a handful
of documents), the event data is kept as clean structured Python objects
and injected directly into the LLM's system prompt. This is faster to
build, has zero moving parts to break during a live demo, and is easy
to keep in sync manually before the event.

"""

EVENT_NAME = "IBM Z Summit 2026"

VENUE_INFO = {
    "main_venue": "Open Auditorium, Christ University Kengeri Campus, Bangalore, India",
    "wifi_ssid": "IBMZ-SUMMIT-2026",
    "wifi_password": "1234",
    "help_desk_location": "Registration Desk, Ground Floor Block 1",
    "parking_info": "Parking is available towards the left side of the main entrance. Please display your event badge.",
    "first_aid_location": "Medical room, Ground Floor Block 1, next to the help desk",
    "lost_and_found": "Please Report to the volunteer desk near the main entrance",
}

FAQS = [
    {
        "question": "What is IBM Z Summit 2026?",
        "answer": (
            "IBM Z Summit 2026 is the flagship annual event of the IBM Z "
            "Student Club, featuring technical workshops, hands-on labs, "
            "a hackathon, guest speaker sessions, networking activities, "
            "and competitions, with 500+ participants from multiple colleges."
        ),
    },
    {
        "question": "How do I get my certificate?",
        "answer": (
            "Participation certificates will be emailed within 7 days after "
            "the event. Certificates for winners will be handed over during "
            "the closing ceremony along with their prizes."
        ),
    },
    {
        "question": "Is food provided?",
        "answer": (
            "Yes, lunch and refreshments will be provided to all registered "
            "participants. Lunch break is between 1:00 PM and 2:00 PM at the "
            "4th block south canteen."
        ),
    },
    {
        "question": "Who do I contact for help during the event?",
        "answer": "You can visit the volunteer desk near the main entrance, or look for anyone wearing an IBM Z Student Club volunteer badge.",
    },
    {
        "question": "How do I form a team for the hackathon?",
        "answer": "TODO: e.g. Teams of up to 4 can register together during check-in, or solo participants can join the team formation board at the Hackathon Room before kickoff.",
    },
    {
        "question": "What should I bring / is there a dress code?",
        "answer": "Bring your laptop, charger, and student ID. Smart casuals; comfortable clothing recommended for the hackathon.",
    },
    {
        "question": "Is accommodation provided for outstation participants?",
        "answer": "Yes, on a request basis — contact the organizing committee at least 3 days before the event.",
    },
    {
        "question": "How do I register for competitions?",
        "answer": "On-spot registration at the front desk, or pre-register through our event website. Check the schedule for competition timings.",
    },
    {
        "question": "What if I lose something during the event?",
        "answer": "Report to the volunteer desk near the main entrance — lost items are collected there throughout the day.",
    },
    {
        "question": "Is there a networking session?",
        "answer": "Yes — see the 'Networking Mixer' session on the schedule, open to all participants and speakers.",
    },
]

# Each session: id, title, track, speaker, room, start_time, end_time (use 24h "HH:MM" on event day)
SCHEDULE = [
    {
        "id": "S1",
        "title": "Opening Keynote",
        "track": "General",
        "speaker": "Dr. Jane Smith, IBM Z Expert",
        "room": "Open Auditorium",
        "start_time": "09:00",
        "end_time": "09:45",
    },
    {
        "id": "S2",
        "title": "Introduction to IBM Z",
        "track": "Workshop",
        "speaker": "Dr. John Doe, IBM Z Researcher",
        "room": "Room 101, 1st Floor, Block 1",
        "start_time": "10:00",
        "end_time": "11:30",
    },
    {
        "id": "S3",
        "title": "Hands-on Lab: Mainframe Basics",
        "track": "Hands-on Lab",
        "speaker": "Priya Nair, IBM Z Solutions Engineer",
        "room": "Lab 201, 2nd Floor, Block 2",
        "start_time": "10:00",
        "end_time": "11:30",
    },
    {
        "id": "S4",
        "title": "Guest Talk: Careers in Enterprise Computing",
        "track": "Guest Speaker",
        "speaker": "Rahul Mehta, Senior Architect, IBM",
        "room": "Open Auditorium",
        "start_time": "11:45",
        "end_time": "12:30",
    },
    {
        "id": "S5",
        "title": "Hackathon Kickoff",
        "track": "Hackathon",
        "speaker": "Dr. Alice Johnson, IBM Z Developer",
        "room": "3rd floor, Crystal Block, Architecture Building",
        "start_time": "12:00",
        "end_time": "12:30",
    },
    {
        "id": "S6",
        "title": "Lunch Break",
        "track": "General",
        "speaker": "—",
        "room": "4th Block South Canteen",
        "start_time": "13:00",
        "end_time": "14:00",
    },
    {
        "id": "S7",
        "title": "Hands-on Lab: Deploying on IBM Z",
        "track": "Hands-on Lab",
        "speaker": "Priya Nair, IBM Z Solutions Engineer",
        "room": "Lab 201, 2nd Floor, Block 2",
        "start_time": "14:15",
        "end_time": "15:45",
    },
    {
        "id": "S8",
        "title": "Workshop: AI Workloads on Mainframe",
        "track": "Workshop",
        "speaker": "Dr. John Doe, IBM Z Researcher",
        "room": "Room 101, 1rd Floor, Block 1",
        "start_time": "14:15",
        "end_time": "15:45",
    },
    {
        "id": "S9",
        "title": "Hackathon Working Session",
        "track": "Hackathon",
        "speaker": "Mentors on rotation",
        "room": "3rd floor, Crystal Block, Architecture Building",
        "start_time": "12:30",
        "end_time": "17:00",
    },
    {
        "id": "S10",
        "title": "Coding Competition: Speed Debugging Challenge",
        "track": "Competition",
        "speaker": "Organizing Committee",
        "room": "Room 302, 3rd floor, 3rd block",
        "start_time": "15:00",
        "end_time": "16:30",
    },
    {
        "id": "S11",
        "title": "Networking Mixer",
        "track": "Networking",
        "speaker": "—",
        "room": "Open Auditorium",
        "start_time": "16:00",
        "end_time": "17:00",
    },
    {
        "id": "S12",
        "title": "Hackathon Submission Deadline & Judging",
        "track": "Hackathon",
        "speaker": "Panel of Judges",
        "room": "3rd floor, Crystal Block, Architecture Building",
        "start_time": "17:00",
        "end_time": "18:00",
    },
    {
        "id": "S13",
        "title": "Closing Ceremony & Prize Distribution",
        "track": "General",
        "speaker": "Organizing Committee",
        "room": "Open Auditorium",
        "start_time": "18:15",
        "end_time": "19:00",
    },
]

SPEAKERS = [
    {
        "name": "Dr. Jane Smith",
        "bio": "Dr. Jane Smith is an IBM Z Expert with over 15 years of experience in mainframe technology.",
        "session_id": "S1",
    },
    {
        "name": "Dr. John Doe",
        "bio": "TODO: e.g. Dr. John Doe is an IBM Z Researcher focused on hybrid cloud and mainframe integration.",
        "session_id": "S2",
    },
    {
        "name": "Priya Nair",
        "bio": "TODO: e.g. Priya Nair is an IBM Z Solutions Engineer specializing in enterprise deployment pipelines.",
        "session_id": "S3",
    },
    {
        "name": "Rahul Mehta",
        "bio": "TODO: e.g. Rahul Mehta is a Senior Architect at IBM with experience building large-scale enterprise systems.",
        "session_id": "S4",
    },
    {
        "name": "Dr. Alice Johnson",
        "bio": "TODO: e.g. Dr. Alice Johnson is an IBM Z Developer who has led multiple student hackathon tracks.",
        "session_id": "S5",
    },
]