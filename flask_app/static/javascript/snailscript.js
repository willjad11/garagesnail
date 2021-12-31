searchbox = document.getElementById('searchtext');

function switchcontent(x) {
    if (x == 1) {
        document.getElementById("box4").style.display = "none"
        document.getElementById("box4-2").style.display = ""
    }
    if (x == 0) {
        document.getElementById("box4").style.display = ""
        document.getElementById("box4-2").style.display = "none"
    }
}

function search() {
    let ul = document.getElementById("sresults");
    let li = ul.getElementsByTagName("li");
    let input = document.getElementById("searchtext");
    let filter = input.value.toUpperCase();
    ul.style.display = "";
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        }
        else {
            li[i].style.display = "none";
        }
    }
}

function search_hide() {
    let sresults = document.getElementById("sresults");
    sresults.style.display = "none";
}

searchbox.addEventListener('keyup', function (event) {
    const key = event.key;
    if (key === "Backspace") {
        search_hide();
    }
}
);