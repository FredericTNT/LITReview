const modal = document.getElementById("myModal");

function initListener() {
	document.getElementById("help").addEventListener('click', function() {modal.style.display = 'block';});
	document.getElementsByClassName("close")[0].addEventListener('click', function() {modal.style.display = "none";});
};

function onLoaded(event) {
	initListener();
};

document.addEventListener('DOMContentLoaded', onLoaded);
