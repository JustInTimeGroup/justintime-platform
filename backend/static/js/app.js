(() => {
  const root = document.documentElement;
  const body = document.body;

  const toggleBtn = document.getElementById("menuToggle");
  const closeBtn = document.getElementById("menuClose");
  const overlay = document.getElementById("mobileOverlay");
  const drawer = document.getElementById("mobileDrawer");

  if (!toggleBtn || !overlay || !drawer) return;

  let lastScrollY = 0;

  const focusableSelector =
    'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])';

  const getFocusable = () => Array.from(drawer.querySelectorAll(focusableSelector));

  const lockScroll = () => {
    // iOS/Safari-safe scroll lock: freeze body position and preserve scroll
    lastScrollY = window.scrollY || window.pageYOffset || 0;
    body.style.position = "fixed";
    body.style.top = `-${lastScrollY}px`;
    body.style.left = "0";
    body.style.right = "0";
    body.style.width = "100%";
    body.classList.add("no-scroll");
  };

  const unlockScroll = () => {
    body.classList.remove("no-scroll");
    body.style.position = "";
    body.style.top = "";
    body.style.left = "";
    body.style.right = "";
    body.style.width = "";

    // Restore scroll position
    window.scrollTo(0, lastScrollY);
  };

  const setOpen = (open) => {
    if (open) {
      root.classList.add("menu-open");
      overlay.hidden = false;

      drawer.setAttribute("aria-hidden", "false");
      toggleBtn.setAttribute("aria-expanded", "true");
      toggleBtn.setAttribute("aria-label", "Close menu");

      lockScroll();

      // Move focus into the drawer
      const focusables = getFocusable();
      (focusables[0] || drawer).focus?.();
    } else {
      root.classList.remove("menu-open");
      overlay.hidden = true;

      drawer.setAttribute("aria-hidden", "true");
      toggleBtn.setAttribute("aria-expanded", "false");
      toggleBtn.setAttribute("aria-label", "Open menu");

      unlockScroll();

      // Return focus to the toggle button
      toggleBtn.focus();
    }
  };

  const isOpen = () => root.classList.contains("menu-open");

  // Toggle open/close
  toggleBtn.addEventListener("click", () => setOpen(!isOpen()));
  if (closeBtn) closeBtn.addEventListener("click", () => setOpen(false));

  // Close when overlay (page behind) is clicked
  overlay.addEventListener("click", () => setOpen(false));

  // Close when any drawer link is clicked
  drawer.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) setOpen(false);
  });

  // Keyboard support: Esc closes + focus trap on Tab
  document.addEventListener("keydown", (e) => {
    if (!isOpen()) return;

    if (e.key === "Escape") {
      e.preventDefault();
      setOpen(false);
      return;
    }

    if (e.key === "Tab") {
      const focusables = getFocusable();
      if (focusables.length === 0) return;

      const first = focusables[0];
      const last = focusables[focusables.length - 1];

      // If focus is outside drawer, bring it in
      if (!drawer.contains(document.activeElement)) {
        e.preventDefault();
        first.focus();
        return;
      }

      // Loop focus
      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  });

  // Defensive: if viewport becomes desktop while menu is open, close it
  const mq = window.matchMedia("(min-width: 900px)");
  const handleMq = () => {
    if (mq.matches && isOpen()) setOpen(false);
  };
  mq.addEventListener?.("change", handleMq);
})();