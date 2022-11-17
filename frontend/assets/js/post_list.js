// 맨 위에 imageRetrieceBseUrl 을 정의해줍니다.
const postListBseUrl = "http://127.0.0.1:5000/posts/";
const imageBseUrl = "http://127.0.0.1:5000/statics/";

/**
 * getPostListDatafromAPI() 로부터 게시물 목록 데이터를 불러옵니다.
 * 불러온 데이터 결과의 길이만큼 (페이지네이션 처리) 게시물을 반복해 그립니다.
 */
function loadPosts() {
  getPostListDatafromAPI()
    .then((result) => {
      for (let i = 0; i < result.length; i++) {
        copyDiv();
        // 커버 이미지 요소를 선택하고 그립니다.
        const coverImageElements = document.querySelector("post-image");
        coverImageElements.src =
          imageBseUrl + result[result.length - 1 - i]["image"];
        // 저자 이름 요소를 선택하고, 그립니다.
        const upAuthorElement = document.querySelector("author-up");
        upAuthorElement.innerText =
          result[result.length - 1 - i]["author_name"];
        const downAuthorElement = document.querySelector("author-down");
        downAuthorElement.innerText =
          result[result.length - 1 - i]["author_name"];
        // 제목 요소를 선택하고 그립니다.
        const titleElement = document.querySelector("title");
        titleElement.innerText = result[result.length - 1 - i]["title"];
        // 내용 요소를 선택하고 그립니다.
        const contentElement = document.querySelector("content");
        contentElement.innerText = result[result.length - 1 - i]["content"];
        // 게시물이 없다면 none 처리를 합니다.
        if (i == 0) {
          document.getElementById("copied-posts").style.display = "none";
        }
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

loadPosts(); // 최종 함수 호출
