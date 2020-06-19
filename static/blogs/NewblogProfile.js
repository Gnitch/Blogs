document.getElementById('id_cover').className = "btn btn-secondary"
document.getElementById('id_video').className = "btn btn-secondary"
document.getElementById('id_video').setAttribute('onchange','Filevalidation()'); 

console.log(document.getElementById('id_video') )
Filevalidation = () => { 
    const fi = document.getElementById('id_video'); 
    // Check if any file is selected. 
    if (fi.files.length > 0) { 
        for (const i = 0; i <= fi.files.length - 1; i++) { 

            const fsize = fi.files.item(i).size; 
            const file = Math.round((fsize / 1024)); 
            if (file >=  104857600) { 
                alert("File too Big, Please select a file less than 100mb"); 
                  $("#id_video").val("")
            } 
        } 
    } 
} 














