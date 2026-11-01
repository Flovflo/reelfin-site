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
      const { top, bottom } = element.getBoundingClientRect();
      // A first callback can follow restored scroll, an anchor, or a fast jump.
      // Never fade content that has already reached the visible viewport.
      if (top < window.innerHeight && bottom > 0) {
        playedReveals.add(element);
        revealObserver.unobserve(element);
        continue;
      }
      const group = element.parentElement;
      const isRow = group?.matches(".duo-stage, .feature-grid, .tv-benefits");
      const index = isRow ? [...group.children].indexOf(element) : 0;
      const delay = window.innerWidth > 760 ? Math.min(index * 75, 150) : 0;
      reveal(element, { delay });
      revealObserver.unobserve(element);
    }
  }, { threshold: 0, rootMargin: "64px 0px 64px 0px" });
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

// The emblem is made of dust. On arrival its grains drift in and settle into
// the rings, scrolling scatters them, and they gather again above the closing
// call to action. Hovering the picture breaks it into no-signal static.
// The original PNGs are always present: without JS, canvas or motion they are
// simply the emblem, and the dust only ever covers what it has hidden.
const dustStages = [...document.querySelectorAll(".hero-emblem, .cta-emblem")];
const dustImages = dustStages.map((stage) => stage.querySelector("img"));
const clampUnit = (value) => Math.min(1, Math.max(0, value));
const ease = (value) => { const t = clampUnit(value); return t * t * (3 - 2 * t); };
let pointerX = -1e4;
let pointerY = -1e4;

