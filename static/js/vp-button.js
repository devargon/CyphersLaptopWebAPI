const button = document.getElementById("vp-button");
button.addEventListener("touchstart", moveButton);
button.addEventListener("mouseover", moveButton);

var count = 0;
var counter = document.getElementById('minty');

function moveButton(event) {
    // Keep the whole button on screen
    button.style.position = "fixed";
    button.style.top = Math.floor(Math.random() * (window.innerHeight - button.offsetHeight)) + "px";
    button.style.left = Math.floor(Math.random() * (window.innerWidth - button.offsetWidth)) + "px";
    count += 1;
    counter.textContent = `You tried getting free VP ${count} times`;
}

// The button runs from the mouse, so anyone who manages to click it must be cheating
var cheater = document.getElementById('cheater');

button.addEventListener("click", function () {
    cheater.hidden = false;
    cheater.querySelector('.cheater-continue').focus();
});

document.getElementById('cheater-back').addEventListener("click", function () {
    cheater.hidden = true;
    button.focus();
});
