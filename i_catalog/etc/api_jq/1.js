$.ajax({
    type: "POST",
    url: "API_ENDPOINT",
    dataType: 'json',
    headers: {
        "Authorization": "Basic " + btoa(
            ID + ":" + TOKEN
        )
    },
    success: function (data){
        // Work with data
        console.log('Data'); 
    }
});