const startDust = () => {
  const source = dustImages[0];
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");
  if (!context) return;
  const sampler = document.createElement("canvas");
  const columns = window.innerWidth < 700 ? 110 : 150;
  const rows = Math.round(columns * source.naturalHeight / source.naturalWidth);
  sampler.width = columns;
  sampler.height = rows;
  const sampleContext = sampler.getContext("2d", { willReadFrequently: true });
  let pixels;
  try {
    sampleContext.drawImage(source, 0, 0, columns, rows);
    pixels = sampleContext.getImageData(0, 0, columns, rows).data;
  } catch {
    return;
  }
  const grains = [];
  for (let y = 0; y < rows; y++) {
    for (let x = 0; x < columns; x++) {
      const index = (y * columns + x) * 4;
      const light = (pixels[index] + pixels[index + 1] + pixels[index + 2]) / 765;
      if (light < .2) continue;
      const angle = Math.random() * Math.PI * 2;
      const distance = .5 + Math.random() * .9;
      grains.push({
        u: (x + .5) / columns - .5, v: (y + .5) / rows - .5, alpha: Math.min(1, light * 1.7), solid: light > .42,
        sx: Math.cos(angle) * distance, sy: Math.sin(angle) * distance * .7 - .25,
        x: 0, y: 0, vx: 0, vy: 0, noise: Math.random(), seed: Math.random() * 100, spin: Math.random() - .5,
      });
    }
  }

  canvas.className = "dust";
  canvas.setAttribute("aria-hidden", "true");
  document.body.append(canvas);
  const light = document.createElement("div");
  light.className = "cursor-light";
  light.setAttribute("aria-hidden", "true");
  document.body.append(light);
  document.documentElement.classList.add("has-dust");
  const brandMark = document.querySelector(".site-header .brand__mark");

  let width = 0;
  let height = 0;
  let ratio = 1;
  let frame = 0;
  let started = 0;
  let smoothScroll = window.scrollY;
  let activeStage = -1;
  let lastLeft = 0;
  let lastTop = 0;
  let arrival = 0;
  let hover = 0;
  let hoverTarget = 0;
  let lightX = window.innerWidth / 2;
  let lightY = window.innerHeight / 2;
  let noiseOffset = 0;
  let docked = null;
  let idle = false;

  const resize = () => {
    width = document.documentElement.clientWidth;
    height = window.innerHeight;
    ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(width * ratio);
    canvas.height = Math.round(height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
  };
  const scatterAround = (bounds) => {
    const spread = bounds.width * 1.3 + width * .3;
    for (const grain of grains) {
      grain.x = bounds.left + bounds.width / 2 + grain.u * bounds.width + grain.sx * spread;
      grain.y = bounds.top + bounds.height / 2 + grain.v * bounds.height + grain.sy * spread;
      grain.vx = 0;
      grain.vy = 0;
    }
  };
  const stop = () => {
    cancelAnimationFrame(frame);
    frame = 0;
    canvas.remove();
    light.remove();
    document.documentElement.classList.remove("has-dust");
    brandMark?.classList.remove("is-docked");
    dustImages.forEach((image) => image.style.removeProperty("opacity"));
    dustStages.forEach((stage) => stage.classList.remove("is-live"));
  };

  dustStages.forEach((stage) => {
    stage.addEventListener("pointerenter", (event) => { if (event.pointerType === "mouse") hoverTarget = 1; });
    stage.addEventListener("pointerleave", () => { hoverTarget = 0; });
  });

  const draw = (time) => {
    frame = requestAnimationFrame(draw);
    started ||= time;
    const seconds = (time - started) / 1000;
    const intro = ease((seconds - .15) / 1.9);
    smoothScroll += (window.scrollY - smoothScroll) * .12;
    const lag = window.scrollY - smoothScroll;
    lightX += (pointerX - lightX) * .08;
    lightY += (pointerY - lightY) * .08;
    light.style.transform = `translate(${lightX}px, ${lightY}px)`;

    // Each stage has a presence: the hero fades over the first scroll, the
    // closing emblem gathers as it rises into view.
    const first = dustImages[0].getBoundingClientRect();
    const last = dustImages[1]?.getBoundingClientRect();
    const firstCentre = first.top + first.height / 2 + lag;
    const lastCentre = last ? last.top + last.height / 2 + lag : Infinity;
    const firstPresence = 1 - Math.pow(clampUnit(window.scrollY / 320), 1.15);
    const lastPresence = last ? ease((height * 1.2 - lastCentre) / (height * .42)) : 0;
    const useFirst = firstCentre > -first.height * .5 && firstPresence > .001 && (firstPresence >= lastPresence || lastCentre > height);
    const stage = useFirst ? 0 : 1;
    const bounds = useFirst ? first : last;

    if (stage === activeStage) {
      // Grains travel with the page while it scrolls.
      const dx = bounds.left - lastLeft;
      const dy = bounds.top - lastTop;
      if (dx || dy) for (const grain of grains) { grain.x += dx; grain.y += dy; }
    } else {
      if (activeStage !== -1) arrival = 0;
      activeStage = stage;
      scatterAround(bounds);
    }
    lastLeft = bounds.left;
    lastTop = bounds.top;
    arrival = Math.min(1, arrival + .03);

    const presence = (useFirst ? firstPresence : lastPresence) * intro;
    const settled = ease(presence);
    const picture = ease((presence - .86) / .14);
    const dust = 1 - picture;
    hover += (hoverTarget - hover) * .07;
    const snow = ease(hover);
    dustImages.forEach((image, index) => { image.style.opacity = String(index === stage ? picture : 0); });
    dustStages.forEach((element, index) => element.classList.toggle("is-live", index === stage && picture > .9));
    const dock = !useFirst || firstPresence < .35;
    if (dock !== docked) { docked = dock; brandMark?.classList.toggle("is-docked", dock); }

    // Nothing to draw once the picture is whole and nobody touches it.
    const quiet = dust < .01 && snow < .01;
    if (quiet && idle) return;
    idle = quiet;
    context.clearRect(0, 0, width, height);
    if (quiet) return;

    for (let i = noiseOffset; i < grains.length; i += 3) grains[i].noise = Math.random();
    noiseOffset = (noiseOffset + 1) % 3;
    const size = Math.max(1.6, bounds.width / columns * 1.05);
    const loose = Math.pow(clampUnit((.97 - settled) / .97), 1.3);
    const spread = bounds.width * .5 + width * .22;
    const centreX = bounds.left + bounds.width / 2;
    const centreY = bounds.top + bounds.height / 2;
    const reach = Math.max(bounds.height * .62, 60);
    for (const grain of grains) {
      const homeX = centreX + grain.u * bounds.width;
      const homeY = centreY + grain.v * bounds.height;
      const wobble = Math.sin(seconds * .8 + grain.seed) * 6 * loose;
      const targetX = homeX * (1 - loose) + (homeX + grain.sx * spread + wobble) * loose;
      const targetY = homeY * (1 - loose) + (homeY + grain.sy * spread + seconds * grain.spin * 10 + wobble) * loose;
      const pull = .05 + .06 * settled;
      grain.vx = (grain.vx + (targetX - grain.x) * pull) * .76;
      grain.vy = (grain.vy + (targetY - grain.y) * pull) * .76;
      // Loose dust parts around the pointer.
      const awayX = grain.x - pointerX;
      const awayY = grain.y - pointerY;
      const away = awayX * awayX + awayY * awayY;
      if (snow < .01 && away < 14400 && settled < .98) {
        const distance = Math.sqrt(away) || 1;
        const force = (1 - distance / 120) * 2.6 * (1 - settled * .6);
        grain.vx += awayX / distance * force;
        grain.vy += awayY / distance * force;
      }
      grain.x += grain.vx;
      grain.y += grain.vy;

      if (snow > .01 && picture > .5) {
        // A soft patch of no-signal static follows the pointer over the rings.
        if (!grain.solid || away > reach * reach) continue;
        const near = 1 - Math.sqrt(away) / reach;
        const grey = Math.floor(grain.noise * grain.noise * 190 + 20);
        context.fillStyle = `rgb(${grey} ${grey} ${grey})`;
        context.globalAlpha = near * near * snow * .95;
        context.fillRect(grain.x - size / 2, grain.y - size / 2, size, size);
        continue;
      }
      if (dust < .02 || grain.y < -20 || grain.y > height + 20 || grain.x < -20 || grain.x > width + 20) continue;
      context.fillStyle = "#fff";
      context.globalAlpha = (grain.alpha + (grain.solid ? .16 : 0) * loose) * dust * (.55 + .45 * settled) * (.3 + .7 * intro) * (.85 + .15 * grain.noise) * ease(arrival);
      const grainSize = size * (.75 + .25 * settled);
      context.fillRect(grain.x - grainSize / 2, grain.y - grainSize / 2, grainSize, grainSize);
    }
    context.globalAlpha = 1;
  };

  resize();
  window.addEventListener("resize", resize, { passive: true });
  reducedMotion.addEventListener("change", () => { if (reducedMotion.matches) stop(); });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) { cancelAnimationFrame(frame); frame = 0; }
    else if (!frame && canvas.isConnected) frame = requestAnimationFrame(draw);
  });
  frame = requestAnimationFrame(draw);

  // The heading under the rings arrives once they have settled.
  if (!reducedMotion.matches) {
    document.querySelectorAll(".mosaic__brand-copy h1, .mosaic__brand-copy > p:first-of-type").forEach((element, index) => {
      element.animate?.([{ opacity: 0, filter: "blur(10px)", transform: "translateY(10px)" }, { opacity: 1, filter: "blur(0)", transform: "none" }],
        { duration: 1100, delay: 1300 + index * 140, easing: "cubic-bezier(.16, 1, .3, 1)", fill: "backwards" });
    });
  }
};

