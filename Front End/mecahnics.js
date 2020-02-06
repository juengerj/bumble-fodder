const lorem = "  Lorem ipsum dolor sit amet consectetur adipisicing elit. Voluptas, eius fugit ex amet, commodi adipisci accusamus laudantium provident dolore impedit quos obcaecati nesciunt odit sequi doloremque distinctio nihil ipsam exercitationem!\
"
markers = [false, false, false, false, false];

function deleteSubreddit(elementId) {
  // alert("This totally works");
  var findAnchor = document.getElementById("containersOfSubreddits");
  findAnchor.removeChild(document.getElementById(elementId));
  markers[elementId] = false;
}

function assignId() {
  for(var i = 0; i < 5; ++i) {
    if(!markers[i]) {
      markers[i] = true;
      return i;
    }
  }
}

function addSubreddit() {
  const scrappingsLimit = 5;
  let currentScrappings = document.getElementsByClassName("addedSubreddit").length;
  //get url from box
  let saying = document.getElementById("enteredSubreddit").value;
  let index = assignId();
  // alert(index);

  //create container for scraping
  let subredditAnchor = document.getElementById("containersOfSubreddits");
  if (currentScrappings < scrappingsLimit) {
    let subreddit2add = document.createElement("div");
    subreddit2add.classList.add("addedSubreddit");
    subreddit2add.setAttribute("id", index);
    let subreddit2addTitle = document.createElement("h4");
    subreddit2addTitle.innerText = saying;

    let subreddit2addContent = document.createElement("div");
    subreddit2addContent.innerText = lorem;

    let subreddit2addDeleteButton = document.createElement("button");
    subreddit2addDeleteButton.classList.add("button")
    subreddit2addDeleteButton.classList.add("btn-danger")
    subreddit2addDeleteButton.innerText = "DELETE";
    subreddit2addDeleteButton.type = "button";
    subreddit2addDeleteButton.addEventListener("click", function(){
      deleteSubreddit(index);
    });

    subreddit2add.appendChild(subreddit2addTitle);
    subreddit2add.appendChild(subreddit2addContent);
    subreddit2add.appendChild(subreddit2addDeleteButton);
    subredditAnchor.appendChild(subreddit2add);

  }
  else {
    alert("SCRAPPING CAP REACHED!!");
  }
  //use entered uubredditurl as title of container
  //fil with lorem ipsum
  //add buttom to remove container.
}

//prevent form submission because there is nothing to submit to.
let form = document.getElementById("subRedditForm");
document.getElementById("subRedditForm").addEventListener("submit", function(event){
  event.preventDefault()
}, false);