const g4vChapterData = [
    {
        cycleId: "Graduated",
        instructors: ["Dean Thomas"],
        status: "Completed",
        startDate: "2026-01-01", // Placeholder
        endDate: "2026-02-21",
        vets: [
            { seq: 1, name: "William Hensley", availability: "Graduated", gradDate: "2/21/2026" },
            { seq: 2, name: "John Artrip", availability: "Graduated", gradDate: "2/21/2026" }
        ]
    },
    {
        cycleId: "A-1",
        instructors: ["Dean Thomas", "Joseph Gentry"],
        status: "Active",
        startDate: "2026-03-02", // Adjust these to your actual start/end
        endDate: "2026-05-15",
        currentSession: 4,
        totalSessions: 10,
        vets: [
            { seq: 17, name: "Rubin Tubbs", availability: "Confirmed" },
            { seq: 8, name: "Mick Husband", availability: "Confirmed" },
            { seq: 13, name: "Spencer Farrow", availability: "Confirmed" },
            { seq: 5, name: "Robert Mason", availability: "Confirmed" }
        ]
    },
    {   
        cycleId: "C-1",
        instructors: ["Tim Rowe", "Charles Lampley"],
        status: "Upcoming",
        startDate: "2026-04-07",
        endDate: "2026-06-22",
        currentSession: 0,
        totalSessions: 10,
        vets: [
            { seq: 16, name: "Joe Gervais", availability: "Confirmed" },
            { seq: 19, name: "Don Garcia", availability: "Confirmed" },
            { seq: 23, name: "Aaron Rozmenoski", availability: "Confirmed" },
            { seq: 21, name: "David Chapman", availability: "Confirmed" }
        ]
    },
     {   
        cycleId: "B-1",
        instructors: ["Garth Arneson", "Tom Drzewiecki"],
        status: "Upcoming",
        startDate: "2026-05-19",
        endDate: "2026-08-4",
        currentSession: 0,
        totalSessions: 10,
        vets: [
            { seq: 6, name: "Billy Zielinski", availability: "Confirmed" },
            { seq: 9, name: "Luke Chowning", availability: "Confirmed" },
            { seq: 0, name: "Open", availability: "Open" },
            { seq: 0, name: "Open ", availability: "Open" }
        ]
    }
];