






var script = document.createElement("script");
//script.src = chrome.extension.getURL("https://cdn.jsdelivr.net/gh/h2non/jshashes/hashes.min.js");
script.src = chrome.extension.getURL(
  "hashes.js"
);

document.head.appendChild(script);







// Decryptor

async function decryptor(key,iv,encrypted){
  // var key_str = "XrrzfjJ8bICWZZB1CvpdMw==";
  // var iv_str = "WUd+gTBrheXMQsAKRtmDTg==";
  // var encrypted_str = "Ws6Fz6vq8WZmT6dXpXgRPF0RJ8sP+e2QxU6/lGJ2oz0=";
  // Convert the base64 strings back to bytes
  key = base64ToArrayBuffer(key);
  iv = base64ToArrayBuffer(iv);
  encrypted = base64ToArrayBuffer(encrypted);
  // Decrypt the message using Web Crypto
  let decrypted = '';
  decrypted =  await window.crypto.subtle
    .decrypt(
      { name: "AES-CBC", iv: iv },
      await window.crypto.subtle.importKey('raw',key,'AES-CBC',true,['decrypt']),
      encrypted
    )
    .then(function (decrypted) {
      // Convert the decrypted bytes to a string
      let plaintext = new TextDecoder().decode(decrypted);
      //console.log("Decrypted message:", plaintext);
      return plaintext;
    });

    return decrypted;

}
// Utility function to convert a base64 string to an ArrayBuffer
function base64ToArrayBuffer(base64) {
  var binary_string = atob(base64);
  var len = binary_string.length;
  var bytes = new Uint8Array(len);
  for (var i = 0; i < len; i++) {
    bytes[i] = binary_string.charCodeAt(i);
  }
  return bytes.buffer;
}

//x-----------Decryptor----------------x




async function sendTOTPCode(code) {
  const endpointUrl = "http://localhost:5000/key";
  const requestBody = {
    code: code,
  };

  const response = await fetch(endpointUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestBody),
  });

  if (!response.ok) {
    throw new Error("Failed to send TOTP code to server.");
  }
}







const clean_dom_content = (domContent)=>{
  const lines = domContent.split('\n');
  let concatenated = "";
  for(let line of lines){
    const trimmed = line.trim();
    if(trimmed!==""){
      concatenated+=(trimmed)+'\n';
    }
  }
  return concatenated.substring(0,concatenated.length-1);
};


setTimeout(() => {
 

  // Select all the <vault> elements in the DOM
  const vaults = document.querySelectorAll("vault");


  // Loop through each <vault> element and create a shadow DOM
  vaults.forEach((vault) => {
    const vaultChildNodes = vault.childNodes;

    const div = document.createElement("div");

    const shadow = div.attachShadow({ mode: "open" });

    // Loop through each child node of the <vault> element and add it to the shadow DOM
    vaultChildNodes.forEach((node) => {
      let copy = node.cloneNode(true);
      shadow.appendChild(copy);
    });

    vault.replaceWith(div);
  });

  let SHA512 = new Hashes.SHA512;
  

  let concatenated="";

  for(let vault of vaults){
    const cleaned = clean_dom_content("<vault>" + vault.innerHTML + "</vault>");
    concatenated += cleaned;
  }

//   console.log(concatenated);
// console.log(SHA512.hex(concatenated));


decryptor('3+/9FztTczQKeXRwrq3FfA==','2geixy4sdJgZCRs6Kj+9TQ==','83XUIPuSSi6nmZoIuyPK2Q==');


}, 1000);

const encrypted_nodes = document.querySelectorAll("encrypted");


encrypted_nodes.forEach(async (node)=>{
  const [encrypted,iv] = node.innerHTML.split('||');
  const resp = await fetch('/key');
  const data = await resp.json();
  console.log(data);
  const decrypted = await decryptor(data.key,iv,encrypted);
  node.innerHTML = decrypted;
});



console.log("BACKROUND RUNNING : "+chrome.extension.getBackgroundPage());