window.addEventListener("pointermove", (event) => {
  if (event.pointerType !== "mouse") return;
  pointerX = event.clientX;
  pointerY = event.clientY;
  document.documentElement.classList.add("has-pointer");
}, { passive: true });
document.documentElement.addEventListener("pointerleave", () => { pointerX = pointerY = -1e4; });

if (dustImages[0] && !reducedMotion.matches) {
  // Both stages show the same file, so the hero's copy is enough to sample.
  if (dustImages[0].complete && dustImages[0].naturalWidth) startDust();
  else dustImages[0].addEventListener("load", startDust, { once: true });
}

// Section titles decode through screen glyphs as they arrive, left to right.
// Only text nodes change, so inline markup and the final text stay intact.
const GLYPHS = "▓▒░█▌▐│┃0123456789ABCDEFXK#%&*+";
const decode = (heading) => {
  const walker = document.createTreeWalker(heading, NodeFilter.SHOW_TEXT);
  const nodes = [];
  while (walker.nextNode()) nodes.push({ node: walker.currentNode, text: walker.currentNode.nodeValue });
  const total = nodes.reduce((sum, item) => sum + item.text.length, 0);
  if (!total) return;
  heading.setAttribute("aria-label", heading.textContent);
  const begin = performance.now();
  const tick = (now) => {
    const progress = Math.min(1, (now - begin) / 800);
    let settled = Math.floor(progress * total);
    for (const item of nodes) {
      let out = "";
      for (const char of item.text) {
        out += settled > 0 || /\s/.test(char) ? char : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
        settled -= 1;
      }
      item.node.nodeValue = out;
    }
    if (progress < 1) requestAnimationFrame(tick);
    else {
      nodes.forEach((item) => { item.node.nodeValue = item.text; });
      heading.removeAttribute("aria-label");
    }
  };
  requestAnimationFrame(tick);
};
if (!reducedMotion.matches && "IntersectionObserver" in window) {
  const decodeObserver = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      decodeObserver.unobserve(entry.target);
      decode(entry.target);
    }
  }, { threshold: .4 });
  document.querySelectorAll(".section-heading h2, .download-band h2, .compatibility h2, .faq h2, .final-cta h2").forEach((heading) => decodeObserver.observe(heading));
}

