(function () {
    const currentScript = document.currentScript;
    const scriptOrigin = new URL(currentScript.src).origin;

    const iframe = document.createElement("iframe");
    iframe.src = scriptOrigin + "/ads/render/";  // this replaces hardcoded 127.0.0.1

    iframe.style.position = "fixed";
    iframe.style.bottom = "20px";
    iframe.style.right = "20px";
    iframe.style.width = "300px";
    iframe.style.height = "250px";
    iframe.style.border = "none";
    iframe.style.zIndex = "9999";
    iframe.style.boxShadow = "0 4px 12px rgba(0, 0, 0, 0.2)";
    iframe.setAttribute("id", "customAdWidget");

    document.body.appendChild(iframe);

    // Close button script
    window.addEventListener("message", function (event) {
        if (event.data === "closeAd") {
            const ad = document.getElementById("customAdWidget");
            if (ad) ad.remove();
        }
    });
})();
