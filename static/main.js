// ファイルアップロード 
$(function () {
  $('#fileform').on('submit', uploadFiles);
});

function uploadFiles (event) {
  event.preventDefault(); // Prevent the default form post

  var file = $('#fileform [name=imagefile]')[0].files[0];
  var reader = new FileReader();

  reader.onloadend = sendFileToCloudVision;
  reader.readAsDataURL(file);
}

function sendFileToCloudVision (event) {
  var content = event.target.result;
  // 読み込んだ画像の表示
  $('#in_img').attr('src', content);
  
  // リクエストの作成
  var request = {
    requests: [{
      image: {
        content: content.split(',')[1]
      },
      features: [{}],
    }]
  };

  // POST処理
  $.post({
    url: 'img_api',
    data: JSON.stringify(request),
    contentType: 'application/json'
  }).fail(function (jqXHR, textStatus, errormsg) {
    $('#results').text('error: ' + textStatus + ' ' + errormsg);
  }).done(displayJSON);
}

// レスポンス表示
function displayJSON (data) {
  var contents = JSON.stringify(data, null, 4);
  var out_img_url ="data:image/png;base64," + data['image']
  $('#results').text(contents);
  var evt = new Event('results-displayed');
  evt.results = contents;
  document.dispatchEvent(evt);
  $('#out_img').attr('src', out_img_url);
}
