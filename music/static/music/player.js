window.addEventListener("load", function() {
	var player = document.getElementById("player");
	player.focus();
	if (localStorage.volume && isFinite(localStorage.volume)) {
		player.volume = localStorage.volume;
	}
});

function startRandomSong() {
	window.location= "random" + window.location.search;
}

function storeVolume() {
	var player = document.getElementById("player");
	localStorage.volume = player.volume;
}
