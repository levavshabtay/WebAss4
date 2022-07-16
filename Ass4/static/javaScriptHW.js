//print date to log
const d = Date();
console.log(d);

//pull the pathname from window location
const activePage = window.location.pathname;
console.log(window);
console.log(window.location);
console.log(activePage);

/*create an arey of the links in nav, 
compare each to pathname and mark the one that is active
*/ 
const navLinks = document.querySelectorAll('div a').forEach(link => {    
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
});


//clock function


setInterval(showTime, 1000);
function showTime() {
	let time = new Date();
	let hour = time.getHours();
	let min = time.getMinutes();
	let sec = time.getSeconds();
	am_pm = "AM";

	if (hour > 12) {
		hour -= 12;
		am_pm = "PM";
	}
	if (hour == 0) {
		hr = 12;
		am_pm = "AM";
	}

	hour = hour < 10 ? "0" + hour : hour;
	min = min < 10 ? "0" + min : min;
	sec = sec < 10 ? "0" + sec : sec;

	let currentTime = hour + ":"
			+ min + ":" + sec + am_pm;

	document.getElementById("clock")
			.innerHTML = currentTime;
}
showTime();



