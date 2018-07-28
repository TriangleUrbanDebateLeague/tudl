var tabs = ["officers", "board"];

hideAllTabs();
document.getElementById(tabs[0] + "-tab").style.display = "block";
document.getElementById(tabs[0] + "-select").classList.add("selected");

for (var i in tabs) {
	setOnClick(tabs[i]);
}

function setOnClick(id) {
	document.getElementById(id + "-select").onclick = function() {
		hideAllTabs();
		document.getElementById(id + "-tab").style.display = "block";
		document.getElementById(id + "-select").classList.add("selected");
	}
}
	

function hideAllTabs() {
	for (var i in tabs) {
		document.getElementById(tabs[i] + "-tab").style.display = "none";
		document.getElementById(tabs[i] + "-select").classList.remove("selected");
	}
}