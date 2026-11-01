const header = document.querySelector(".site-header");
const menuButton = document.querySelector(".menu-toggle");
const menu = document.querySelector("#mobile-menu");

const closeMenu = () => {
  menuButton?.setAttribute("aria-expanded", "false");
  if (menu) menu.hidden = true;
};

menuButton?.addEventListener("click", () => {
  const isOpen = menuButton.getAttribute("aria-expanded") === "true";
  menuButton.setAttribute("aria-expanded", String(!isOpen));
  if (menu) menu.hidden = isOpen;
});
menu?.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton?.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia("(min-width: 761px)").addEventListener("change", (event) => {
  if (event.matches) closeMenu();
});
if (menuButton && menu) document.documentElement.classList.add("has-menu");
const updateHeader = () => header?.classList.toggle("is-scrolled", window.scrollY > 12);
updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });

// Content is visible by default. Animation never owns a persistent hidden state.
const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const playedReveals = new WeakSet();
const activeReveals = new Set();
let revealObserver;

const reveal = (element, { delay = 0, showcase = false } = {}) => {
  if (!element || playedReveals.has(element) || reducedMotion.matches || !element.animate) return;
  playedReveals.add(element);
  const animation = element.animate(
    [
      { opacity: 0, transform: showcase ? "translateY(24px) scale(.985)" : "translateY(16px)" },
      { opacity: 1, transform: "none" },
    ],
    { duration: showcase ? 860 : 640, delay, easing: "cubic-bezier(.22, 1, .36, 1)", fill: "backwards" },
  );
  activeReveals.add(animation);
  animation.finished.then(() => animation.cancel()).catch(() => {}).finally(() => activeReveals.delete(animation));
};

const startReveals = () => {
  if (reducedMotion.matches) return;
  const hero = document.querySelector(".hero");
  if (hero && (!window.location.hash || window.location.hash === "#top")) {
    const entrance = [
      ...hero.querySelectorAll(".hero__title-line"),
      hero.querySelector(".hero__lede"),
      hero.querySelector(".button"),
      hero.querySelector(".hero__platforms"),
      hero.querySelector(".hero__duo-link"),
    ];
    entrance.forEach((element, index) => reveal(element, { delay: index * 55 }));
    reveal(hero.querySelector(".hero__stage"), { delay: 240, showcase: true });
    reveal(hero.querySelector(".image-credit"), { delay: 320 });
  }
  if (!("IntersectionObserver" in window)) return;
  revealObserver?.disconnect();
  revealObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      const element = entry.target;
      const group = element.parentElement;
      const isRow = group?.matches(".duo-stage, .feature-grid, .tv-benefits");
      const index = isRow ? [...group.children].indexOf(element) : 0;
      const delay = window.innerWidth > 760 ? Math.min(index * 75, 150) : 0;
      reveal(element, { delay });
      revealObserver.unobserve(element);
    }
  }, { threshold: 0.12, rootMargin: "0px 0px -5% 0px" });
  document.querySelectorAll(".section-heading, .duo-stage > figure, .feature, .tv-benefits > article, .tvos > .app-capture, .compatibility, .faq > h2, .faq details, .final-cta").forEach((element) => {
    if (!playedReveals.has(element)) revealObserver.observe(element);
  });
};

reducedMotion.addEventListener("change", () => {
  if (reducedMotion.matches) {
    revealObserver?.disconnect();
    for (const animation of activeReveals) animation.cancel();
    activeReveals.clear();
  } else {
    startReveals();
  }
});
startReveals();
