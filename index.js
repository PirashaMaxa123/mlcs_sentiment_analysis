import $ from 'jquery';
let review = {
  review:"It was bad"
};

//$.post("http://localhost:5000/sentimentForReview", JSON.stringify(review));

let promise = $.ajax({
  method: "POST",
  url: "http://localhost:5000/sentimentForReview",
  data: JSON.stringify(review),
  contentType: "application/json; charset=utf-8", // "application/json; charset=utf-8"
  dataType:"json"
});

promise.then(
  data => console.log("data: ", data),
  error => console.log('error: ', error)
);