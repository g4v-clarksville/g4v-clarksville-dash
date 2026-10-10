document.addEventListener("DOMContentLoaded", function () {
    const navHTML = `
    <nav class="sticky top-0 z-50 backdrop-blur-xl bg-[#030712]/80 border-b border-slate-800/60">
        <div class="max-w-7xl mx-auto px-6 h-24 flex items-center justify-between">
            <!-- Left Group: Chapter Brand & G4V National Portal -->
            <div class="flex items-center gap-6">
                <a href="index.html" class="flex items-center gap-4">
                    <img src="images/Picture2.png" alt="Chapter Patch" class="w-16 h-16 rounded-2xl object-cover shadow-xl shadow-amber-500/20 border-2 border-amber-500/40">
                    <div>
                        <span class="block font-['Space_Grotesk'] font-bold tracking-tight text-white text-lg">G4V CLARKSVILLE</span>
                        <span class="block text-xs text-amber-400 font-semibold tracking-widest uppercase">Chapter #287</span>
                    </div>
                </a>

                <a href="https://guitars4vets.org" target="_blank" class="hidden sm:inline-block px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-black font-semibold text-xs tracking-wide transition-all shadow-lg shadow-amber-500/20">
                    National Portal
                </a>
            </div>

            <!-- Center Navigation Links -->
            <div class="hidden md:flex items-center gap-8 text-sm font-medium text-slate-300">
                <a href="mission.html" class="nav-link hover:text-amber-400 transition-colors" data-page="mission.html">Mission</a>
                <a href="operations.html" class="nav-link hover:text-amber-400 transition-colors" data-page="operations.html">Operations</a>
                <a href="songs.html" class="nav-link hover:text-amber-400 transition-colors" data-page="songs.html">Songbook Index</a>
                <a href="archives.html" class="nav-link hover:text-amber-400 transition-colors" data-page="archives.html">Archives</a>
                <a href="sessions.html" class="nav-link hover:text-amber-400 transition-colors" data-page="sessions.html">Sessions</a>
                <a href="jams.html" class="nav-link hover:text-amber-400 transition-colors" data-page="jams.html">Jams</a>
            </div>

            <!-- Right Group: Local Office Info & OSD Partner Logo -->
            <div class="flex items-center gap-4">
                <div class="text-right hidden xl:block">
                    <a href="https://maps.google.com/?q=115+N+3rd+St+Clarksville+TN+37040" target="_blank" rel="noopener noreferrer" class="block text-xs font-bold text-amber-400 hover:text-amber-300 transition-colors">
                        Local Office &rarr;
                    </a>
                    <span class="block text-[10px] text-slate-400">115 N 3rd St, Clarksville</span>
                </div>

                <a href="https://www.osdtn.org" target="_blank" rel="noopener noreferrer" title="Visit OSD Tennessee National Portal" class="group relative">
                    <img src="images/OSD logo.jpg" alt="Operation Stand Down Logo" class="w-16 h-16 rounded-2xl object-cover shadow-xl shadow-amber-500/20 border-2 border-amber-500/40 group-hover:scale-105 transition-transform duration-300">
                </a>
            </div>
        </div>
    </nav>`;

    // Insert into placeholder element
    const navPlaceholder = document.getElementById("nav-placeholder");
    if (navPlaceholder) {
        navPlaceholder.innerHTML = navHTML;

        // Automatically highlight active page link
        const currentPage = window.location.pathname.split("/").pop() || "index.html";
        document.querySelectorAll(".nav-link").forEach(link => {
            if (link.getAttribute("data-page") === currentPage) {
                link.classList.remove("text-slate-300");
                link.classList.add("text-amber-400", "font-bold");
            }
        });
    }
});
