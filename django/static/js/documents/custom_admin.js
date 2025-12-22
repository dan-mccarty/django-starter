(function () {
  document.addEventListener("DOMContentLoaded", function () {
    const originalInput = document.querySelector("#id_original");
    const slugInput = document.querySelector("#id_slug");

    if (!originalInput || !slugInput) return;

    originalInput.addEventListener("input", function () {
      const inputText = originalInput.value;

      // Remove extension
      let base = inputText.replace(/\.[^/.]+$/, "");

      // Replace underscores with spaces
      base = base.replace(/_/g, " ");

      // Lowercase
      base = base.toLowerCase();

      // Replace multiple whitespace → single
      base = base.replace(/\s+/g, " ");

      // Replace spaces → hyphens
      base = base.replace(/ /g, "-");

      // Remove unsafe URL characters
      base = base.replace(/[^a-z0-9\-]/g, "");

      slugInput.value = base;
    });
  });
})();
