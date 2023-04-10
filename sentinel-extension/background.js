chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  chrome.tabs.executeScript(tabs[0].id, { file: "content.js" });

  chrome.tabs.executeScript(tabs[0].id, {
    code: 'localStorage.setItem("BACKGROUND", "' + Date.now() + '");',
  });
});


console.log("BACKGROUND SCRIPT RUNNING !!!!");

  
const responseStartedHandler = (details)=>{
  console.log("RESPONSE STARTED DETAILS : ");
  console.log(details)
}

chrome.webRequest.onHeadersReceived.addListener(
  responseStartedHandler,
  { urls: ["<all_urls>"] },
  ["responseHeaders"]
);
