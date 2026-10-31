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
const updateHeader = () => header?.classList.toggle("is-scrolled", window.scrollY > 12);
updateHeader();
window.addEventListener("scroll", updateHeader, { passive: true });
