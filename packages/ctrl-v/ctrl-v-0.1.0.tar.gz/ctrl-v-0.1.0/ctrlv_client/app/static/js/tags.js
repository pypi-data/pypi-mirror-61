const tagBox = document.querySelector("#tagbox");
const availableTagsDiv = document.querySelector("#availableTags");
const tagsInput = document.querySelector("#tags");

function addToTags(str){
  tagsInput.value += tagsInput.value? ',' + str:str;
}

function removeFromTags(str){
  let tagsArr = tagsInput.value.split(',');
  tagsArr = tagsArr.filter(item => item != str);
  tagsInput.value = tagsArr.join(',');
}

function tagRemove(elem){
  removeFromTags(
    elem.closest('.tag').querySelector('.tagname').textContent
  );
  
  elem.closest('.tag').remove();
}

function tagAdd(str){
  if(!tagsInput.value.split(',').includes(str)){
    let tag = `
      <div class='tag'>
        <span class='tagname'>${str}</span>
        <button type="button" class='' onclick='tagRemove(this)'>x</button>
      </div>
    `;
    let tagListDiv = document.querySelector("#taglist");
    tagListDiv.innerHTML += tag;
    addToTags(str);
  }
  hideAvailableTags();
  tagBox.value = '';
}

function showAvailableTags(str){
  let li_str = '';
  for(let curr_tag of availableTags){
    if(curr_tag.includes(str) && !tagsInput.value.split(',').includes(curr_tag)){
      li_str += `
        <li><a onclick='tagAdd(this.textContent)'>${curr_tag}</a></li>
      `;   
    }
  }
  availableTagsDiv.innerHTML = li_str;
}

function hideAvailableTags(){
  availableTagsDiv.innerHTML = '';
}


tagBox.addEventListener('keydown', function(event) {
    let tag_value = this.value.trim().toLowerCase();
    if (event.code == 'Enter') {
      if (tag_value){
        tagAdd(tag_value);
        // Don't submit the form!
        event.preventDefault();
      }
    }
    else if(event.code == 'Backspace'){
      let input_text_value = document.querySelector("#tagbox").value;
      let last_tag = document.querySelector("#taglist div:last-of-type");
      if(last_tag && !input_text_value){
        tagRemove( 
          last_tag
        );
      }
    }
    else if((event.code >= 'KeyA' && event.code <= 'KeyZ') || event.code=="Space"){
      // if alphabet
      // console.log(event.code[event.code.length-1]);
      // this.value.trim() will not include last pressed key
      tag_value += event.key.toLowerCase();
      showAvailableTags(tag_value);
      
    }
});