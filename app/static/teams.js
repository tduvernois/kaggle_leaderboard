function getTeamSubmissions(name){
    let team_name = name.value

    $.get('/team_submissions/' + team_name, null)
        .done(function(response) {
            cleanTable()
            updateTable(response, team_name)
        }).fail(function() {
            console.log("error")
        });

}

function updateTable(submissions, team_name){

    var parent = $('#table_submissions')[0]
    var thead = document.createElement("thead");
    parent.append(thead);

    var domString = `<thead><tr> \
            <th style="text-align:center">Submission Time</th> \
            <th style="text-align:center">Liberty US Score</th> \
            <th style="text-align:center">Liberty Spain Score</th> \
            <th style="text-align:center">Global Score</th> \
        </tr></thead><tbody id="table-body"></tbody>`
    thead.outerHTML = domString;


    console.log(submissions.length)
    for (let i = 0; i < submissions.length; i++) {
        var tr = document.createElement("tr");
        // preprend before
        parent = $('#table-body')[0]
        parent.append(tr);
        let timestamp = submissions[i].timestamp
        let score_libertyUs = submissions[i].score_libertyUs
        let score_libertySpain = submissions[i].score_LibertySpain
        let score_global = score_libertyUs + score_libertySpain

        var domString = `<td style="text-align:center">${timestamp}</td> \
        <td style="text-align:center">${score_libertyUs.toFixed(3)}</td> \
        <td style="text-align:center">${score_libertySpain.toFixed(3)}</td> \
        <td style="text-align:center">${score_global.toFixed(3)}</td>`
        tr.outerHTML =  domString;
    }

    var best_score = updateBestScore(submissions)

    // update dom best score element
    parent = $('#best_score')[0]
    var domString = `<p style="margin-top: 20px;">${team_name} best score: ${best_score.toFixed(3)}</p>`
//    var domString = `<div class="ui statistic" style="margin-top: 20px;"><div class="value">${best_score}</div><div class="label">Best score</div>`
    parent.innerHTML =  domString;




}

function cleanTable(){
    $('#table_submissions')[0].innerHTML = ''
}

function updateBestScore(submissions){

    var best_score = 0
    for (let i = 0; i < submissions.length; i++) {
        var global_score = submissions[i].score_libertyUs + submissions[i].score_LibertySpain
        if(global_score > best_score){
            best_score = global_score
        }
    }
    return best_score
}
