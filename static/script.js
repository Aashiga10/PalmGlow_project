function filterDesign(category) {

    let cards = document.getElementsByClassName("card");

    for (let i = 0; i < cards.length; i++) {

        cards[i].style.display = "none";

        if (category === "all" || cards[i].classList.contains(category)) {
            cards[i].style.display = "block";
        }
    }
}
function calculatePrice() {

    let design = parseInt(document.getElementById("design").value);
    let length = parseInt(document.getElementById("length").value);
    let glitter = document.getElementById("glitter");

    let total = design + length;

    if (glitter.checked) {
        total += parseInt(glitter.value);
    }
    document.getElementById("totalInput").value = total;
    document.getElementById("total").innerText = total;
}
