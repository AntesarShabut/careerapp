function storeNameAndEmail() {
    // get the name and email from the input fields
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;

    // store the name and email in local storage
    localStorage.setItem("name", name);
    localStorage.setItem("email", email);
}

// save the name and email before leaving the page
window.addEventListener("beforeunload", storeNameAndEmail);

window.addEventListener("load", function() {
    // retrieve the name and email from local storage and set the input fields
    var name = localStorage.getItem("name");
    var email = localStorage.getItem("email");
    document.getElementById("name").value = name;
    document.getElementById("email").value = email;
});