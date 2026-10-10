document.addEventListener("DOMContentLoaded", function () {
    const footerHTML = `
    <footer class="border-t border-slate-800/80 bg-slate-950 py-12 text-center text-sm text-slate-500">
        <div class="max-w-7xl mx-auto px-6 space-y-2">
            <p class="font-['Space_Grotesk'] font-bold text-white">GUITARS FOR VETS • CLARKSVILLE CHAPTER #287</p>
            <p>Established February 18, 2026.</p>
        </div>
    </footer>`;

    const footerPlaceholder = document.getElementById("footer-placeholder");
    if (footerPlaceholder) {
        footerPlaceholder.innerHTML = footerHTML;
    }
});
