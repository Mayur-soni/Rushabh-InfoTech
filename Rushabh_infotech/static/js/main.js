// 🚫 Do not run on admin
if (window.location.pathname.startsWith("/admin")) {
    console.log("Admin detected — skipping frontend JS");
} else {

    document.addEventListener("DOMContentLoaded", function () {

        /* ================= HEADER SCROLL ================= */

        const header = document.getElementById("header");

        function handleHeaderScroll() {
            if (!header) return;

            if (window.scrollY > 80) {
                header.classList.add("scrolled");
                header.classList.remove("transparent");
            } else {
                header.classList.remove("scrolled");
                header.classList.add("transparent");
            }
        }

        if (header) {
            const bodyClass = document.body.className;

            if (bodyClass.includes("page-home")) {
                header.classList.add("transparent");
            } else {
                header.classList.add("scrolled");
            }

            window.addEventListener("scroll", handleHeaderScroll);
            handleHeaderScroll();
        }

        /* ================= NAV ACTIVE LINK ================= */

        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll("nav a");

        navLinks.forEach(link => {
            if (link.getAttribute("href") === currentPath) {
                link.classList.add("active");
            }
        });

        /* ================= PARTICLES ================= */

        function createParticles() {
            const particlesContainer = document.getElementById("particles");
            if (!particlesContainer) return;

            particlesContainer.innerHTML = "";

            for (let i = 0; i < 20; i++) {
                const particle = document.createElement("div");
                particle.classList.add("particle");

                const size = Math.random() * 100 + 50;
                const left = Math.random() * 100;
                const duration = Math.random() * 30 + 20;
                const delay = Math.random() * 10;

                particle.style.width = `${size}px`;
                particle.style.height = `${size}px`;
                particle.style.left = `${left}%`;
                particle.style.animationDuration = `${duration}s`;
                particle.style.animationDelay = `${delay}s`;

                particlesContainer.appendChild(particle);
            }
        }

        createParticles();
        window.addEventListener("resize", createParticles);

        /* ================= SMOOTH SCROLL ================= */

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener("click", function (e) {
                e.preventDefault();

                const targetId = this.getAttribute("href");
                if (targetId === "#") return;

                const targetElement = document.querySelector(targetId);
                if (!targetElement) return;

                const headerHeight = document.querySelector("header")?.offsetHeight || 0;

                window.scrollTo({
                    top: targetElement.offsetTop - headerHeight,
                    behavior: "smooth"
                });
            });
        });

    });

}

