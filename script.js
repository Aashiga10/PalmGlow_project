function filterDesign(category) {

    let cards = document.getElementsByClassName("card");

    for (let i = 0; i < cards.length; i++) {

        cards[i].style.display = "none";

        if (category === "all" || cards[i].classList.contains(category)) {
            cards[i].style.display = "block";
        }
    }
}
