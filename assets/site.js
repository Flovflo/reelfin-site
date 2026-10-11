const header = document.querySelector(".site-header");
const revealItems = document.querySelectorAll(".reveal");
const navLinks = [...document.querySelectorAll(".site-nav a[href^='#']")];
const sections = navLinks
  .map((link) => document.querySelector(link.getAttribute("href")))
  .filter(Boolean);

const updateHeader = () => {
  header?.classList.toggle("is-scrolled", window.scrollY > 8);
};

const setActiveLink = (id) => {
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.getAttribute("href") === `#${id}`);
  });
};

updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  revealItems.forEach((item) => item.classList.add("is-visible"));
} else {
  document.body.classList.add("motion-ready");

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }

        entry.target.classList.add("is-visible");
        revealObserver.unobserve(entry.target);
      });
    },
    {
      // Any intersection: a section taller than ~5 viewports can never reach a ratio threshold.
      threshold: 0,
      rootMargin: "0px 0px -10% 0px",
    }
  );

  revealItems.forEach((item) => {
    const rect = item.getBoundingClientRect();
    if (rect.top < window.innerHeight * 0.92) {
      item.classList.add("is-visible");
      return;
    }

    revealObserver.observe(item);
  });
}

// Scroll-spy from scroll position: the IntersectionObserver version only saw
// sections whose intersection changed, so the underline went stale (and stayed
// lit above the first section).
const updateActiveLink = () => {
  const headerOffset = header ? header.getBoundingClientRect().bottom : 0;
  const probe = headerOffset + window.innerHeight * 0.3;
  const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;

  let activeId = null;
  if (atBottom && sections.length) {
    activeId = sections[sections.length - 1].id;
  } else {
    sections.forEach((section) => {
      if (section.getBoundingClientRect().top <= probe) {
        activeId = section.id;
      }
    });
  }

  setActiveLink(activeId);
};

let activeLinkFrame = 0;
const scheduleActiveLinkUpdate = () => {
  if (activeLinkFrame) {
    return;
  }

  activeLinkFrame = requestAnimationFrame(() => {
    activeLinkFrame = 0;
    updateActiveLink();
  });
};

updateActiveLink();
window.addEventListener("scroll", scheduleActiveLinkUpdate, { passive: true });
window.addEventListener("resize", scheduleActiveLinkUpdate);
