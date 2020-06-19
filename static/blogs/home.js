up_clicked = 'no';
down_clicked = 'no';
saved = 'no';
function upvote(ele,secEle) {
    down_clicked = 'no'
    if(up_clicked == 'no') {
        up_clicked = 'yes';
        document.getElementById(ele).className = "fas fa-thumbs-up green fa-2x";
        document.getElementById(secEle).className = "fas fa-thumbs-down white fa-2x";        
    }
    else {
        document.getElementById(ele).className = "fas fa-thumbs-up white fa-2x";   
        up_clicked = 'no';
    }
}

function downvote(ele,secEle) {
    up_clicked = 'no';
    if(down_clicked == 'no') {
        down_clicked = 'yes';
        document.getElementById(ele).className = "fas fa-thumbs-down red fa-2x";
        document.getElementById(secEle).className = "fas fa-thumbs-up white fa-2x";        
    }
    else {
        down_clicked = 'no';
        document.getElementById(ele).className = "fas fa-thumbs-down white fa-2x";
    }

}

function save(ele) {
    if(saved == 'no'){
        document.getElementById(ele).className = "fas fa-bookmark save fa-2x";
        saved = 'yes';
    }
    else {
        saved = 'no';
        document.getElementById(ele).className = "fas fa-bookmark gray fa-2x";
    }
}



