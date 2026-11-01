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
  // Apple product artwork stays still, including its containing surfaces.
  if (element.matches(".device-artwork") || element.querySelector(".device-artwork")) return;
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

// A brief silver trace follows our own emblem's pixels. The original PNG is
// always present underneath: no loader, hidden brand, or dependency on canvas.
const emblem = document.querySelector(".hero-emblem");
const emblemImage = emblem?.querySelector("img");
const emblemCanvas = emblem?.querySelector("canvas");
let emblemFrame = 0;
let emblemPlayed = false;

const stopEmblem = () => {
  cancelAnimationFrame(emblemFrame);
  emblemFrame = 0;
  const context = emblemCanvas?.getContext("2d");
  context?.clearRect(0, 0, emblemCanvas.width, emblemCanvas.height);
  emblemImage?.style.removeProperty("opacity");
};

const playEmblem = () => {
  if (emblemPlayed || reducedMotion.matches || document.hidden || !emblemCanvas || !emblemImage?.naturalWidth) return;
  const context = emblemCanvas.getContext("2d");
  if (!context) return;
  emblemPlayed = true;
  const bounds = emblem.getBoundingClientRect();
  if (bounds.bottom < 0 || bounds.top > window.innerHeight) return;
  const imageBounds = emblemImage.getBoundingClientRect();
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  emblemCanvas.width = Math.round(bounds.width * ratio);
  emblemCanvas.height = Math.round(bounds.height * ratio);
  context.scale(ratio, ratio);

  const sampler = document.createElement("canvas");
  sampler.width = emblemImage.naturalWidth;
  sampler.height = emblemImage.naturalHeight;
  const sampleContext = sampler.getContext("2d", { willReadFrequently: true });
  if (!sampleContext) return;
  let pixels;
  try {
    sampleContext.drawImage(emblemImage, 0, 0);
    pixels = sampleContext.getImageData(0, 0, sampler.width, sampler.height).data;
  } catch {
    return;
  }
  const scale = imageBounds.width / sampler.width;
  const points = [];
  const step = window.innerWidth > 760 ? 2 : 3;
  for (let y = 0; y < sampler.height; y += step) {
    for (let x = 0; x < sampler.width; x += step) {
      const index = (y * sampler.width + x) * 4;
      const light = (pixels[index] + pixels[index + 1] + pixels[index + 2]) / 765;
      if (light < .3) continue;
      const px = (x - sampler.width / 2) * scale;
      const py = (y - sampler.height / 2) * scale;
      const phase = Math.atan2(py, px);
      points.push({ x: px, y: py, light, phase, depth: Math.sin(x * .17 + y * .11) });
    }
  }
  let started;
  const draw = (time) => {
    if (reducedMotion.matches || document.hidden) return stopEmblem();
    started ??= time;
    const progress = Math.min((time - started) / 3000, 1);
    const settle = Math.pow(1 - progress, 2);
    const fade = Math.min(progress * 7, 1) * Math.min((1 - progress) * 5, 1);
    context.clearRect(0, 0, bounds.width, bounds.height);
    const resolve = Math.max(0, Math.min((progress - .4) / .5, 1));
    emblemImage.style.opacity = String(.24 + .76 * resolve * resolve * (3 - 2 * resolve));
    for (const point of points) {
      const turn = settle * 1.1 * point.depth;
      const drift = settle * (12 + 22 * point.light);
      const x = point.x * Math.cos(turn) - point.y * Math.sin(turn) + Math.cos(point.phase) * drift;
      const y = point.x * Math.sin(turn) + point.y * Math.cos(turn) + Math.sin(point.phase) * drift * .65;
      const sweep = Math.max(0, 1 - Math.abs((point.x + point.y * .45) / 130 - (progress * 2.8 - 1.4)) * 3);
      const alpha = fade * (.6 + sweep * .4) * point.light;
      context.fillStyle = `rgba(224,233,241,${alpha})`;
      context.fillRect(bounds.width / 2 + x, bounds.height / 2 + y, 1 + settle * .7, 1 + settle * .7);
    }
    if (progress < 1) emblemFrame = requestAnimationFrame(draw);
    else stopEmblem();
  };
  emblemFrame = requestAnimationFrame(draw);
};

if (emblemImage?.complete) playEmblem();
else emblemImage?.addEventListener("load", playEmblem, { once: true });
reducedMotion.addEventListener("change", () => {
  if (reducedMotion.matches) stopEmblem();
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden) stopEmblem();
});
window.addEventListener("resize", stopEmblem, { passive: true });