// Native scrolling selects UI states inside stationary Apple product artwork.
// Without JS, on mobile, and with reduced motion the three HTML chapters remain
// an ordinary page, each with its own complete static product image.
const story = document.querySelector(".product-story");
if (story) {
  const wideStory = window.matchMedia("(min-width: 1100px)");
  const chapters = [...story.querySelectorAll(".story__chapter")];
  const links = [...story.querySelectorAll("[data-story-link]")];
  const tvScreen = story.querySelector(".story__screen--tv");
  const phoneScreen = story.querySelector(".story__screen--phone");
  let storyFrame = 0;
  const clamp = (value) => Math.min(1, Math.max(0, value));
  const smooth = (value) => { const t = clamp(value); return t * t * (3 - 2 * t); };
  const requestScreen = (image) => {
    if (!image || image.dataset.requested) return;
    image.dataset.requested = "true";
    image.srcset = image.dataset.storySrcset;
    image.src = image.dataset.storySrc;
    image.decode().then(() => {
      image.dataset.ready = "true";
      image.hidden = false;
      scheduleStory();
    }).catch(() => {});
  };
  const updateStory = () => {
    storyFrame = 0;
    const enhanced = wideStory.matches && !reducedMotion.matches;
    story.classList.toggle("has-scroll-story", enhanced);
    if (!enhanced) return;
    const first = chapters[0].getBoundingClientRect();
    const last = chapters[chapters.length - 1].getBoundingClientRect();
    const anchorLine = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop) || 110;
    const progress = clamp((anchorLine - first.top) / (last.top - first.top));
    const storyBounds = story.getBoundingClientRect();
    const nearStory = storyBounds.top < window.innerHeight + 400 && storyBounds.bottom > 0;
    if (nearStory && first.top < window.innerHeight) requestScreen(tvScreen);
    if (nearStory && progress > .32) requestScreen(phoneScreen);
    story.style.setProperty("--story-progress", progress);
    story.style.setProperty("--tv-ui", tvScreen?.dataset.ready ? smooth((progress - .16) / .28) : 0);
    story.style.setProperty("--phone-ui", phoneScreen?.dataset.ready ? smooth((progress - .56) / .3) : 0);
    const active = Math.round(progress * (chapters.length - 1));
    links.forEach((link, index) => {
      if (index === active) link.setAttribute("aria-current", "step");
      else link.removeAttribute("aria-current");
    });
    chapters.forEach((chapter, index) => {
      const emphasis = 1 - Math.min(1, Math.abs(progress * 2 - index));
      const shade = Math.round(166 + emphasis * 81);
      chapter.style.setProperty("--chapter-color", `rgb(${shade} ${shade} ${shade})`);
    });
    story.querySelector(".story__counter").textContent = `0${active + 1} / 03`;
  };
  const scheduleStory = () => {
    if (!storyFrame) storyFrame = requestAnimationFrame(updateStory);
  };
  window.addEventListener("scroll", scheduleStory, { passive: true });
  window.addEventListener("resize", scheduleStory, { passive: true });
  wideStory.addEventListener("change", scheduleStory);
  reducedMotion.addEventListener("change", scheduleStory);
  updateStory();
}
