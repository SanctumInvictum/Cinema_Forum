
let htmlString = `
  <div id="cardId" class="row pt-1 px-5">
    <div class="col-md-10">
        <div class="media blog-media w-100">
            <a href="blog-post-left-sidebar.html"><img class="d-flex"
                                                       src="https://www.bootdey.com/image/350x380/6495ED/000000"
                                                       alt="Generic placeholder image"></a>
            <div class="circle">
                <h5 class="day">14</h5>
                <span class="month">sep</span>
            </div>
            <div class="media-body">
                <a href=""><h5 class="mt-0">Standard Blog Post</h5></a>
                Sodales aliquid, in eget ac cupidatat velit autem numquam ullam ducimus occaecati placeat error.
                <a href="" class="post-link">Read More</a>

                <div class="row">
                    <div class="col-sm text-center">by: username</div>
                    <div class="col-sm text-center">Love: 10</div>
                    <div class="col-sm text-center"><a href="">07 comments</a></div>
                    <div class="col-sm text-center">Date: 14.09.2023</div>
                </div>

            </div>
        </div>
    </div>
</div>
`;


let months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];


window.onload = function () {
// $(document).ready(function () {
    let divContent = '#page-content-wrapper';
    let cardContent = '#cardContent';
    let content = [];
    let url = "/api/posts";
    // let parameters = "limit=4&page=2&sortby=created_at"; // ЭТО СО СКИПОМ
    let parameters = "limit=8&page=1&sortby=created_at";

    // пример карточки
    let div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    div = div.firstChild;

    $.ajax({
           url: url,
           method: 'get',
           data: parameters,
           async: true,
           timeout: 10000, // 10 sec
           success: function(result){
                // console.log(result);
                // console.log(div);
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
                    copyCard.getElementsByClassName("row")[0].childNodes[1].textContent = `by: ${posts[i].username}`;
                    copyCard.getElementsByClassName("row")[0].childNodes[3].textContent = `Likes: ${posts[i].likes_count}`;
                    copyCard.getElementsByClassName("row")[0].children[2].children[0].href += reviewUrl;
                    copyCard.getElementsByClassName("row")[0].children[2].children[0].textContent = `${posts[i].comments_count} comments`;
                    copyCard.getElementsByClassName("row")[0].children[3].textContent = `Date: ${datePost.getDate()}.${datePost.getMonth()+1}.${datePost.getFullYear()}`;
                    copyCard.getElementsByClassName("media blog-media w-100")[0].children[0].href = reviewUrl;
                    $(divContent).append(copyCard);

                }

           }
        });




};

