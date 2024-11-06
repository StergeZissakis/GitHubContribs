async function spawnThread(statusField, url, results, resultsIndex) {
    setTimeout(function(){
        $.get(url).done(function(data, statusText, xhr) {
            results[resultsIndex] = data.results
            $(statusField).val(data.status)
        })
        .fail(function(jqXHR, statusText, errorThrown) {
            $(statusField).val(statusText)
        })
    }, 0)
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).ready(function() {

    $("#run").on( "click", async function() {
        $("#run").prop( "disabled", true )

        $('#commitsStatus').val("")
        $('#issuesStatus').val("")
        $('#pullsStatus').val("")
        $("#results").val("")

        var userName = $("#userName").val() || 'nlohmann'
        var toDate = $("#toDate").val()
        var fromDate = $("#fromDate").val()

        uriQueryStr = ""
        if( fromDate )
            uriQueryStr += "?start_date=" + fromDate
        if( toDate ){
            if( fromDate )
                uriQueryStr += "&"
            else
                uriQueryStr += "?"
            uriQueryStr += "end_date=" + toDate
        }
        uriQueryStr = "/" + uriQueryStr

        urls = []
        statusFields = []
        if( $('#commits').prop('checked') ) {
            urls.push("http://" + window.location.host.split(":")[0] + ":8000/commits/"+ userName + uriQueryStr)
            statusFields.push('#commitsStatus')
        }
        if( $('#issues').prop('checked') == true ) {
            urls.push("http://" + window.location.host.split(":")[0] + ":8000/issues/"+ userName + uriQueryStr)
            statusFields.push('#issuesStatus')
        }
        if( $('#pullRequests').prop('checked') == true ) {
            urls.push("http://" + window.location.host.split(":")[0] + ":8000/pulls/"+ userName + uriQueryStr)
            statusFields.push('#pullsStatus')
        }

        if( urls.length == 0) {
            $("#run").prop( "disabled", false )
            return
        }

        results = new Array(urls.length)

        for (var i = 0; i < urls.length; i++) {
            spawnThread(statusFields[i], urls[i], results, i);
        }

        // wait for all threads to finish
        var keepLooping = true
        while(keepLooping) {
            var ok = true
            for (var i = 0; i < statusFields.length; i++) {
                ok &= $(statusFields[i]).val().length > 0
            }
            if(ok){
                keepLooping = false
            } else {
                await sleep(1000)
            }
        }

        if( results.length ) {
            finalResult = new Array(results[0].length)
            for (var i = 0; i < results[0].length; i++)
                finalResult[i] = 0

            for (var i = 0; i < results.length; i++) {
                for(var j = 0; j < results[i].length; j++){
                    finalResult[j] += results[i][j]
                }
            }
            $("#results").val(finalResult)
        }

        $("#run").prop( "disabled", false )
    });

});
