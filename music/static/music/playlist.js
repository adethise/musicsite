playlist = {
	load() {
		this.songs = JSON.parse(localStorage.playlist || "[]");
		this.draw();
	},
	draw() {
		var panel = document.getElementById("playlist-panel");
		panel.innerHTML = "";
		for (i in this.songs) {
			panel.innerHTML += songToNode(this.songs[i], i);
		}
		this.updateItemsCount();
	},
	updateItemsCount() {
		document.getElementById("playlist-item-count").innerHTML =
			this.songs.length + " songs in the playlist";
	},
	add(id) {
		var song = new Song(id);
		this.songs.push(song);
		localStorage.playlist = JSON.stringify(this.songs);
		document.getElementById("playlist-panel").innerHTML +=
			songToNode(song, this.songs.length - 1);
		this.updateItemsCount();
	},
	addAll() {
		var songs = document.getElementsByClassName("search-result");
		for (s = 0 ; s < songs.length ; s++) {
			this.add(songs[s].id);
		}
	},
	remove(pos) {
		this.songs.splice(pos, 1);
		this.draw();
		/*var node = document.getElementById("playlist-item-" + pos);
		node.parentNode.removeChild(node);*/
		localStorage.playlist = JSON.stringify(this.songs);
	},
	removeAll() {
		this.songs = [];
		this.draw();
		localStorage.playlist = JSON.stringify(this.songs);
	},
	startRandomSong() {
		if (this.songs.length > 0) {
			var idx = Math.floor(Math.random() * this.songs.length);
			playlist.playSong(this.songs[idx]);
		}
	},
	playSong(song) {
		document.getElementById("player-panel-song").classList.remove("hidden");
		document.getElementById("player-song-name").innerHTML = song.name;
		document.getElementById("player-song-artist").innerHTML = song.artist;

		var playersource = document.getElementById("player-song-source");
		playersource.innerHTML = song.source
		if (song.source)
			playersource.parentNode.classList.remove("hidden");
		else
			playersource.parentNode.classList.add("hidden");

		var playercategory = document.getElementById("player-song-category");
		playercategory.innerHTML = song.category
		if (song.category)
			playersource.parentNode.classList.remove("hidden");
		else
			playersource.parentNode.classList.add("hidden");

		var player = document.getElementById("player");
		player.innerHTML = "<source src=\"" + song.filepath + "\" type=\"" + song.mime + "\">";

		player.load();
		player.focus();
	}
};

function Song(id) {
	var node = document.getElementById(id);
	this.name     = node.getElementsByClassName("song-name")[0].innerHTML;
	this.artist   = node.getElementsByClassName("song-artist")[0].innerHTML;
	this.source   = node.getElementsByClassName("song-source")[0].innerHTML;
	this.category = node.getElementsByClassName("song-category")[0].innerHTML;
	this.filepath = node.getElementsByClassName("song-filepath")[0].innerHTML;
	this.mime     = node.getElementsByClassName("song-mime")[0].innerHTML;
	this.link     = node.getElementsByTagName("a")[0].href;
}

function songToNode(song, pos) {
	return (
"    <div id=\"playlist-item-" + pos + "\" class=\"panel panel-default panel-body song-panel\">\n" +
"        <p>\n" +
"            <a href=\"" + song.link + "\" class=\"song-link-block\">\n" +
"                <span class=\"song-name\">" + song.name + "</span>\n" +
"                <br>\n" +
"                <span class=\"song-artist\">" + song.artist + "</span>\n" +
"                <span class=\"song-source\">" + song.source + "</span>\n" +
"            </a>\n" +
"            <button class=\"pull-right\" onClick=\"playlist.remove(" + pos + ");\">-</button>\n" +
"        </p>\n" +
"    </div>\n");
};

window.addEventListener("load", function() {
	playlist.load();
});
