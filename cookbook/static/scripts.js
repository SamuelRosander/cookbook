function confirmDelete(name, url) {
    if (confirm("Are you sure you want to delete " + name + "?")) {
        window.location.href=url;
    }
}

function dismiss(element){
    element.parentNode.classList.add("hidden");
};

flashes = document.getElementsByClassName("flash");
for (let i=0; i<flashes.length; i++) {
    flashes[i].addEventListener("transitionend", () =>  { 
        flashes[i].style.display = "none"; 
    }) 
}

function toggleUserMenu() {
    document.getElementById("user-menu").classList.toggle("visible");
    document.getElementById("navbar").classList.remove("visible");
    document.getElementById("heading-menu").classList.remove("visible");
}

function toggleMenu() {
    document.getElementById("navbar").classList.toggle("visible");
    document.getElementById("user-menu").classList.remove("visible");
    document.getElementById("heading-menu").classList.remove("visible");
}

function toggleHeadingMenu() {
    document.getElementById("heading-menu").classList.toggle("visible");
    document.getElementById("user-menu").classList.remove("visible");
    document.getElementById("navbar").classList.remove("visible");
}

document.onmouseup = function(e) {
    if ((e.target.id != "menu-icon") 
            && (e.target.id != "user-icon")
            && (e.target.parentElement.id != "user-menu")
            && (e.target.id != "heading-menu-btn")
            && (e.target.parentElement.id != "heading-menu-btn")
            && (e.target.parentElement.id != "heading-menu")) {
        document.getElementById("user-menu").classList.remove("visible");
        document.getElementById("navbar").classList.remove("visible");
        document.getElementById("heading-menu").classList.remove("visible");
    }
}

function changeHeading() {
    let headings = document.getElementsByClassName("heading-grid")
    
    for (let i=0; i<headings.length; i++) {
        headings[i].classList.toggle("hidden");
    }

    document.getElementById("name").focus()
    document.getElementById("name").select()
}