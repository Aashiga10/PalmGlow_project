console.log("Palm Glow JS Loaded");

function filterDesign(category) {
    let designCards = document.querySelectorAll(".design-card");

    designCards.forEach(card => {
        let col = card.closest(".col-12") || card;
        if (category === "all" || card.classList.contains(category)) {
            col.style.display = "";
        } else {
            col.style.display = "none";
        }
    });

    // Update button styling to highlight active filter
    let buttons = document.querySelectorAll(".filter-btn");
    buttons.forEach(btn => {
        let filterVal = btn.getAttribute("data-filter");
        if (filterVal === category) {
            btn.classList.remove("btn-outline-warning");
            btn.classList.add("btn-warning");
        } else {
            btn.classList.remove("btn-warning");
            btn.classList.add("btn-outline-warning");
        }
    });
}

function calculatePrice() {
    let designElem = document.getElementById("design");
    let lengthElem = document.getElementById("length");
    let glitterElem = document.getElementById("glitter");
    let totalInput = document.getElementById("totalInput");
    let totalDisplay = document.getElementById("total");

    // Only run if we are on the customized booking page
    if (!designElem || !lengthElem) return;

    let design = parseInt(designElem.value) || 0;
    let length = parseInt(lengthElem.value) || 0;
    let total = design + length;

    if (glitterElem && glitterElem.checked) {
        total += parseInt(glitterElem.value) || 0;
    }

    if (totalInput) totalInput.value = total;
    if (totalDisplay) totalDisplay.innerText = total;
}

window.onload = function () {
    if (document.getElementById("design")) {
        calculatePrice();
    }

    // Click to enlarge design images in modal
    let previewModal = document.getElementById("imageModal");
    let previewImg = document.getElementById("modalPreviewImg");
    if (previewModal && previewImg && typeof bootstrap !== "undefined") {
        let bsModal = new bootstrap.Modal(previewModal);
        document.querySelectorAll(".design-card img").forEach(img => {
            img.style.cursor = "zoom-in";
            img.title = "Click to view full image";
            img.addEventListener("click", function () {
                previewImg.src = this.src;
                bsModal.show();
            });
        });
    }
};
