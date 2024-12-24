document.addEventListener("DOMContentLoaded", () => {
    const toggleModeButton = document.getElementById("toggle-mode");
    const body = document.body;
    const appTitle = document.getElementById("app-title");

    // Cargar modo guardado
    const savedMode = localStorage.getItem("theme");
    if (savedMode) {
        body.classList.add(savedMode);
        updateButtonText(savedMode);
    }

    // Cambiar entre modos
    toggleModeButton.addEventListener("click", () => {
        const currentMode = body.classList.contains("light-mode") ? "dark-mode" : "light-mode";
        body.classList.toggle("light-mode");
        localStorage.setItem("theme", currentMode);
        updateButtonText(currentMode);
    });

    function updateButtonText(mode) {
        toggleModeButton.textContent = mode === "light-mode" ? "Cambiar a modo oscuro" : "Cambiar a modo claro";
    }
});
