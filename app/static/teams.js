function getTeamSubmissions(name){
    let team_name = name.value

    $.get('/team_submissions/' + team_name, null)
        .done(function(response) {
            cleanTable()
            updateTable(response)
        }).fail(function() {
            console.log("error")
        });

}

function updateTable(submissions){

    var parent = $('#table_submissions')[0]
    var tr = document.createElement("tr");
    parent.append(tr);

    var domString = `<tr> \
            <th style="text-align:center">Submission Time</th> \
            <th style="text-align:center">Liberty US Score</th> \
            <th style="text-align:center">Liberty Spain Score</th> \
            <th style="text-align:center">Global Score</th> \
        </tr>`
    tr.outerHTML = domString;


    console.log(submissions.length)
    for (let i = 0; i < submissions.length; i++) {
        var tr = document.createElement("tr");
        // preprend before
        parent.append(tr);
        let timestamp = submissions[i].timestamp
        let score_libertyUs = submissions[i].score_libertyUs
        let score_libertySpain = submissions[i].score_LibertySpain
        let score_global = score_libertyUs + score_libertySpain

        var domString = `<td style="text-align:center">${timestamp}</td> \
        <td style="text-align:center">${score_libertyUs}</td> \
        <td style="text-align:center">${score_libertySpain}</td> \
        <td style="text-align:center">${score_global}</td>`
        tr.outerHTML =  domString;
    }
}

function cleanTable(){
    $('#table_submissions')[0].innerHTML = ''
}

