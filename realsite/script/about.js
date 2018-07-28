var tabs = ["officers", "board"];

hideAllTabs();
document.getElementById(tabs[0] + "-tab").style.display = "block";

for (var i in tabs) {
	setOnClick(tabs[i]);
}

function setOnClick(id) {
	document.getElementById(id + "-select").onclick = function() {
		hideAllTabs();
		document.getElementById(id + "-tab").style.display = "block";
	}
}
	

function hideAllTabs() {
	for (var i in tabs) {
		document.getElementById(tabs[i] + "-tab").style.display = "none";
	}
}