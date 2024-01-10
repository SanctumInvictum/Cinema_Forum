


// http://127.0.0.1:8000/api/posts/search?query=%D0%9A%D0%BE%D0%BD%D1%82%D0%B5%D0%BD%D1%82&limit=10&page=1&sortby=id



window.onload = function () {
    let url = "/api/posts/search";
    let parameters;
    // console.log("location.hash", window.location.hash);
    // let parameters = `query=${location.hash}&sortby=id`;

    if (location.hash) {
        parameters = `&sortby=id&query=${location.hash.toString()}`;
    } else {
        return 0;
    }

    $.ajax({
           url: url,
           method: 'get',
           data: parameters,
           async: true,
           timeout: 10000, // 10 sec
           success: function(result){
               let posts = result["posts"];

                for (let i = 0; i < posts.length; i++) {
                    let datePost = new Date(Date.parse(posts[i].created_at));
                    let copyCard = div.cloneNode(true);
                    let reviewUrl = `reviews/${posts[i].id}`;

                    // ДОБАВИТЬ USERNAME, КЛИК ПО КАТЕГОРИЯМ (ФИЛЬТР)
                    copyCard.setAttribute("id", posts[i].id);
                    copyCard.getElementsByClassName("day")[0].innerHTML = datePost.getDate();
                    copyCard.getElementsByClassName("month")[0].innerHTML = months[datePost.getMonth()];
                    copyCard.getElementsByClassName("media-body")[0].children[0].children[0].innerHTML = posts[i].title;
                    copyCard.getElementsByClassName("media-body")[0].childNodes[1].href += reviewUrl;
                    copyCard.getElementsByClassName("media-body")[0].childNodes[2].textContent = posts[i].content.slice(0, 50) + "...";
                    copyCard.getElementsByClassName("media-body")[0].childNodes[3].href += reviewUrl;
                    // console.log(copyCard.getElementsByClassName("row")[0].childNodes[1].textContent = `by: ${posts[i].username}`);
                    copyCard.getElementsByClassName("row")[0].childNodes[3].textContent = `Likes: ${posts[i].likes_count}`;
                    copyCard.getElementsByClassName("row")[0].children[2].children[0].href += reviewUrl;
                    copyCard.getElementsByClassName("row")[0].children[2].children[0].textContent = `${posts[i].comments_count} comments`;
                    copyCard.getElementsByClassName("row")[0].children[3].textContent = `Date: ${datePost.getDate()}.${datePost.getMonth()+1}.${datePost.getFullYear()}`;
                    copyCard.getElementsByClassName("media blog-media w-100")[0].children[0].href = reviewUrl;
                    $(divContent).append(copyCard);

                }

           }
        });

}