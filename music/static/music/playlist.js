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
	},
	add(id) {
		var song = new Song(id);
		this.songs.push(song);
		localStorage.playlist = JSON.stringify(this.songs);
		document.getElementById("playlist-panel").innerHTML +=
			songToNode(song, this.songs.length - 1);
	},
	remove(pos) {
		this.songs.splice(pos, 1);
		this.draw();
		/*var node = document.getElementById("playlist-item-" + pos);
		node.parentNode.removeChild(node);*/
		localStorage.playlist = JSON.stringify(this.songs);
	},
	startRandomSong() {
		var idx = Math.floor(Math.random() * this.songs.length);
		window.location = this.songs[idx].link + window.location.search;
	}
};

function Song(id) {
	var node = document.getElementById(id);
	this.name     = node.getElementsByClassName("song-name")[0].innerHTML;
	this.artist   = node.getElementsByClassName("song-artist")[0].innerHTML;
	this.source   = node.getElementsByClassName("song-source")[0].innerHTML;
	this.category = node.getElementsByClassName("song-category")[0].innerHTML;
	this.link     = node.getElementsByTagName("a")[0].href;
}

function songToNode(song, pos) {
	return (
"<div id=\"playlist-item-" + pos + "\">\n" +
"    <div class=\"panel panel-default panel-body song-link-block\">\n" +
"        <p>\n" +
"            <a href=\"" + song.link + "\" class=\"song-link-block\">\n" +
"                <span class=\"song-name\">" + song.name + "</span>\n" +
"                <br>\n" +
"                <span class=\"song-artist\">" + song.artist + "</span>\n" +
"                <span class=\"song-source\">" + song.source + "</span>\n" +
"            </a>\n" +
"            <button class=\"pull-right\" onClick=\"playlist.remove(" + pos + ");\">-</button>\n" +
"        </p>\n" +
"    </div>\n" +
"</div>\n");
};

window.addEventListener("load", function() {
	playlist.load();
});
