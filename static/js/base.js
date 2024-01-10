

document.getElementById('nameBrand').onclick = function() {
        let url = "/home";
        window.location.href = `${url}`;
};

document.getElementById('popularLink').onclick = function() {
        let url = "/home/popular";
        window.location.href = `${url}`;
};

document.getElementById('modalSignUpBtn').onclick = function() {
        let url = "/home/signup";
        window.location.href = `${url}`;
};

document.getElementById('searchBtn').onclick = function() {
        let url = "/home/search";
        let query = searchInput.value;
        window.location.href = `${url}#${query}`;
};