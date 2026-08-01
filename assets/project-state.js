(() => {
  const storagePrefix = "publication-project-open:";

  for (const details of document.querySelectorAll("details.project[data-project-state]")) {
    const storageKey = `${storagePrefix}${details.dataset.projectState}`;

    try {
      const savedState = window.localStorage.getItem(storageKey);
      if (savedState === "open") {
        details.open = true;
      } else if (savedState === "closed") {
        details.open = false;
      }
    } catch {
      // Browsers can disable localStorage in restricted privacy modes.
    }

    details.addEventListener("toggle", () => {
      try {
        window.localStorage.setItem(storageKey, details.open ? "open" : "closed");
      } catch {
        // The disclosure control still works when persistence is unavailable.
      }
    });
  }
})();
