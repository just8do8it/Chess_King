function overlayOn(text) {
	document.getElementById("text").innerHTML = text;
	document.getElementById("overlay").style.display = "block";
}
function overlayOff() {
	document.getElementById("overlay").style.display = "none";
}
