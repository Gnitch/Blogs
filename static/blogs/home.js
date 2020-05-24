function upvote(ele,secEle) {
    document.getElementById(ele).className = "fas fa-thumbs-up green";
    document.getElementById(secEle).className = "fas fa-thumbs-down white";
}

function downvote(ele,secEle) {
        document.getElementById(ele).className = "fas fa-thumbs-down red";
    document.getElementById(secEle).className = "fas fa-thumbs-up white";
}

function save(ele) {
    document.getElementById(ele).className = "fas fa-bookmark save";
}

document.getElementById('id_cover').className = "btn btn-secondary"
document.getElementById('id_video').className = "btn btn-secondary"


