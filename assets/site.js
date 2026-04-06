const root = document.documentElement;
const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

if (root) {
  let ticking = false;

  const updateScrollChrome = () => {
    ticking = false;

    const maxScroll = Math.max(root.scrollHeight - window.innerHeight, 1);
    const progress = Math.min(Math.max(window.scrollY / maxScroll, 0), 1);

    root.style.setProperty("--scroll-progress", progress.toFixed(4));
  };

  const requestUpdate = () => {
    if (ticking) {
      return;
    }

    ticking = true;
    window.requestAnimationFrame(updateScrollChrome);
  };

  const getTargetFromHash = (hash) => {
    if (!hash || hash.length < 2) {
      return null;
    }

    const targetId = decodeURIComponent(hash.slice(1));
    return document.getElementById(targetId);
  };

  const snapToHashTarget = () => {
    const target = getTargetFromHash(window.location.hash);

    if (!target) {
      requestUpdate();
      return;
    }

    target.scrollIntoView({
      behavior: "auto",
      block: "start",
    });
    requestUpdate();
  };

  const isSamePageHashLink = (link) => {
    if (!(link instanceof HTMLAnchorElement)) {
      return false;
    }

    const url = new URL(link.href, window.location.href);

    return (
      Boolean(url.hash) &&
      url.origin === window.location.origin &&
      url.pathname === window.location.pathname
    );
  };

  const bindSmoothInPageLinks = () => {
    const links = document.querySelectorAll("a[href]");

    for (const link of links) {
      if (!isSamePageHashLink(link)) {
        continue;
      }

      link.addEventListener("click", (event) => {
        const target = getTargetFromHash(new URL(link.href, window.location.href).hash);

        if (!target) {
          return;
        }

        event.preventDefault();

        if (window.location.hash !== link.hash) {
          history.pushState(null, "", link.hash);
        }

        target.scrollIntoView({
          behavior: prefersReducedMotion.matches ? "auto" : "smooth",
          block: "start",
        });
        requestUpdate();
      });
    }
  };

  bindSmoothInPageLinks();
  snapToHashTarget();
  window.addEventListener("load", snapToHashTarget, { once: true });
  window.addEventListener("pageshow", snapToHashTarget);
  updateScrollChrome();
  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
  window.addEventListener("load", requestUpdate);
}
