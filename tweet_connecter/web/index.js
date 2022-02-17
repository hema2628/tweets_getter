window.onload = function (){


    author_list = document.getElementById("author_bar");
    tweets_field = document.getElementById("tweets_list");
    authors = []

    // $.ajax({
    //     url: '../../tweet_connecter/web/tweeter.csv',
    //     dataType: 'text',
    //   }).done(successFunction);
    //
    // function successFunction(data){
    //     console.log(data)
    //     data = eel.get_IDlist("tweeter.csv")
    //     creat_author_list(data);
    //     tweets_field.innerHTML = "<h3>No tweets shown here</h3>";
    // }

    eel.get_IDlist("web/tweeter.csv")




}

eel.expose(init_page)
function init_page(message){


    creat_author_list(message)
}

function getJsonObject(path, success, error) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                if (success) success(JSON.parse(xhr.responseText));
            } else {
                if (error) error(xhr);
            }
        }
    };
    xhr.open("GET", path, true);
    xhr.send();
}

function search_tweets(value){
    console.log(value)

    // values = value.split(',');
    // author_name = values[0];
    // author_id = values[1];


    // getJsonObject('../../tweet_connecter/web/tweetCollection/'+author_id+'.json',
    //     function (data){
    //
    //         creat_tweet_list(data,author_name,author_id);
    //     },
    //     function(xhr) { console.error(xhr); })

    eel.tweet_getter_by_Id(value)

}

function creat_author_list(data){


    var allRows = data.toString().split(/\r?\n|\r/);
    allRows = allRows[0].split(",");

    for (var singleRow = 0; singleRow < allRows.length; singleRow++) {
        var rowCells = allRows[singleRow];

        if(singleRow<=3){

            $("#author_bar").prepend("<li><a id='"+rowCells.toString()+"' onclick='search_tweets(this.id)' href='#'>"+rowCells+"</a></li>")
        }else{
            document.getElementById("dropdown_menu").innerHTML+="<li><a id='"+rowCells.toString()+"' onclick='search_tweets(this.id)' href='#'>"+rowCells+"</a></li>"
        }

        }

}

eel.expose(creat_tweet_list)
function creat_tweet_list(data){
    // var tweetsOBJ = data.split(/\r?\n|\r/).slice(1,);
    var tweetsOBJ = data
    console.log(tweetsOBJ)
    author_name = tweetsOBJ[0].user.name
    author_id = tweetsOBJ[0].user.screen_name
    tweeter_author_id = tweetsOBJ[0].user.id;

    tweets = ""
    tweets += "<div id=\"tweeter_info\"><p id=\"author_name\">Tweeter: "+author_name+"</p>\n" +
        "    <p id=\"author_id\">Author id: "+author_id+"</p>"+
        "    <p id=\"tweet_author_id\">Tweet author id: "+tweeter_author_id+"</p></div>"

    for (var i = 0; i<tweetsOBJ.length; i++){

        tweets += creat_tweet_box(tweetsOBJ[i],);
    }


    tweets_field.innerHTML = tweets;


}

function creat_tweet_box(tweet_info){
    var date = new Date(tweet_info.created_at);
    img_url = ""
    link = ""
    if(tweet_info.entities.media){
        img_url = tweet_info.entities.media[0].media_url
        link = tweet_info.entities.media[0].url
    }else{
        img_url = tweet_info.user.profile_image_url
        link = "https://twitter.com/"+tweet_info.user.screen_name
    }



    tweet_box = "<div class=\"tweet_box\">\n" +
        "            <div style=\"display: inline-block\" class=\"tweetbox_left\">"+
        "            <div id=\"tweet_text\"><b class=\"titles\"></b><br>"+ tweet_info.text+"</div>\n" +
        "            <div id=\"authorname\"><b class=\"titles\">By: </b> "+ author_name+"</div>\n" +
        "            <div id=\"created_at\"><b class=\"titles\">Created time: </b> "+ date+"</div></div>\n" +
        "            <div style=\"display: inline-block\" class=\"tweetbox_right\">" +
        "            <img src=\""+img_url+"\" alt=\"\">" +
        "            <a href=\""+link+"\"> click to view details >>></a>"+
        "            </div>"+
        "        </div>"

    return tweet_box
}